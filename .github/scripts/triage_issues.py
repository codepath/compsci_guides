"""
Triage GitHub issues for the compsci_guides wiki using Claude.
- Fetches open issues (or a single triggered issue)
- Fetches the relevant wiki page content
- Asks Claude to evaluate the feedback
- Creates ONE Asana task (with subtasks per issue) in both
  'Curriculum Asks' and 'Course Delivery Asks' projects
- Labels issues for easy human review (no comments posted)
"""

import os
import re
import json
import requests
import anthropic
from github import Github
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
REPO_NAME = os.environ["REPO_NAME"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
ASANA_ACCESS_TOKEN = os.environ["ASANA_ACCESS_TOKEN"]
TRIGGER_ISSUE_NUMBER = os.environ.get("TRIGGER_ISSUE_NUMBER", "")

ASANA_PROJECT_NAMES = ["Curriculum Asks", "Course Delivery Asks"]
ASANA_API = "https://app.asana.com/api/1.0"
ALREADY_TRIAGED_LABEL = "claude-triaged"
VALID_FEEDBACK_LABEL = "needs-review"
INVALID_FEEDBACK_LABEL = "invalid"
WIKI_BASE_URL = f"https://raw.githubusercontent.com/wiki/{REPO_NAME}"

# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_wiki_page(page_name: str) -> str | None:
    safe_name = page_name.strip().replace(" ", "-")
    url = f"{WIKI_BASE_URL}/{safe_name}.md"
    r = requests.get(url, timeout=10)
    return r.text if r.status_code == 200 else None


def guess_wiki_page(issue_title: str, issue_body: str) -> tuple[str, str | None]:
    combined = f"{issue_title}\n{issue_body}"
    url_match = re.search(r'wiki/([^\s\)\"]+)', combined)
    if url_match:
        content = fetch_wiki_page(url_match.group(1))
        return url_match.group(1), content
    content = fetch_wiki_page(issue_title)
    return issue_title, content


def ensure_label_exists(repo, name: str, color: str, description: str):
    try:
        repo.get_label(name)
    except Exception:
        repo.create_label(name=name, color=color, description=description)


def already_triaged(issue) -> bool:
    return any(lbl.name == ALREADY_TRIAGED_LABEL for lbl in issue.labels)


# ── Claude evaluation ─────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a teaching assistant for a computer science course.
You review GitHub issues submitted by students who believe they found errors
in wiki pages containing coding problem solutions.

Your job:
1. Read the student's issue carefully.
2. If wiki page content is provided, check whether their concern is valid.
3. Respond with a JSON object (no markdown fences) with these fields:
   - "verdict": "valid" | "invalid" | "unclear"
   - "confidence": "high" | "medium" | "low"
   - "summary": one sentence explaining your verdict
   - "suggestion": if valid, a concrete suggestion for fixing the wiki page;
                   if invalid, a brief explanation of why the issue should be closed;
                   if unclear, what additional information is needed
"""

def evaluate_issue(title: str, body: str, wiki_content: str | None) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    wiki_section = (
        f"<wiki_page_content>\n{wiki_content[:6000]}\n</wiki_page_content>"
        if wiki_content
        else "<wiki_page_content>Could not be fetched — evaluate based on the issue alone.</wiki_page_content>"
    )
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"<issue_title>{title}</issue_title>\n<issue_body>{body or '(no body)'}</issue_body>\n{wiki_section}"}],
    )
    raw = response.content[0].text.strip()
    raw = re.sub(r"^```[a-z]*\n?|```$", "", raw, flags=re.MULTILINE).strip()
    return json.loads(raw)


# ── Asana ─────────────────────────────────────────────────────────────────────

def asana_headers() -> dict:
    return {
        "Authorization": f"Bearer {ASANA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }


def get_project_ids(project_names: list[str]) -> dict[str, str]:
    """Return a mapping of project name -> project GID."""
    # First get all workspaces
    r = requests.get(f"{ASANA_API}/workspaces", headers=asana_headers())
    workspaces = r.json().get("data", [])

    found = {}
    for ws in workspaces:
        r = requests.get(
            f"{ASANA_API}/projects",
            headers=asana_headers(),
            params={"workspace": ws["gid"], "limit": 100}
        )
        for project in r.json().get("data", []):
            if project["name"] in project_names:
                found[project["name"]] = project["gid"]
        if len(found) == len(project_names):
            break

    missing = set(project_names) - set(found.keys())
    if missing:
        print(f"  Warning: Could not find Asana projects: {missing}")
    return found


def create_asana_task(project_gid: str, title: str, notes: str) -> str | None:
    """Create a parent task in a project and return its GID."""
    r = requests.post(
        f"{ASANA_API}/tasks",
        headers=asana_headers(),
        json={"data": {
            "name": title,
            "notes": notes,
            "projects": [project_gid]
        }}
    )
    data = r.json().get("data")
    return data["gid"] if data else None


def create_asana_subtask(parent_gid: str, name: str, notes: str):
    """Create a subtask under a parent task."""
    requests.post(
        f"{ASANA_API}/tasks/{parent_gid}/subtasks",
        headers=asana_headers(),
        json={"data": {"name": name, "notes": notes}}
    )


def build_subtask_notes(result: dict) -> str:
    verdict = result["verdict"].upper()
    confidence = result.get("confidence", "unknown")
    summary = result.get("summary", "")
    suggestion = result.get("suggestion", "")
    url = result["url"]

    action = {
        "valid": "✅ Recommended Action: Fix the wiki page",
        "invalid": "🔴 Recommended Action: Close the GitHub issue",
        "unclear": "❓ Recommended Action: Manual review needed"
    }.get(result["verdict"], "")

    return (
        f"GitHub Issue: {url}\n\n"
        f"Verdict: {verdict} (confidence: {confidence})\n"
        f"Summary: {summary}\n\n"
        f"Suggestion: {suggestion}\n\n"
        f"{action}"
    )


def create_batch_asana_tasks(triaged: list[dict], project_ids: dict[str, str]):
    """Create one parent task with subtasks in each project."""
    today = datetime.now().strftime("%B %d, %Y")
    valid_count = sum(1 for r in triaged if r["verdict"] == "valid")
    invalid_count = sum(1 for r in triaged if r["verdict"] == "invalid")
    unclear_count = sum(1 for r in triaged if r["verdict"] == "unclear")

    parent_title = f"GitHub Issue Triage — {today}"
    parent_notes = (
        f"Automated triage of open GitHub issues for github.com/{REPO_NAME}/wiki\n\n"
        f"Issues reviewed: {len(triaged)}\n"
        f"  • Valid (fix needed): {valid_count}\n"
        f"  • Invalid (close recommended): {invalid_count}\n"
        f"  • Unclear (manual review): {unclear_count}\n\n"
        f"See subtasks for individual issue details and recommendations."
    )

    for project_name, project_gid in project_ids.items():
        print(f"  Creating Asana task in '{project_name}'...")
        parent_gid = create_asana_task(project_gid, parent_title, parent_notes)
        if not parent_gid:
            print(f"  Failed to create parent task in '{project_name}'")
            continue

        for result in triaged:
            verdict_emoji = {"valid": "⚠️", "invalid": "✅", "unclear": "❓"}.get(result["verdict"], "")
            subtask_name = f"{verdict_emoji} #{result['number']}: {result['title']}"
            subtask_notes = build_subtask_notes(result)
            create_asana_subtask(parent_gid, subtask_name, subtask_notes)
            print(f"    Subtask created: {subtask_name}")


# ── Main ──────────────────────────────────────────────────────────────────────

def process_issue(issue, repo) -> dict | None:
    if already_triaged(issue):
        print(f"  Skipping #{issue.number} — already triaged.")
        return None

    print(f"  Processing issue #{issue.number}: {issue.title}")
    _, wiki_content = guess_wiki_page(issue.title, issue.body or "")
    result = evaluate_issue(issue.title, issue.body or "", wiki_content)
    verdict = result.get("verdict", "unclear")
    print(f"    Verdict: {verdict} (confidence: {result.get('confidence')})")

    issue.add_to_labels(ALREADY_TRIAGED_LABEL)
    if verdict == "valid":
        issue.add_to_labels(VALID_FEEDBACK_LABEL)
    elif verdict == "invalid":
        issue.add_to_labels(INVALID_FEEDBACK_LABEL)

    return {
        "number": issue.number,
        "title": issue.title,
        "url": issue.html_url,
        "verdict": verdict,
        "confidence": result.get("confidence"),
        "summary": result.get("summary", ""),
        "suggestion": result.get("suggestion", ""),
    }


def main():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    ensure_label_exists(repo, ALREADY_TRIAGED_LABEL, "0075ca", "Triaged by Claude")
    ensure_label_exists(repo, VALID_FEEDBACK_LABEL, "e4e669", "Valid — needs human review")
    ensure_label_exists(repo, INVALID_FEEDBACK_LABEL, "ee0701", "Invalid feedback")

    triaged = []

    if TRIGGER_ISSUE_NUMBER:
        issue = repo.get_issue(int(TRIGGER_ISSUE_NUMBER))
        result = process_issue(issue, repo)
        if result:
            triaged.append(result)
    else:
        for issue in repo.get_issues(state="open"):
            if issue.pull_request:
                continue
            result = process_issue(issue, repo)
            if result:
                triaged.append(result)

    if triaged:
        project_ids = get_project_ids(ASANA_PROJECT_NAMES)
        create_batch_asana_tasks(triaged, project_ids)
    else:
        print("No new issues to triage.")


if __name__ == "__main__":
    main()

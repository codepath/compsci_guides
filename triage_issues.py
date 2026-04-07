"""
Triage GitHub issues for the compsci_guides wiki using Claude.
- Fetches open issues (or a single triggered issue)
- Fetches the relevant wiki page content
- Asks Claude to evaluate the feedback
- Posts a comment with a suggestion or dismissal
- Labels the issue for easy human review
"""

import os
import re
import requests
import anthropic
from github import Github

# ── Config ────────────────────────────────────────────────────────────────────
REPO_NAME = os.environ["REPO_NAME"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TRIGGER_ISSUE_NUMBER = os.environ.get("TRIGGER_ISSUE_NUMBER", "")

WIKI_BASE_URL = f"https://raw.githubusercontent.com/wiki/{REPO_NAME}"
ALREADY_TRIAGED_LABEL = "claude-triaged"
VALID_FEEDBACK_LABEL = "needs-review"
INVALID_FEEDBACK_LABEL = "invalid"

# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_wiki_page(page_name: str) -> str | None:
    """Try to fetch the raw content of a wiki page by name."""
    # Wiki pages use underscores for spaces in raw URLs
    safe_name = page_name.strip().replace(" ", "-")
    url = f"{WIKI_BASE_URL}/{safe_name}.md"
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        return r.text
    return None


def guess_wiki_page(issue_title: str, issue_body: str) -> tuple[str, str | None]:
    """
    Try to extract a wiki page name from the issue title or body.
    Returns (page_hint, page_content).
    """
    # Look for explicit mentions of a wiki page or problem name
    combined = f"{issue_title}\n{issue_body}"
    # Heuristic: look for a capitalized multi-word phrase or URL fragment
    url_match = re.search(r'wiki/([^\s\)\"]+)', combined)
    if url_match:
        page_name = url_match.group(1).replace("-", " ").replace("_", " ")
        content = fetch_wiki_page(url_match.group(1))
        return page_name, content

    # Fall back: use the issue title as the page hint
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
                   if invalid, a polite explanation of why the code is correct;
                   if unclear, what additional information is needed
   - "comment_for_student": a friendly GitHub comment to post on the issue
     (use markdown; mention whether a fix will be made or why the issue will be closed)
"""

def evaluate_issue(title: str, body: str, wiki_content: str | None) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    wiki_section = (
        f"<wiki_page_content>\n{wiki_content[:6000]}\n</wiki_page_content>"
        if wiki_content
        else "<wiki_page_content>Could not be fetched — evaluate based on the issue alone.</wiki_page_content>"
    )

    user_message = f"""
<issue_title>{title}</issue_title>
<issue_body>{body or '(no body)'}</issue_body>
{wiki_section}
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    import json
    raw = response.content[0].text.strip()
    raw = re.sub(r"^```[a-z]*\n?|```$", "", raw, flags=re.MULTILINE).strip()
    return json.loads(raw)


# ── Main ──────────────────────────────────────────────────────────────────────

def process_issue(issue, repo):
    if already_triaged(issue):
        print(f"  Skipping #{issue.number} — already triaged.")
        return

    print(f"  Processing issue #{issue.number}: {issue.title}")

    page_hint, wiki_content = guess_wiki_page(issue.title, issue.body or "")
    print(f"    Wiki page hint: {page_hint} — content fetched: {wiki_content is not None}")

    result = evaluate_issue(issue.title, issue.body or "", wiki_content)
    verdict = result.get("verdict", "unclear")
    print(f"    Verdict: {verdict} (confidence: {result.get('confidence')})")
    print(f"    Summary: {result.get('summary')}")

    # Post Claude's comment
    comment_body = result.get("comment_for_student", "")
    footer = (
        "\n\n---\n*This initial triage was performed automatically by Claude. "
        "A human maintainer will review and take final action.*"
    )
    issue.create_comment(comment_body + footer)

    # Apply labels
    issue.add_to_labels(ALREADY_TRIAGED_LABEL)
    if verdict == "valid":
        issue.add_to_labels(VALID_FEEDBACK_LABEL)
    elif verdict == "invalid":
        issue.add_to_labels(INVALID_FEEDBACK_LABEL)


def main():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Ensure labels exist
    ensure_label_exists(repo, ALREADY_TRIAGED_LABEL, "0075ca", "Triaged by Claude")
    ensure_label_exists(repo, VALID_FEEDBACK_LABEL, "e4e669", "Valid — needs human review")
    ensure_label_exists(repo, INVALID_FEEDBACK_LABEL, "ee0701", "Invalid feedback")

    if TRIGGER_ISSUE_NUMBER:
        # Triggered by a specific new issue
        issue = repo.get_issue(int(TRIGGER_ISSUE_NUMBER))
        process_issue(issue, repo)
    else:
        # Scheduled run — process all open, untriaged issues
        open_issues = repo.get_issues(state="open")
        for issue in open_issues:
            if issue.pull_request:
                continue  # Skip PRs
            process_issue(issue, repo)


if __name__ == "__main__":
    main()

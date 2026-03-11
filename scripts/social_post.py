#!/usr/bin/env python3
"""
Auto-post new Vibelyo articles to social media platforms.

Supported platforms: medium, linkedin, pinterest
Usage:  social_post.py <platform>

Required env vars per platform:
  Medium:    MEDIUM_TOKEN, SITE_URL, NEW_FILES
  LinkedIn:  LINKEDIN_TOKEN, LINKEDIN_PERSON_URN, SITE_URL, NEW_FILES
  Pinterest: PINTEREST_TOKEN, PINTEREST_BOARD_ID, SITE_URL, NEW_FILES
"""

import os
import sys
import requests
import frontmatter


SITE_URL = os.environ.get("SITE_URL", "https://vibelyo.site")


def get_post_url(filepath: str) -> str:
    """Convert a content filepath to its live URL.
    e.g. content/blogging/my-post.md → https://vibelyo.site/blogging/my-post/
    """
    slug = filepath.replace("content/", "").replace(".md", "")
    return f"{SITE_URL}/{slug}/"


def get_new_files() -> list[str]:
    """Read new file list from the NEW_FILES env var (set by GitHub Actions)."""
    raw = os.environ.get("NEW_FILES", "").strip()
    if not raw:
        return []
    return [f.strip() for f in raw.splitlines() if f.strip()]


# ---------------------------------------------------------------------------
# Medium
# ---------------------------------------------------------------------------

def post_to_medium(filepath: str) -> None:
    token = os.environ.get("MEDIUM_TOKEN", "")
    if not token:
        print("  MEDIUM_TOKEN missing — skipped")
        return

    post = frontmatter.load(filepath)
    if post.get("draft", False):
        print(f"  Draft post, skipping: {filepath}")
        return

    title = post.get("title", "Untitled")
    description = post.get("description", "")
    tags = post.get("tags", [])[:5]          # Medium allows max 5 tags
    canonical_url = get_post_url(filepath)

    # Get the authenticated user's Medium ID
    me = requests.get(
        "https://api.medium.com/v1/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    me.raise_for_status()
    user_id = me.json()["data"]["id"]

    # Build markdown body — prepend a canonical attribution line
    body = (
        f"# {title}\n\n"
        f"*Originally published at [{SITE_URL}]({canonical_url})*\n\n"
        f"{post.content}"
    )

    payload = {
        "title": title,
        "contentFormat": "markdown",
        "content": body,
        "tags": tags,
        "canonicalUrl": canonical_url,
        "publishStatus": "public",
    }

    resp = requests.post(
        f"https://api.medium.com/v1/users/{user_id}/posts",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=20,
    )

    if resp.status_code in (200, 201):
        url = resp.json()["data"].get("url", "")
        print(f"  ✅ Medium: {url}")
    else:
        print(f"  ❌ Medium error {resp.status_code}: {resp.text}")


# ---------------------------------------------------------------------------
# LinkedIn
# ---------------------------------------------------------------------------

def post_to_linkedin(filepath: str) -> None:
    token = os.environ.get("LINKEDIN_TOKEN", "")
    person_urn = os.environ.get("LINKEDIN_PERSON_URN", "")

    if not token or not person_urn:
        print("  LinkedIn credentials missing — skipped")
        return

    post = frontmatter.load(filepath)
    if post.get("draft", False):
        print(f"  Draft post, skipping: {filepath}")
        return

    title = post.get("title", "Untitled")
    description = post.get("description", "")
    tags = post.get("tags", [])
    url = get_post_url(filepath)

    # Build hashtags from tags (remove spaces/hyphens, add #)
    hashtags = " ".join(
        f"#{t.replace(' ', '').replace('-', '').replace('_', '')}"
        for t in tags[:5]
    )

    commentary = (
        f"📝 New post on Vibelyo: {title}\n\n"
        f"{description}\n\n"
        f"{hashtags}\n\n"
        f"🔗 {url}"
    )

    payload = {
        "author": f"urn:li:person:{person_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": commentary},
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {"text": description},
                        "originalUrl": url,
                        "title": {"text": title},
                    }
                ],
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }

    resp = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        json=payload,
        timeout=15,
    )

    if resp.status_code in (200, 201):
        print(f"  ✅ LinkedIn: post published")
    else:
        print(f"  ❌ LinkedIn error {resp.status_code}: {resp.text}")


# ---------------------------------------------------------------------------
# Pinterest
# ---------------------------------------------------------------------------

def post_to_pinterest(filepath: str) -> None:
    token = os.environ.get("PINTEREST_TOKEN", "")
    board_id = os.environ.get("PINTEREST_BOARD_ID", "")

    if not token or not board_id:
        print("  Pinterest credentials missing — skipped")
        return

    post = frontmatter.load(filepath)
    if post.get("draft", False):
        print(f"  Draft post, skipping: {filepath}")
        return

    title = post.get("title", "Untitled")
    description = post.get("description", "")
    url = get_post_url(filepath)

    payload = {
        "board_id": board_id,
        "title": title,
        "description": description,
        "link": url,
        "alt_text": title,
    }

    resp = requests.post(
        "https://api.pinterest.com/v5/pins",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=15,
    )

    if resp.status_code in (200, 201):
        pin_id = resp.json().get("id", "")
        print(f"  ✅ Pinterest pin created: {pin_id}")
    else:
        print(f"  ❌ Pinterest error {resp.status_code}: {resp.text}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

PLATFORM_MAP = {
    "medium": post_to_medium,
    "linkedin": post_to_linkedin,
    "pinterest": post_to_pinterest,
}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: social_post.py <medium|linkedin|pinterest>")
        sys.exit(1)

    platform = sys.argv[1].lower()
    handler = PLATFORM_MAP.get(platform)
    if not handler:
        print(f"Unknown platform '{platform}'. Choices: {', '.join(PLATFORM_MAP)}")
        sys.exit(1)

    files = get_new_files()
    if not files:
        print("No new files in NEW_FILES — nothing to post.")
        return

    for filepath in files:
        if not os.path.exists(filepath):
            print(f"File not found (may have been renamed): {filepath}")
            continue
        print(f"→ {filepath}")
        handler(filepath)


if __name__ == "__main__":
    main()

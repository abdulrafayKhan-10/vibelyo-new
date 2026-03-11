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
# X (Twitter)
# ---------------------------------------------------------------------------

def post_to_x(filepath: str) -> None:
    import tweepy

    api_key = os.environ.get("X_API_KEY", "")
    api_secret = os.environ.get("X_API_SECRET", "")
    access_token = os.environ.get("X_ACCESS_TOKEN", "")
    access_secret = os.environ.get("X_ACCESS_SECRET", "")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("  X credentials missing — skipped")
        return

    post = frontmatter.load(filepath)
    if post.get("draft", False):
        print(f"  Draft post, skipping: {filepath}")
        return

    title = post.get("title", "Untitled")
    tags = post.get("tags", [])
    url = get_post_url(filepath)

    hashtags = " ".join(
        f"#{t.replace(' ', '').replace('-', '').replace('_', '')}"
        for t in tags[:3]  # Keep tweet concise
    )

    # Build tweet — stay under 280 chars
    base = f"New on Vibelyo: {title}\n\n{hashtags}\n\n{url}"
    if len(base) > 280:
        # Trim title if needed
        max_title = 280 - len(f"New on Vibelyo: ...\n\n{hashtags}\n\n{url}")
        title = title[:max_title] + "..."
        base = f"New on Vibelyo: {title}\n\n{hashtags}\n\n{url}"

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
    )

    try:
        response = client.create_tweet(text=base)
        tweet_id = response.data["id"]
        print(f"  ✅ X: tweet posted — https://x.com/i/web/status/{tweet_id}")
    except tweepy.TweepyException as exc:
        print(f"  ❌ X error: {exc}")


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
    "x": post_to_x,
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

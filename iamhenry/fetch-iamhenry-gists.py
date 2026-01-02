#!/usr/bin/env python3

import requests
import json
import os
from typing import List, Dict


def fetch_all_gists(username: str, token: str | None = None) -> List[Dict]:
    """Fetch all gists for a given GitHub username."""
    url = f"https://api.github.com/users/{username}/gists"
    headers = {"Accept": "application/vnd.github.v3+json"}

    if token:
        headers["Authorization"] = f"token {token}"

    all_gists = []
    page = 1
    per_page = 100

    while True:
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error fetching gists: {response.status_code}")
            print(response.text)
            break

        gists = response.json()
        if not gists:
            break

        all_gists.extend(gists)
        print(f"Fetched {len(gists)} gists (page {page})")

        if len(gists) < per_page:
            break

        page += 1

    return all_gists


def fetch_gist_content(gist_url: str, token: str | None = None) -> Dict[str, str]:
    """Fetch the actual file contents of a gist."""
    headers = {"Accept": "application/vnd.github.v3+json"}

    if token:
        headers["Authorization"] = f"token {token}"

    response = requests.get(gist_url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching gist content: {response.status_code}")
        return {}

    gist_data = response.json()
    files = {}

    for filename, file_info in gist_data.get("files", {}).items():
        raw_url = file_info.get("raw_url")
        if raw_url:
            file_response = requests.get(raw_url, headers=headers)
            if file_response.status_code == 200:
                files[filename] = file_response.text

    return files


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be safe for filesystem."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


def main():
    token = os.environ.get("GITHUB_TOKEN")
    username = "iamhenry"

    print(f"Fetching all gists for {username}...")
    gists = fetch_all_gists(username, token or "")

    print(f"\nTotal gists found: {len(gists)}")

    output_dir = f"{username}-gists"
    os.makedirs(output_dir, exist_ok=True)

    for gist in gists:
        gist_id = gist["id"]
        description = gist.get("description") or "no-description"
        sanitized_desc = sanitize_filename(description)
        gist_dir = os.path.join(output_dir, f"{gist_id}-{sanitized_desc}")
        os.makedirs(gist_dir, exist_ok=True)

        print(f"\nFetching gist: {description}")

        files = fetch_gist_content(gist["url"], token or "")

        for filename, content in files.items():
            sanitized_filename = sanitize_filename(filename)
            file_path = os.path.join(gist_dir, sanitized_filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  - Saved: {sanitized_filename}")

        gist_info_path = os.path.join(gist_dir, "gist-info.json")
        with open(gist_info_path, "w") as f:
            gist_info = {
                "id": gist["id"],
                "description": gist.get("description"),
                "html_url": gist["html_url"],
                "created_at": gist["created_at"],
                "updated_at": gist["updated_at"],
                "public": gist["public"],
            }
            json.dump(gist_info, f, indent=2)

    output_file = f"{username}-gists.json"
    with open(output_file, "w") as f:
        json.dump(gists, f, indent=2)

    print(f"\nAll gists saved to {output_dir}/")
    print(f"Gist metadata saved to {output_file}")


if __name__ == "__main__":
    main()

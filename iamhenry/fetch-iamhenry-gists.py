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


def main():
    token = os.environ.get("GITHUB_TOKEN")
    username = "iamhenry"

    print(f"Fetching all gists for {username}...")
    gists = fetch_all_gists(username, token or "")

    print(f"\nTotal gists found: {len(gists)}")

    for gist in gists:
        print(f"- {gist['description'] or 'No description'} ({gist['html_url']})")

    output_file = f"{username}-gists.json"
    with open(output_file, "w") as f:
        json.dump(gists, f, indent=2)

    print(f"\nSaved to {output_file}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Export your solved LeetCode problems to CSV using LeetCode's progress query.

Windows PowerShell:
  py -m pip install requests
  $env:LEETCODE_SESSION = "YOUR_COOKIE_VALUE"
  py .\export_leetcode_solved.py

Output: leetcode_solved_problems.csv in the same folder as this script.
Never share your LEETCODE_SESSION cookie.
"""

import csv
import os
import sys
from pathlib import Path

import requests

URL = "https://leetcode.com/graphql/"
OUTPUT_FILE = Path(__file__).with_name("leetcode_solved_problems.csv")

QUERY = """
query userProgressQuestionList($filters: UserProgressQuestionListInput) {
  userProgressQuestionList(filters: $filters) {
    totalNum
    questions {
      frontendId
      title
      titleSlug
      difficulty
      lastSubmittedAt
      topicTags {
        name
      }
    }
  }
}
"""

def main():
    session_cookie = os.environ.get("LEETCODE_SESSION")
    if not session_cookie:
        sys.exit(
            'LEETCODE_SESSION is missing. In PowerShell, run:\n'
            '$env:LEETCODE_SESSION = "YOUR_COOKIE_VALUE"'
        )

    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Origin": "https://leetcode.com",
        "Referer": "https://leetcode.com/progress/",
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"LEETCODE_SESSION={session_cookie}",
    })

    all_questions = []
    skip = 0
    limit = 100
    total = None

    while total is None or skip < total:
        payload = {
            "query": QUERY,
            "variables": {
                "filters": {
                    "questionStatus": "SOLVED",
                    "skip": skip,
                    "limit": limit,
                }
            },
        }

        try:
            response = session.post(URL, json=payload, timeout=30)
        except requests.RequestException as exc:
            sys.exit(f"Network error contacting LeetCode: {exc}")

        if not response.ok:
            print(f"LeetCode returned HTTP {response.status_code}.")
            print("Response body (first 3000 characters):")
            print(response.text[:3000])
            sys.exit(
                "\nThe request was rejected. LeetCode's internal API may have changed. "
                "Do not share your session cookie."
            )

        try:
            body = response.json()
        except ValueError:
            sys.exit("LeetCode did not return JSON; it may have returned a security/check page.")

        if body.get("errors"):
            print("LeetCode GraphQL errors:")
            for error in body["errors"]:
                print("-", error.get("message", error))
            sys.exit(
                "\nThe GraphQL query was rejected. The schema may have changed. "
                "Do not share your session cookie."
            )

        result = (body.get("data") or {}).get("userProgressQuestionList")
        if result is None:
            sys.exit("Response did not contain userProgressQuestionList.")

        total = int(result.get("totalNum") or 0)
        questions = result.get("questions") or []
        if not questions:
            break

        all_questions.extend(questions)
        skip += len(questions)
        print(f"Retrieved {min(skip, total)} of {total} solved problems...")

        if len(questions) < limit:
            break

    # Deduplicate and sort by the visible LeetCode problem number.
    unique = {}
    for q in all_questions:
        number = str(q.get("frontendId") or "").strip()
        slug = q.get("titleSlug") or ""
        if not number or not slug:
            continue
        tags = q.get("topicTags") or []
        unique[number] = {
            "Problem Number": number,
            "Title": q.get("title") or "",
            "Difficulty": q.get("difficulty") or "",
            "URL": f"https://leetcode.com/problems/{slug}/",
            "Last Accepted Timestamp": q.get("lastSubmittedAt") or "",
            "Topics": ", ".join(t.get("name", "") for t in tags if t.get("name")),
        }

    def sort_key(row):
        n = row["Problem Number"]
        return (0, int(n)) if n.isdigit() else (1, n.lower())

    rows = sorted(unique.values(), key=sort_key)
    if not rows:
        sys.exit(
            "No solved problems were returned. Confirm your LeetCode account shows "
            "solved questions on its Progress page."
        )

    columns = [
        "Problem Number", "Title", "Difficulty", "URL",
        "Last Accepted Timestamp", "Topics",
    ]
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSuccess: exported {len(rows)} unique solved problems.")
    print(f"CSV saved to: {OUTPUT_FILE}")
    print("Import it into Google Sheets: File > Import > Upload.")

if __name__ == "__main__":
    main()

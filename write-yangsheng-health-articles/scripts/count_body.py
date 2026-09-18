#!/usr/bin/env python3
"""Count non-whitespace characters in an extracted plain-text article body.

Include section headings and the disclaimer. Exclude the article title,
byline, sources, and editorial notes before passing the text to this script.
Markdown must be converted to visible plain text by the caller.
"""

import argparse
from pathlib import Path
import sys


def count_characters(body: str) -> int:
    """Count punctuation, letters, and digits individually; ignore whitespace."""
    return sum(not character.isspace() for character in body)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="UTF-8 plain-text body file, or - for stdin")
    parser.add_argument("--min-length", type=int, default=800)
    parser.add_argument("--max-length", type=int, default=1000)
    args = parser.parse_args()
    if not 0 <= args.min_length <= args.max_length:
        parser.error("length bounds must satisfy 0 <= min-length <= max-length")
    try:
        body = (
            sys.stdin.read().removeprefix("\ufeff")
            if args.path == "-"
            else Path(args.path).read_text(encoding="utf-8-sig")
        )
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    count = count_characters(body)
    valid = args.min_length <= count <= args.max_length
    status = "PASS" if valid else "FAIL"
    print(f"{count} characters; target {args.min_length}-{args.max_length}: {status}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())

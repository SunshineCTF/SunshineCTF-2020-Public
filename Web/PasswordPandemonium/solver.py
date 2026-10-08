#!/usr/bin/env python3
# PasswordPandemonium solver.
#
# The /sign_up endpoint validates a password against ~10 rules (length, a prime
# count of digits, equal upper/lower, >=3 symbols, contains an emoji, MD5 hash
# begins with a digit, must be valid QuickJS that evaluates truthy but not to a
# string, and must be a palindrome). Supplying a password that passes every rule
# (plus any non-empty username) returns the flag. Several short palindromic
# JavaScript snippets satisfy all the rules at once; submit candidates until the
# server hands back the sun{...} flag.
import os
import re
import sys

import requests

URL = os.environ.get("URL") or (sys.argv[1] if len(sys.argv) > 1 else
                                "https://passwordpandemonium.ctf.hackucf.org")
URL = URL.rstrip("/")

# Palindromic snippets that pass QuickJS + every analytics rule (from the writeup).
CANDIDATES = [
    "(_=>(1))()//Xx\U0001f42cxX//)())1(>=_(",
    "()=>{}//Ab1\U0001f44b1bA//}{>=)(",
    "1//Ab✔bA//1",
]


def attempt(password):
    r = requests.post(f"{URL}/sign_up",
                      data={"username": "solver", "password": password},
                      timeout=15)
    m = re.search(r"sun\{[^}]*\}", r.text)
    return m.group(0) if m else None


def main():
    for pw in CANDIDATES:
        flag = attempt(pw)
        if flag:
            print(f"password: {pw!r}")
            print(flag)
            return 0
    print("NO FLAG FOUND", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

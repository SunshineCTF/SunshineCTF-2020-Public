#!/usr/bin/env python3
# TSATechie solver (device-enrollment stage).
#
# The offline part of the challenge recovers the device serial, derives the UDID
#   UDID = SHA1(serial + ECID + wifiMac + bluetoothMac)
#        = 1d87930059bad8eab14bebb81d7680c02a299ac6
# and the model iPhone10,1. The web stage at POST /udid/verify expects an Apple
# configuration PLIST carrying those two values; when both match, the server
# 301-redirects to a secret /udid/<flag-without-sun> page that renders the flag.
# Posting the plist and following the redirect yields the sun{...} flag.
import os
import re
import sys

import requests

URL = os.environ.get("URL") or (sys.argv[1] if len(sys.argv) > 1 else
                                "https://tsatechie.ctf.hackucf.org")
URL = URL.rstrip("/")

UDID = "1d87930059bad8eab14bebb81d7680c02a299ac6"
PRODUCT = "iPhone10,1"

PLIST = (
    '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
    '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
    '<plist version="1.0">\n'
    '<dict>\n'
    '    <key>UDID</key>\n'
    f'    <string>{UDID}</string>\n'
    '    <key>PRODUCT</key>\n'
    f'    <string>{PRODUCT}</string>\n'
    '</dict>\n'
    '</plist>\n'
)


def main():
    # requests follows the 301 to /udid/<flag-without-sun>, which renders the flag.
    r = requests.post(f"{URL}/udid/verify", data=PLIST.encode(),
                      headers={"Content-Type": "application/x-plist"}, timeout=15)
    m = re.search(r"sun\{[^}]*\}", r.text)
    if m:
        print(m.group(0))
        return 0
    print("NO FLAG FOUND", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

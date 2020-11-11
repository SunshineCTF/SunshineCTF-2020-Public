#!/usr/bin/env python3

# Special thanks to Warsame_Egeh for letting me view his implementation for device enrollment.

import xml.etree.ElementTree as ET
import re
from flask import Flask, send_file, request, Response, redirect, render_template
app = Flask(__name__)

# Load flag as global variable on launch.
with open("flag.txt") as f:
     flag = f.read()
     flag_nosun = flag[4:-1]

def get_plist(inp):
    binary = inp.decode("utf-8", "ignore")
    # Clear out all of that pesky "binary" stuff.
    stri = re.sub(r"[^\x00-\x7f]",r"", binary)
    start = stri.index("<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">")
    end = stri.index("</plist>") + 8
     # And now we have our PLIST as a string.
    return stri[start:end]

@app.route("/")
def home():
    return send_file(
            "index.html",
            attachment_filename="index.html",
            mimetype="text/html"
        )

@app.route("/udid/")
@app.route("/udid")
def home_redir():
    return redirect("/")

@app.route("/udid/enroll")
def enroll():
    try:
        return send_file(
            "enrollment.mobileconfig",
            attachment_filename="enrollment.mobileconfig",
            mimetype="application/x-apple-aspen-config; chatset=utf-8"
        )
    except:
        return "<p>You were supposed to get a device enrollment challenge but something went awry. Report this to the CTF organizers.</p>"

@app.route("/udid/verify", methods=["POST"])
def verify():
    try:
        # Get plist
        pl = get_plist(request.get_data())
        # Parse it by treating it like XML!
        # Odd iteration: Key
        # Even iteration: Value
        root = ET.fromstring(pl)[0]
        memory = ""

        data = {
            "product": "",
            "udid": ""
        }

        for child in root:
            if child.tag.lower() == "key":
                # Key Mode
                memory = child.text.lower()
            elif child.tag.lower() == "string":
                # Value Mode
                data[memory] = child.text

        # If the UDID inputted is valid, show the user the flag!
        if data["udid"] == "1d87930059bad8eab14bebb81d7680c02a299ac6" and data["product"] == "iPhone10,1":
            return redirect(f"/udid/{flag_nosun}", 301)
        else:
            return redirect("/udid/flag", 301)
    except:
        return redirect("/udid/flag", 301)

@app.route("/udid/flag")
def finalize():
    # idea: show plist response here?
    return send_file(
            "error.html",
            attachment_filename="error.html",
            mimetype="text/html"
        )

@app.route(f"/udid/{flag_nosun}")
def works():
    # Render flag template.
    return render_template("flag.html", FLAG=flag)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)

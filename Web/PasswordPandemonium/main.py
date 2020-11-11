# Related to validator
import hashlib
from emoji import UNICODE_EMOJI
import quickjs
from sympy import isprime

# Load flag as global variable on launch.
with open("flag.txt") as f:
     flag = f.read()

# Related to web server
from flask import Flask, request, Response, render_template, send_file
app = Flask(__name__)

"""
String validate(passwd)

@param String passwd The password to validate.

@return An error message, or the string "PASS" if passed.
"""
def validate(passwd) -> (str, bool):
    # print(passwd)
    # First check: Minimum length
    if len(passwd) < 8:
        return "Password is too short.", False
    # Second check: Maximum length
    if len(passwd) > 32:
        return "Password is too long.", False

    # Password analytics check
    analytics = {
        "upper": 0,
        "lower": 0,
        "num": 0,
        "symbol": 0,
        "emoji": 0
    }
    arr = list(passwd)
    for char in arr:
        if char.isupper():
            analytics["upper"] += 1
        elif char.islower():
            analytics["lower"] += 1
        elif char.isdigit():
            analytics["num"] += 1
        elif not char.isalpha():
            analytics["symbol"] += 1
        # https://stackoverflow.com/a/36217640
        if char in UNICODE_EMOJI:
            analytics["emoji"] += 1

    # Third check: Must include a letter.
    if analytics["upper"] == 0 and analytics["lower"] == 0:
        return "Password must include at least one letter.", False

    # Fourth check: Symbol count
    if analytics["symbol"] < 3:
        return "Password must include more than two special characters.", False

    # Fifth check: Must have prime amount of numbers
    if not isprime(analytics["num"]):
        return "Password must include a prime amount of numbers.", False

    # Sixth check: SpOnGeGaR cHeCk
    if analytics["upper"] != analytics["lower"]:
        return "Password must have equal amount of uppercase and lowercase characters.", False

    # Seventh check: Must include an emoji
    if analytics["emoji"] == 0:
        return "Password must include an emoji.", False

    # Eight check: Hash must start with a number
    if not list(hashlib.md5(passwd.encode()).hexdigest())[0].isdigit():
        return "Password's MD5 hash must start with a number.", False

    # Ninth check: Must be valid JavaScript (eval'd with QuickJS)
    try:
        context = quickjs.Context()
        context.set_time_limit(5)
        run = context.eval(passwd)
        if not run:
            return "Password must be valid JavaScript that evaluates to True.", True
        elif type(run) == str:
            return "Password must be valid JavaScript that doesn't return a string.", True
    except:
        return "Password must be valid JavaScript that evaluates to True.", True


    # Tenth check: Must be a palindrome.
    if (passwd != passwd[::-1]):
        return "Password must be a palindrome.", False 

    return "PASS", False

# Web server endpoints
@app.route("/")
@app.route("/sign_up")
def home():
    # Render login page template
    return render_template("index.html")

@app.route("/sign_up", methods=["POST"])
def process():
    data = request.form
    if not data["username"] or len(data["username"]) == 0:
        return render_template("err.html", error="No username supplied.")

    out, do_marquee = validate(data["password"])
    if out == "PASS":
        # return flag
        return render_template("pass.html", flag=flag)
    else:
        # return error
        return render_template("err.html", error=out, marquee=do_marquee)

# serves stylesheet
@app.route('/index.css')
def serve_css():
    return send_file(
            "index.css",
            attachment_filename="index.css",
            mimetype="text/css"
    )

# serves image
@app.route('/logo.png')
def serve_logo():
    return send_file(
            "logo.png",
            attachment_filename="logo.png",
            mimetype="image/png"
    )

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)
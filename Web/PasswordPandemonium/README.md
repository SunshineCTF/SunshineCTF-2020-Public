# [Web 100] PasswordPandemonium

A simple challenge where you have to craft a specifically-crafted password with the following requirements (in order):

- Minimum length of 8
- Maximum length of 32
- Must include at least one letter
- Must include >= 2 special characters
- Must include a prime amount of numbers
- Must have even amount of capital and lowercase characters
- Must include an emoji
- MD5 hash must start with a number
- Must be valid JavaScript that evaluates to True
- Must be JavaScript that does not evaluate to a String
- Must be a palindrome

This is created as a Flask app with the following endpoints (excluding static assets):

- `GET /`, `GET /sign_up` The sign-up page.
- `POST /sign_up` Submission verification

As long as these endpoints are handled by the Flask application, in general, it can be deployed however you wish. However, the following is worth noting:

- The flag can be set in `flag.txt`
- Install dependencies with `pip3 i -r requirements.txt`

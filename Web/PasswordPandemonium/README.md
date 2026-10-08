# [Web] PasswordPandemonium

A simple challenge where you have to craft a password that satisfies a long list of sign-up password requirements.

This is created as a Flask app with the following endpoints (excluding static assets):

- `GET /`, `GET /sign_up` The sign-up page.
- `POST /sign_up` Submission verification

As long as these endpoints are handled by the Flask application, in general, it can be deployed however you wish. However, the following is worth noting:

- The flag can be set in `flag.txt`
- Install dependencies with `pip3 i -r requirements.txt`

See [writeup.md](writeup.md) for the solution.

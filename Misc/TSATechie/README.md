# [Misc] TSATechie

A multi-part challenge built around iOS device identifiers and a device enrollment web page.

This is created as a Flask app (see `index.py` for its endpoints). As long as those endpoints are handled by the Flask application, in general, it can be deployed however you wish. However, the following is worth noting:

- The flag can be set in `flag.txt`
- The absolute URL to the device enrollment challenge must be set in `enrollment.mobileconfig` so the profile knows where to send the device's UDID/model.

See [writeup.md](writeup.md) for the solution.

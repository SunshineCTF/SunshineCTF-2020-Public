# [Misc 150] TSATechie

This challenge is made up of multiple smaller challenges that test a player's iOS identifier and device enrollment knowledge. This challenge consists of:
- Hand-crafting a serial number based on given information
- Using the newly-created serial number to generate an iPhone's UDID
- Using this UDID, on top of the given iPhone model, to fake a response from a device enrollment challenge

This is created as a Flask app with the following endpoints:

- `GET /` The home page with a button to begin the device enrollment challenge.
- `GET /udid/enroll` Returns the device enrollment configuration profile.
- `POST /udid/verify` Takes in a PLIST body (string or binary) and redirects to a web page depending if the input PLIST contains the UDID/device we are looking for
- `GET /udid/flag` Shows an error saying the device was invalid
- `GET /udid/:FLAG` The flag. Only returned if the POST contains the expected data.

As long as these endpoints are handled by the Flask application, in general, it can be deployed however you wish. However, the following is worth noting:

- The flag can be set in `flag.txt`
- The absolute URL to the device enrollment challenge must be set in `enrollment.mobileconfig` so the profile knows where to send the device's UDID/model.

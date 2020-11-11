# TSATechie Writeup

This is a multiple-part challenge, most of it which is done offline. The challenge is structured into three main components:
- Hand-crafting a serial number based on given information
- Using the newly-created serial number to generate an iPhone's UDID
- Using this UDID, on top of the given iPhone model, to fake a response from a device enrollment challenge

### A foreward

The serial number and UDID in this challenge are not of iPhones owned by anyone. While it's possible for the serial number to eventually be valid, it was intentionally chosen to be at a future date. The MAC addresses, while theoretically valid (they *do* belong to Apple, are random.

## Creating a Serial Number

The PDF that players are given is designed to reveal all the information needed to craft the rest of the serial number, and later, the UDID.

The serial number given in the PDF is `##T##621J##H`. The goal is to find the missing characters.

As Apple does not document their serial number format publicly, third-party resources have to be relied on. Tab-TV.com has a good, albeit somewhat inaccurate (some information omitted), reference image that says what each of these missing fields are, which can be found with a Google search.

The first two missing characters maps to the Foxconn factory ID in Zhengzhou (`FK`). This information is revealed in multiple ways:
- Plus Code: The `HV55+C8` identifier in the "seized note" is a few blocks away from the factory.
- Flight History: The original departure location is meant to originate near the factory.

The next two missing characters is the production week of the device (`DP`). This information can also be found online and the solution is provided redundantly:
- Flight History: All dates given are in the same week.
- Information: Seizure date is also within the expected week.

The last two missing characters is the device model. Here, it's an [iPhone 8](https://reincubate.com/lookup/FKTDP621JC6H/), as given in the Seized Device section. The numerical identifier for the model (`JC6`) can be found on the Tab-TV diagram, but is also colloborated by a few pieces of information:
- Device: `iPhone10,1` is the device's model and maps to an iPhone 8.
- Flight History: The layover in Japan is a hint that this is a Japanese iPhone. This is mostly trivia, but can be used for checking the final serial number.

Now that the serial number is found, we can craft the UDID.

## Creating a UDID

The [UDID](https://www.theiphonewiki.com/wiki/UDID) is a unique identifier for each iPhone. The iPhone 8 uses an older format for UDIDs, which can be summarized as:
```txt
UDID = SHA1(serial + ECID + wifiMac + bluetoothMac)
```
The ECID and both MAC addresses given are already in the correct format, so this should be a simple excersize in string concatenation and hashing.

The string that should end up getting hashed is:
```txt
FKTDP621JC6H284313561763971814:88:e6:ac:6314:88:e6:ac:64
```
This should output the UDID of the hypothetical device, which is `1d87930059bad8eab14bebb81d7680c02a299ac6`.

This can be verified in the PDF, where the last five characters are exposed for this reason.

## Device Enrollment Challenge

The Web server linked is mostly static files, except for the endpoint at `POST /udid/verify`. This endpoint is linked inside of the `enrollment.mobileconfig` file served by the web server.

This endpoint expects a request body that is a PLIST in the following format:
```plist
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>UDID</key
        <string>1d87930059bad8eab14bebb81d7680c02a299ac6</string>
        <key>PRODUCT</key>
        <string>iPhone10,1</string>
</dict>
</plist>
```
This format can be scraped with a MITM proxy tool like Burp Suite or Charles Proxy running on an iPhone completing the enrollment challenge, however, the body will be sent as a binary PLIST. Additional work may be neccessary to convert it to plaintext on non-Apple software. The response is also documented on Apple's website [here](https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/iPhoneOTAConfiguration/ConfigurationProfileExamples/ConfigurationProfileExamples.html#//apple_ref/doc/uid/TP40009505-CH4-SW6), but it's quite hard to find so it shouldn't be an expected solution.

*It is worth noting that the device enrollment challenge only gets the UDID and model of the device and does not store this data nor is the profile persistent. It is only compared with the known UDID.*

Sending a body in this format (either in plaintext or as a binary) will reveal the flag. Both the UDID and Product fields must be accurate for the flag to be shown.
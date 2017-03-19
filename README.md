# google-location-to-gpx-converter-extractor

- This script allows you to extract a time segment of your Google Location History and convert it into a GPX file.
- The GPX file format used here is compatible with Strava.com, not tested with anything else.
- Useful to extract bike rides out of your Google Maps navigation for instance.

# Caveats

- This scrip likely uses a ton of RAM, because it loads your entire google location history in RAM and for most long-time users of Google Services, that's hundreds of megabytes of JSON (which, turned into Python data structures, will be more like 1-2GB of RAM).
- For the same reason, the script will likely take a little bit of time (likely not more than a minute on <4 years old computer) and a significant amount of CPU, don't worry, that's normal, it's just parsing tons of JSON.

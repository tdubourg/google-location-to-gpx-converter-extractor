#!/usr/bin/python2

######## User-modifiable parts of the script start here #############

# Change this variable value to the path to your Google Location History JSON export.
google_location_history_json_file_path = '/cygdrive/d/data/Downloads/LocationHistory.json'
# Change this variable value to the path where you want to save the result GPX file.
output_gpx_file_path = '/cygdrive/d/data/Downloads/output_test.gpx'
# All GPS data between start_timestamp and end_timestamp will be included in the final GPX file
# THESE TIMESTAMPS NEED TO BE IN YOUR LOCAL TIMEZONE
start_timestamp = 1489767300
end_timestamp = 1489970266
# THIS IS IMPORTANT. If you mess this up, you're not going to get what you want. This is the difference (offset)
# between UTC time and your local timezone. If you're on GMT for instance, it varies between UTC and UTC+1 depending on
# daylight saving. Type 'utc time' in Google to see what the current UTC time is, and figure out the difference between
# your timezone and UTC timezone. If you're behind UTC by 7 hours for instance, enter -7
timezone_hours_offset_to_utc = -7
######## User-modifiable parts of the script end here #############

from json import load as jload
import datetime

STRAVA_GPX_FILE_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8"?>
<gpx creator="strava.com Android" version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
 <metadata>
  <time>{year}-{month}-{day}T{hour}:{minute}:{second}Z</time>
 </metadata>
 <trk>
  <name>Activity Exported from Google Location History</name>
  <trkseg>
    {trackpoints}
  </trkseg>
 </trk>
</gpx>
"""
# Format of a trackpoint GPX (XML) entry
# Note that we zero the elevation data because apparently Strava wants it to be there
# even though GLoc doesn't have it. It seems that Strava then figures it out from its topographical maps anyway
TRKPT_FMT = '<trkpt lat="{lat}" lon="{long}"><ele>0.0</ele><time>{year}-{month}-{day}T{hour}:{minute}:{second}Z</time></trkpt>'

with open(google_location_history_json_file_path, 'r') as f:
  # Note: if you want to make this script more efficient by loading only
  # the data that matches the timestamp by reading the file as a JSON stream
  # please feel free to send a pull request. I'm lazy and I've got enough RAM
  gloc_data = jload(f)

# Reduce the GLoc data to only the time segment we want to extract
gloc_data = [_ for _ in gloc_data['locations'] if int(_['timestampMs']) >= (start_timestamp * 1000) and int(_['timestampMs']) <= (end_timestamp * 1000)]

if not gloc_data:
  import sys
  print (
    "Sorry, but not location information from your Google Locaiton History was"
    "found between your start_timestamp and your end_timestamp. Check the"
    "timestamps and try again (make sure the timestamps are in your local"
    "timezone and you've set the timezone offset variable correctly."
  )
  sys.exit(-1)

# Extract the GPX-needed information out of the GLoc data
final_data = [
  {
    'time': datetime.datetime.fromtimestamp(int(_['timestampMs']) / 1000 - timezone_hours_offset_to_utc * 3600),
    'lat': float(_['latitudeE7']) / 1e7,
    'long': float(_['longitudeE7']) / 1e7,
  }
  for _ in gloc_data
]

trackpoints = [
  TRKPT_FMT.format(
    year=_['time'].year,
    month='%02d' % _['time'].month,
    day='%02d' % _['time'].day,
    hour='%02d' % _['time'].hour,
    minute='%02d' % _['time'].minute,
    second='%02d'% _['time'].second,
    lat=_['lat'],
    long=_['long'],
  )
  for _ in final_data
]
 
with open(output_gpx_file_path, 'w+') as f:
  f.write(
    STRAVA_GPX_FILE_TEMPLATE.format(
      year=final_data[0]['time'].year,
      month='%02d' % final_data[0]['time'].month,
      day='%02d' % final_data[0]['time'].day,
      hour='%02d' % final_data[0]['time'].hour,
      minute='%02d' % final_data[0]['time'].minute,
      second='%02d' % final_data[0]['time'].second,
      trackpoints="\n".join(reversed(trackpoints)),
    ),
  )

print("File GPX data written to %s" % output_gpx_file_path)

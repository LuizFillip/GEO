import pytz
from datetime import datetime, timedelta

# Get a list of all timezones
timezones = pytz.all_timezones

# Create a dictionary to store timezone meridian longitudes
timezone_meridians = {}

# Define a reference time (can be any date and time)
reference_time = datetime(2023, 1, 1, 0, 0, 0)

# Iterate through each timezone and get its UTC offset
for timezone_name in timezones:
    timezone = pytz.timezone(timezone_name)
    utc_offset = (timezone.utcoffset(reference_time) + timezone.dst(reference_time)).total_seconds() / 3600
    timezone_meridians[timezone_name] = utc_offset

# Print timezone meridian longitudes
for timezone_name, meridian_longitude in timezone_meridians.items():
    print(f"{timezone_name}: {meridian_longitude} hours from UTC")


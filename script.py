import astropy.units as u
from astropy.coordinates import EarthLocation, solar_system_ephemeris
from astropy.time import Time
from sunpy.coordinates import sun
import numpy as np
import pandas as pd

# Define the geodetic coordinates
latitude = 29.6 * u.deg
longitude = -98.5 * u.deg  # Note that the longitude should come first

# Create the EarthLocation object
location = EarthLocation.from_geodetic(longitude, latitude)
max2023 = Time('2023-10-14 16:54')
max2024 = Time('2024-04-08 18:35')

time = max2024

# Define an array of observation times centered around the time of interest
times = time + np.concatenate([np.arange(-120, -5) * u.min,
                                np.arange(-300, 300) * u.s,
                                np.arange(5, 121) * u.min])

# Create an observer coordinate for the time array
observer = location.get_itrs(times)

# Calculate the eclipse amounts using a JPL ephemeris
with solar_system_ephemeris.set('de440s'):
    amount = sun.eclipse_amount(observer)
    amount_minimum = sun.eclipse_amount(observer, moon_radius='minimum')

# Calculate the start/end points of partial/total solar eclipse
partial = np.flatnonzero(amount > 0)
if len(partial) > 0:
    print("Eclipse detected:")
    start_partial, end_partial = times[partial[[0, -1]]]
    print(f"  Partial solar eclipse starts at {start_partial} UTC")

    total = np.flatnonzero(amount_minimum == 1)
    if len(total) > 0:
        start_total, end_total = times[total[[0, -1]]]
        print(f"  Total solar eclipse starts at {start_total} UTC\n"
                f"  Total solar eclipse ends at {end_total} UTC")
    print(f"  Partial solar eclipse ends at {end_partial} UTC")

df = pd.DataFrame({'time': times.to_datetime(), 'amount': amount, 'amount_minimum': amount_minimum})

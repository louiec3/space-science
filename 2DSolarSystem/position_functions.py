import spiceypy as sp
import datetime as dt
import numpy as np
import spiceypy as sp
import pandas as pd

import os 
from os.path import dirname

path_script = dirname(os.path.abspath(__file__)) + '\\'

try:
    sp.furnsh(path_script + 'kernel_meta.txt')
except:
    sp.furnsh(path_script + 'kernel_meta_py.txt')


def utc_to_ephemeris(initial_year, days):
    initial_time_utc = dt.datetime(year=initial_year, month=1, day=1, hour=0, second=0)
    final_time_utc = initial_time_utc + dt.timedelta(days=days)

    initial_time_utc_str = initial_time_utc.strftime('%Y-%m-%dT%H:%M:%S')
    final_time_utc_str = final_time_utc.strftime('%Y-%m-%dT%H:%M:%S')

    initial_time_et = sp.utc2et(initial_time_utc_str)
    final_time_et = sp.utc2et(final_time_utc_str)

    return initial_time_et, final_time_et


def obtain_orbit_data(initial_time, final_time, days, obj_id):
    time_interval_et = np.linspace(start=initial_time, stop=final_time, num=days)

    obj_wrt_sun_position = []
    for time_interval in time_interval_et:
        # _ is a convention to mark a temporary variable
        _position, _ = sp.spkgps(targ=0, et=time_interval, ref='ECLIPJ2000', obs=obj_id)
        # earth_wrt_sun_position.append(_position) 
        obj_wrt_sun_position.append(np.concatenate([np.array([time_interval]), _position]))

    obj_wrt_sun_position = np.array(obj_wrt_sun_position[1:])
    
    df_obj_wrt_sun_position = pd.DataFrame(obj_wrt_sun_position, columns =['Time', 'X', 'Y', 'Z'])

    return df_obj_wrt_sun_position
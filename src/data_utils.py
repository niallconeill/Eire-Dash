import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()

HOME_DIR = os.getenv('HOME_DIR')

def load_raw_data() -> pd.DataFrame:
    """
    Loads the data csv into a Pandas Dataframe
    """
    return pd.read_csv(HOME_DIR + '/data/hrly_Irish_weather.csv', low_memory=False)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to clean raw csv data 
    """
    df = df.copy()
    df = (df.assign(date=lambda d: d['date'].astype('datetime64[ns]'),
            county=lambda d: d['county'].astype('string'),
            station=lambda d: d['station'].astype('string')
                      .replace('SherkinIsland', 'Sherkin Island')
                      .str.title(),
                      latitude=lambda d: d['latitude'].astype('float32'),
                      longitude=lambda d: d['longitude'].astype('float32'))
            .set_index(['date', 'station', 'county', 'latitude', 'longitude'])
            .replace(' ', np.nan)
            .assign(rain=lambda d: d['rain'].astype('float32'),
                    temp=lambda d: d['temp'].astype('float32'),
                    wetb=lambda d: d['wetb'].astype('float32'),
                    dewpt=lambda d: d['dewpt'].astype('float32'),
                    vappr=lambda d: d['vappr'].astype('float32'),
                    rhum=lambda d: d['rhum'].astype('float32'),
                    msl=lambda d: d['msl'].astype('float32'),
                    wdsp=lambda d: d['wdsp'].astype('float32'),
                    wddir=lambda d: d['wddir'].astype('float32')
                    )
            .drop(['sun', 'vis', 'clht', 'clamt'], axis=1)
            .interpolate()
            .reset_index(level=['station', 'county', 'latitude', 'longitude'])
            .assign(date=lambda d:d.index.day,
                    month=lambda d: d.index.month_name(locale='en_us'),
                    year=lambda d: d.index.year,
                    year_month=lambda d: d.index.strftime('%Y-%m')
                   ))
    return df


def get_data() -> pd.DataFrame:
    """
    Function to retrieve preprocessed Dataframe
    """
    df = load_raw_data()
    return clean_data(df)
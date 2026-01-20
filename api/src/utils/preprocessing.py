from . import helpers as utils
import pandas as pd

def preprocess(df):
    df.dropna(inplace=True)

    df['Journey_Day'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True, errors='coerce').dt.day
    df['Journey_Month'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True, errors='coerce').dt.month
    df.drop('Date_of_Journey', axis=1, inplace=True)

    df['Dep_Hour'] = pd.to_datetime(df['Dep_Time'], format='%H:%M').dt.hour
    df['Dep_Minute'] = pd.to_datetime(df['Dep_Time'], format='%H:%M').dt.minute
    df.drop('Dep_Time', axis=1, inplace=True)

    arrival_dt = df['Arrival_Time'].apply(utils.parse_arrival_time)
    df['Arrival_Hour'] = arrival_dt.dt.hour
    df['Arrival_Minute'] = arrival_dt.dt.minute
    df.drop('Arrival_Time', axis=1, inplace=True)

    df['Duration'] = df['Duration'].apply(utils.convert_duration)

    stop_map = {
        'non-stop': 0,
        '1 stop': 1,
        '2 stops': 2,
        '3 stops': 3,
        '4 stops': 4
    }

    df['Total_Stops'] = df['Total_Stops'].map(stop_map)

    df['no_meal'] = df['Additional_Info'].apply(lambda x: 1 if x == 'In-flight meal not included' else 0)
    df['no_baggage'] = df['Additional_Info'].apply(lambda x: 1 if x == 'No check-in baggage included' else 0)
    df['info_missing'] = df['Additional_Info'].apply(lambda x: 1 if x == 'No info' else 0)

    df.drop(['Route', 'Additional_Info'], axis=1, inplace=True)

    df = pd.get_dummies(df, drop_first=True)

    int_cols = df.select_dtypes(include=['int64']).columns
    df[int_cols] = df[int_cols].astype('float64')

    return df

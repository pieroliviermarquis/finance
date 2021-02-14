import pandas as pd
import requests


def get_fred_data(series):
  
  df_all = pd.DataFrame()
  for name, serie in series.items():
    r = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=' + str(serie) + '&api_key=465e1b96e52576cf38130016ce9994d2&file_type=json').json()
    df = pd.DataFrame.from_dict(r['observations'])
    df = df[['date', 'value']]
    df.set_index('date', inplace=True)
    df.index = pd.to_datetime(df.index)
    df.rename(columns={'value': name}, inplace=True)
    df_all = pd.concat([df_all, df], axis=1)
  return df_all


def clean_fred_data(df):

  df.ffill(inplace=True)
  cols = df.columns
  df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
  df.dropna(inplace=True)
  return df


def get_sm_data():
  
  r = requests.get('https://squeezemetrics.com/monitor/static/DIX.csv')
  df = pd.read_csv(io.BytesIO(r.content), encoding='utf-8')  
  df.set_index(['date'], inplace=True)
  df = df.apply(pd.to_numeric, errors='coerce')
  df.index = pd.to_datetime(df.index)
  df.drop(['price'], axis=1, inplace=True)
  return df

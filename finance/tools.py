import pandas as pd

def get_fred_data(series):

  df_all = pd.DataFrame()

  for name, serie in series.items():
    r = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=' + str(serie) + '&api_key=465e1b96e52576cf38130016ce9994d2&file_type=json').json()
    df = pd.DataFrame.from_dict(r['observations'])
    df = df[['date', 'value']]
    df.set_index('date', inplace=True)
    df.rename(columns={'value': name}, inplace=True)
    df.index = pd.to_datetime(df.index)
    df_all = pd.concat([df_all, df], axis=1)

  return df_all

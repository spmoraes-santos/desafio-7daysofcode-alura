#### Created by S.P. Moraes-Santos

import pandas as pd

def prepare_dataframe(df, datetime_column):
    """
    Prepare and clean a dataframe.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        datetime_column (str): Name of the column to be parsed as datetime.

    Returns:
        pd.DataFrame: Cleaned DataFrame with datetime properly parsed,
                      sorted by datetime, and without duplicates.
    """
    df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')
    df = df.sort_values(by=datetime_column)
    df = df.drop_duplicates()
    return df
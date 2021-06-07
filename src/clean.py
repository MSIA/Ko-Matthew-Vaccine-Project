import logging

import pandas as pd

logger = logging.getLogger(__name__)


def clean(local_path, columns, response, threshold, null_vals, other, save_path):
    '''Takes raw data and cleans it for model use
    Args:
        local_path (str): path to raw data file
        columns (:obj:`list` of :obj:`str`): subset of columns needed for
        response (str): column that represents intention of getting vaccine
        threshold (int): cutoff separating people who do not want vaccine in response
        null_vals (:obj:`list` of :obj:`int`): values representing no answer
        other (int): value to replace null answers

    Returns:
        dfm (pandas.core.frame.DataFrame): DataFrame holding full clean data
    '''
    df = pd.read_csv(local_path)
    df = filter(df, columns, response, threshold)
    df = replace_na(df, null_vals, other)
    df = df.drop(response, axis=1)
    df.to_csv(save_path, index=False)


def filter(df, columns, response, threshold):
    '''Filters out columns and rows wanted based on response
    '''
    dfm = df[columns]
    dfm = dfm[df[response]>threshold]

    return dfm


def replace_na(df, nulls, other):
    '''
    '''
    for val in null_vals:
        df = df.replace(val, other)
    return df

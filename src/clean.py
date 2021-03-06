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
        None
    '''
    try:
        df = pd.read_csv(local_path)
    except FileNotFoundError:
        logger.error("File %s not found", local_path)
        logger.debug("Check path in the configuration file")
    except Exception as e:
        logger.error("General error reading file: ", e)
    df = filter(df, columns, response, threshold)
    df = replace_na(df, null_vals, other)
    df = df.drop(response, axis=1)  # only needed people who were not getting vaccine
    df.to_csv(save_path, index=False)


def filter(df, columns, response, threshold):
    '''Filters out columns and rows wanted based on response

    Args:
        df (pandas.core.frame.DataFrame): DataFrame to filter
        columns (:obj:`list` of :obj:`str`): subset of columns needed for
        response (str): column that represents intention of getting vaccine
        threshold (int): cutoff separating people who do not want vaccine in response

    Returns
        dfm (pandas.core.frame.DataFrame): DataFrame holding filtered data
    '''
    dfm = df[columns]
    dfm = dfm[df[response] > threshold]  # response variable is integer
    return dfm


def replace_na(df, nulls, other):
    '''Replace coded na values with a code for other

    Args:
        df (pandas.core.frame.DataFrame): DataFrame with coded null values
        nulls (:obj:`list` of :obj:`int`): values representing no answer
        other (int): value to replace null answers

    Returns
        df (pandas.core.frame.DataFrame): DataFrame holding replaced values
    '''
    for val in nulls:
        df = df.replace(val, other)  # na are coded as special integers
    return df

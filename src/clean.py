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
    dfm = df[columns]
    dfm = dfm[df[response]>threshold]
    
    for val in null_vals:
        dfm = dfm.replace(val, other)

    dfm = dfm.drop(response, axis=1)
    dfm.to_csv(save_path, index=False)

    return dfm

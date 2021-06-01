import logging

import pandas as pd

logger = logging.getLogger(__name__)


def clean(local_path, columns, response, threshold, null_vals, other, db_col):
    '''
    '''
    df = pd.read_csv(local_path)
    dfm = df[columns]
    dfm = dfm[df[response]>threshold]

    for val in null_vals:
        dfm = dfm.replace(val, other)

    dfm = dfm[db_col]

    return dfm

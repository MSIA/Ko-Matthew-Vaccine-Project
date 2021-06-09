import pandas as pd
import pytest
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from src import train


def test_transform_happy():
    df_in_values = [[2, 1, 5, 1, 4, 3, 1977, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
                    [1, 1, 6, 3, 2, 4, 1969, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                    [2, 3, 7, 1, 2, 1, 1974, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0],
                    [1, 1, 7, 5, 2, 3, 1999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [2, 1, 5, 2, 0, 4, 1945, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0]]
    df_in_index = [68269, 52003, 62456, 63813, 14106]
    df_in_columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION', 'TBIRTH_YEAR',
                     'WHYNOT1', 'WHYNOT2', 'WHYNOT3', 'WHYNOT4', 'WHYNOT5', 'WHYNOT6',
                     'WHYNOT7', 'WHYNOT8', 'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    enc = OneHotEncoder().fit(df_in[df_in_columns[:6]])

    cat_inputs = [2,1,5,1,2,4]
    year = 1998
    out_true = enc.transform([cat_inputs]).toarray()
    out_true = np.append(out_true[0],year)
    out_true = [out_true]
    out_test = train.transform(enc, cat_inputs, year)

    assert np.array_equal(out_test, out_true)


def test_transform_sad():
    df_in_values = [[2, 1, 5, 1, 4, 3, 1977, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
                    [1, 1, 6, 3, 2, 4, 1969, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                    [2, 3, 7, 1, 2, 1, 1974, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0],
                    [1, 1, 7, 5, 2, 3, 1999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [2, 1, 5, 2, 0, 4, 1945, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0]]
    df_in_index = [68269, 52003, 62456, 63813, 14106]
    df_in_columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION', 'TBIRTH_YEAR',
                     'WHYNOT1', 'WHYNOT2', 'WHYNOT3', 'WHYNOT4', 'WHYNOT5', 'WHYNOT6',
                     'WHYNOT7', 'WHYNOT8', 'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    enc = OneHotEncoder().fit(df_in[df_in_columns[:6]])

    cat_inputs = [1,5,1,2,4]
    year = 1998

    # Test if the wrong number of inputs are given
    with pytest.raises(ValueError):
        out_test = train.transform(enc, cat_inputs, year)

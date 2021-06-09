import pandas as pd
import numpy as np
import pytest
from src import clean


def test_filter_happy():
    df_in_values = [['V278140006S99460324210012', 27, 4, 38060.0, 4,
                    182.72097240000002, 182.66064644, 1946, 2, 2, 2, 1, 2, 1, 2, 7,
                    2, 3, 1, 2, 0, 2, 1, 1, 1, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, 2, 2, 2,
                    2, -88, 7, -99, 2, -88, 1, 2, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, 2, -99, -99, -99, -99, -99, -99, -99,
                    -99, -99, -99, -99, 1, -99, 1, -99, -99, -99, -99, -99, -99, -99,
                    -99, -99, -99, -99, 1, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, 1, -99, -99, -99, -99, -99, -99, -99, 2,
                    3, 1, 1, -88, -88, -88, -88, -88, -88, 2, -88, -88, -88, -88,
                    -88, -88, -88, 2, 35, 18, 1, 1, 1, 1, 1, -99, -99, -99, -99, -99,
                    -99, -99, 1, 3, 2, 2, 2, 2, 2, 1, 3, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88.0, -88, 0, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, 4],
                   ['V277230001S90311420210022', 27, 31, np.nan, 3, 462.47664759,
                    426.27473555, 1970, 2, 2, 2, 1, 2, 1, 2, 5, 2, 5, 1, 2, 0, 2, 1,
                    2, -88, 4, -99, -99, -99, -99, -99, -99, -99, -99, 1, -99, -99,
                    -88, -88, -88, -88, -88, -88, 2, 2, 2, 1, 1, -88, 2, 2, -88, 2,
                    2, -88, -88, -88, -88, -88, 4, -88, -88, -88, -88, -88, 1, 4,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    1, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 1, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, 1,
                    -99, -99, -99, -99, -99, -99, -99, 2, 3, 1, 1, -88, -88, -88,
                    -88, -88, -88, 2, -88, -88, -88, -88, -88, -88, -88, 2, 200, 20,
                    1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 3,
                    -88, 1, 4, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88.0, -88, 0, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, 4],
                   ['V270620004S54240247800022', 27, 24, np.nan, 2, 599.60804219,
                    1149.4202337000002, 1964, 2, 2, 2, 1, 2, 1, 2, 7, 2, 1, 2, 2, 0,
                    2, 2, 1, 1, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, 2, 2, 2, 1, 1, -88, 1, 2,
                    -88, 2, 2, -88, -88, -88, -88, -88, 4, -88, -88, -88, -88, -88,
                    1, 2, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 1,
                    -99, 2, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 1,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    1, -99, -99, -99, -99, -99, -99, -99, 1, 3, 1, 1, -88, -88, -88,
                    -88, -88, -88, 2, -88, -88, -88, -88, -88, -88, -88, 2, 200, 150,
                    2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88.0, -88, 0, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, 6],
                   ['V278110006S91160636800022', 27, 16, np.nan, 4, 222.65914016,
                    437.37755293, 1971, 2, 2, 2, 1, 2, 1, 2, 4, 2, 1, 2, 2, 0, 2, 2,
                    2, -88, 2, 1, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99,
                    -88, -88, -88, -88, -88, -88, 2, 1, 2, 2, -88, 8, 2, 2, -88, 1,
                    2, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, 4,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    4, -99, -99, 1, 1, -99, 1, -99, -99, 1, -99, -99, -99, -99, -99,
                    1, -99, 1, -99, 1, -99, -99, -99, 1, -99, -99, 1, -99, 1, -99,
                    -99, -99, -99, -99, 1, 2, 1, 2, -88, 1, -99, -99, -99, -99, 2,
                    -88, -88, -88, -88, -88, -88, -88, 2, 70, 20, 3, 2, 4, 3, 2, 2,
                    2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 1, 2, 3, 6, 2, -88, 1, 3, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88.0, -88, 1, -99, 1, -99, -99, -99, -99,
                    -99, 1, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 1,
                    -99, -99, 1],
                   ['V277250005S33551858510022', 27, 55, np.nan, 3, 1174.2225149,
                    2182.2187323000003, 1965, 2, 1, 2, 1, 2, 1, 2, 7, 2, 1, 3, 2, 1,
                    2, 2, 1, 1, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, 2, 1, 1, 1, -99, -88, 1,
                    2, -88, 2, 2, -88, -88, -88, -88, -88, 4, -88, -88, -88, -88,
                    -88, 1, 4, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, 1, 1, 1, -99, -99, -99, 1, -99, -99, -99, -99, -99,
                    -99, -99, -99, 1, -99, -99, -99, 1, -99, 1, -99, 1, -99, -99, 1,
                    -99, -99, -99, -99, -99, -99, -99, 1, 3, 1, 1, -88, -88, -88,
                    -88, -88, -88, 2, -88, -88, -88, -88, -88, -88, -88, 2, 200, 40,
                    2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2,
                    -88, 1, 4, -88, -88, 1, -99, -99, -99, -99, -99, -99, 1, 1, -99,
                    1, -99, 1, -99, 1, -99, 4, 3.0, 3, -99, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, 6]]
    df_in_index = [63320, 56234, 5630, 62858, 56610]
    df_in_columns = ['SCRAM', 'WEEK', 'EST_ST', 'EST_MSA', 'REGION', 'HWEIGHT',
                     'PWEIGHT', 'TBIRTH_YEAR', 'ABIRTH_YEAR', 'EGENDER', 'AGENDER',
                     'RHISPANIC', 'AHISPANIC', 'RRACE', 'ARACE', 'EEDUC',
                     'AEDUC', 'MS', 'THHLD_NUMPER', 'AHHLD_NUMPER', 'THHLD_NUMKID',
                     'AHHLD_NUMKID', 'THHLD_NUMADLT', 'RECVDVACC', 'DOSES',
                     'GETVACC', 'WHYNOT1',  'WHYNOT2', 'WHYNOT3', 'WHYNOT4',
                     'WHYNOT5', 'WHYNOT6',  'WHYNOT7', 'WHYNOT8', 'WHYNOT9',
                     'WHYNOT10',  'WHYNOT11', 'WHYNOTB1', 'WHYNOTB2',
                     'WHYNOTB3', 'WHYNOTB4', 'WHYNOTB5', 'WHYNOTB6', 'HADCOVID',
                     'WRKLOSS', 'EXPCTLOSS', 'ANYWORK', 'KINDWORK', 'RSNNOWRK',
                     'TW_START', 'UI_APPLY', 'UI_RECV', 'SSA_RECV', 'SSA_APPLY',
                     'SSAPGM1', 'SSAPGM2', 'SSAPGM3', 'SSAPGM4', 'SSAPGM5',
                     'SSALIKELY', 'SSAEXPCT1', 'SSAEXPCT2', 'SSAEXPCT3',
                     'SSAEXPCT4', 'SSAEXPCT5', 'SSADECISN', 'EIP', 'EIPSPND1',
                     'EIPSPND2', 'EIPSPND3', 'EIPSPND4', 'EIPSPND5', 'EIPSPND6',
                     'EIPSPND7', 'EIPSPND8', 'EIPSPND9', 'EIPSPND10', 'EIPSPND11',
                     'EIPSPND12', 'EIPSPND13', 'EXPNS_DIF', 'CHNGHOW1',
                     'CHNGHOW2', 'CHNGHOW3', 'CHNGHOW4', 'CHNGHOW5', 'CHNGHOW6',
                     'CHNGHOW7', 'CHNGHOW8', 'CHNGHOW9', 'CHNGHOW10', 'CHNGHOW11',
                     'CHNGHOW12', 'WHYCHNGD1', 'WHYCHNGD2', 'WHYCHNGD3',
                     'WHYCHNGD4', 'WHYCHNGD5', 'WHYCHNGD6', 'WHYCHNGD7',
                     'WHYCHNGD8', 'WHYCHNGD9', 'WHYCHNGD10', 'WHYCHNGD11',
                     'WHYCHNGD12', 'WHYCHNGD13', 'SPNDSRC1', 'SPNDSRC2',
                     'SPNDSRC3', 'SPNDSRC4', 'SPNDSRC5', 'SPNDSRC6', 'SPNDSRC7',
                     'SPNDSRC8', 'FEWRTRIPS', 'FEWRTRANS', 'PLNDTRIPS',
                     'CURFOODSUF', 'CHILDFOOD', 'FOODSUFRSN1', 'FOODSUFRSN2',
                     'FOODSUFRSN3', 'FOODSUFRSN4', 'FOODSUFRSN5', 'FREEFOOD',
                     'WHEREFREE1', 'WHEREFREE2', 'WHEREFREE3', 'WHEREFREE4',
                     'WHEREFREE5', 'WHEREFREE6', 'WHEREFREE7', 'SNAP_YN', 'TSPNDFOOD',
                     'TSPNDPRPD', 'ANXIOUS', 'WORRY', 'INTEREST', 'DOWN',
                     'HLTHINS1', 'HLTHINS2', 'HLTHINS3', 'HLTHINS4', 'HLTHINS5',
                     'HLTHINS6', 'HLTHINS7', 'HLTHINS8', 'PRIVHLTH', 'PUBHLTH',
                     'DELAY', 'NOTGET', 'PRESCRIPT', 'MH_SVCS', 'MH_NOTGET',
                     'TENURE', 'LIVQTR', 'RENTCUR', 'MORTCUR', 'MORTCONF',
                     'EVICT', 'FORCLOSE', 'ENROLL1', 'ENROLL2', 'ENROLL3',
                     'TEACH1', 'TEACH2', 'TEACH3', 'TEACH4', 'TEACH5',
                     'COMPAVAIL', 'COMP1', 'COMP2', 'COMP3', 'INTRNTAVAIL',
                     'INTRNT1', 'INTRNT2', 'INTRNT3', 'SCHLHRS', 'TSTDY_HRS',
                     'TCH_HRS', 'TNUM_PS', 'PSPLANS1', 'PSPLANS2', 'PSPLANS3',
                     'PSPLANS4', 'PSPLANS5', 'PSPLANS6', 'PSCHNG1', 'PSCHNG2',
                     'PSCHNG3', 'PSCHNG4', 'PSCHNG5', 'PSCHNG6', 'PSCHNG7',
                     'PSWHYCHG1', 'PSWHYCHG2', 'PSWHYCHG3', 'PSWHYCHG4',
                     'PSWHYCHG5', 'PSWHYCHG6', 'PSWHYCHG7', 'PSWHYCHG8',
                     'PSWHYCHG9', 'INCOME']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    df_true_values = [[   2,    1,    5,    5,    1,    3, 1970,    4,  -99,  -99,
                    -99, -99,  -99,  -99,  -99,  -99,    1,  -99,  -99]]
    df_true_index = [56234]
    df_true_columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION',
                       'TBIRTH_YEAR','GETVACC', 'WHYNOT1', 'WHYNOT2', 'WHYNOT3',
                       'WHYNOT4', 'WHYNOT5','WHYNOT6', 'WHYNOT7', 'WHYNOT8',
                       'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    df_true = pd.DataFrame(df_true_values, index=df_true_index, columns=df_true_columns)

    columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION', 'TBIRTH_YEAR',
               'GETVACC', 'WHYNOT1', 'WHYNOT2', 'WHYNOT3', 'WHYNOT4', 'WHYNOT5',
               'WHYNOT6', 'WHYNOT7', 'WHYNOT8', 'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    response = 'GETVACC'
    threshold = 2

    df_test = clean.filter(df_in, columns, response, threshold)

    assert df_test.equals(df_true)


def test_filter_sad():
    df_in_values = [['V278140006S99460324210012', 27, 4, 38060.0, 4,
                    182.72097240000002, 182.66064644, 1946, 2, 2, 2, 1, 2, 1, 2, 7,
                    2, 3, 1, 2, 0, 2, 1, 1, 1, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, 2, 2, 2,
                    2, -88, 7, -99, 2, -88, 1, 2, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, 2, -99, -99, -99, -99, -99, -99, -99,
                    -99, -99, -99, -99, 1, -99, 1, -99, -99, -99, -99, -99, -99, -99,
                    -99, -99, -99, -99, 1, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, 1, -99, -99, -99, -99, -99, -99, -99, 2,
                    3, 1, 1, -88, -88, -88, -88, -88, -88, 2, -88, -88, -88, -88,
                    -88, -88, -88, 2, 35, 18, 1, 1, 1, 1, 1, -99, -99, -99, -99, -99,
                    -99, -99, 1, 3, 2, 2, 2, 2, 2, 1, 3, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88.0, -88, 0, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, 4],
                   ['V277230001S90311420210022', 27, 31, np.nan, 3, 462.47664759,
                    426.27473555, 1970, 2, 2, 2, 1, 2, 1, 2, 5, 2, 5, 1, 2, 0, 2, 1,
                    2, -88, 4, -99, -99, -99, -99, -99, -99, -99, -99, 1, -99, -99,
                    -88, -88, -88, -88, -88, -88, 2, 2, 2, 1, 1, -88, 2, 2, -88, 2,
                    2, -88, -88, -88, -88, -88, 4, -88, -88, -88, -88, -88, 1, 4,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    1, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 1, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, 1,
                    -99, -99, -99, -99, -99, -99, -99, 2, 3, 1, 1, -88, -88, -88,
                    -88, -88, -88, 2, -88, -88, -88, -88, -88, -88, -88, 2, 200, 20,
                    1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 3,
                    -88, 1, 4, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88.0, -88, 0, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, 4],
                   ['V270620004S54240247800022', 27, 24, np.nan, 2, 599.60804219,
                    1149.4202337000002, 1964, 2, 2, 2, 1, 2, 1, 2, 7, 2, 1, 2, 2, 0,
                    2, 2, 1, 1, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, 2, 2, 2, 1, 1, -88, 1, 2,
                    -88, 2, 2, -88, -88, -88, -88, -88, 4, -88, -88, -88, -88, -88,
                    1, 2, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 1,
                    -99, 2, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 1,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    1, -99, -99, -99, -99, -99, -99, -99, 1, 3, 1, 1, -88, -88, -88,
                    -88, -88, -88, 2, -88, -88, -88, -88, -88, -88, -88, 2, 200, 150,
                    2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88.0, -88, 0, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, 6],
                   ['V278110006S91160636800022', 27, 16, np.nan, 4, 222.65914016,
                    437.37755293, 1971, 2, 2, 2, 1, 2, 1, 2, 4, 2, 1, 2, 2, 0, 2, 2,
                    2, -88, 2, 1, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99,
                    -88, -88, -88, -88, -88, -88, 2, 1, 2, 2, -88, 8, 2, 2, -88, 1,
                    2, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, 4,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    4, -99, -99, 1, 1, -99, 1, -99, -99, 1, -99, -99, -99, -99, -99,
                    1, -99, 1, -99, 1, -99, -99, -99, 1, -99, -99, 1, -99, 1, -99,
                    -99, -99, -99, -99, 1, 2, 1, 2, -88, 1, -99, -99, -99, -99, 2,
                    -88, -88, -88, -88, -88, -88, -88, 2, 70, 20, 3, 2, 4, 3, 2, 2,
                    2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 1, 2, 3, 6, 2, -88, 1, 3, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88.0, -88, 1, -99, 1, -99, -99, -99, -99,
                    -99, 1, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 1,
                    -99, -99, 1],
                   ['V277250005S33551858510022', 27, 55, np.nan, 3, 1174.2225149,
                    2182.2187323000003, 1965, 2, 1, 2, 1, 2, 1, 2, 7, 2, 1, 3, 2, 1,
                    2, 2, 1, 1, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, 2, 1, 1, 1, -99, -88, 1,
                    2, -88, 2, 2, -88, -88, -88, -88, -88, 4, -88, -88, -88, -88,
                    -88, 1, 4, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, 1, 1, 1, -99, -99, -99, 1, -99, -99, -99, -99, -99,
                    -99, -99, -99, 1, -99, -99, -99, 1, -99, 1, -99, 1, -99, -99, 1,
                    -99, -99, -99, -99, -99, -99, -99, 1, 3, 1, 1, -88, -88, -88,
                    -88, -88, -88, 2, -88, -88, -88, -88, -88, -88, -88, 2, 200, 40,
                    2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2,
                    -88, 1, 4, -88, -88, 1, -99, -99, -99, -99, -99, -99, 1, 1, -99,
                    1, -99, 1, -99, 1, -99, 4, 3.0, 3, -99, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88, -88,
                    -88, -88, -88, -88, 6]]
    df_in_index = [63320, 56234, 5630, 62858, 56610]
    df_in_columns = ['SCRAM', 'WEEK', 'EST_ST', 'EST_MSA', 'REGION', 'HWEIGHT',
                     'PWEIGHT', 'TBIRTH_YEAR', 'ABIRTH_YEAR', 'EGENDER', 'AGENDER',
                     'RHISPANIC', 'AHISPANIC', 'RRACE', 'ARACE', 'EEDUC',
                     'AEDUC', 'MS', 'THHLD_NUMPER', 'AHHLD_NUMPER', 'THHLD_NUMKID',
                     'AHHLD_NUMKID', 'THHLD_NUMADLT', 'RECVDVACC', 'DOSES',
                     'GETVACC', 'WHYNOT1',  'WHYNOT2', 'WHYNOT3', 'WHYNOT4',
                     'WHYNOT5', 'WHYNOT6',  'WHYNOT7', 'WHYNOT8', 'WHYNOT9',
                     'WHYNOT10',  'WHYNOT11', 'WHYNOTB1', 'WHYNOTB2',
                     'WHYNOTB3', 'WHYNOTB4', 'WHYNOTB5', 'WHYNOTB6', 'HADCOVID',
                     'WRKLOSS', 'EXPCTLOSS', 'ANYWORK', 'KINDWORK', 'RSNNOWRK',
                     'TW_START', 'UI_APPLY', 'UI_RECV', 'SSA_RECV', 'SSA_APPLY',
                     'SSAPGM1', 'SSAPGM2', 'SSAPGM3', 'SSAPGM4', 'SSAPGM5',
                     'SSALIKELY', 'SSAEXPCT1', 'SSAEXPCT2', 'SSAEXPCT3',
                     'SSAEXPCT4', 'SSAEXPCT5', 'SSADECISN', 'EIP', 'EIPSPND1',
                     'EIPSPND2', 'EIPSPND3', 'EIPSPND4', 'EIPSPND5', 'EIPSPND6',
                     'EIPSPND7', 'EIPSPND8', 'EIPSPND9', 'EIPSPND10', 'EIPSPND11',
                     'EIPSPND12', 'EIPSPND13', 'EXPNS_DIF', 'CHNGHOW1',
                     'CHNGHOW2', 'CHNGHOW3', 'CHNGHOW4', 'CHNGHOW5', 'CHNGHOW6',
                     'CHNGHOW7', 'CHNGHOW8', 'CHNGHOW9', 'CHNGHOW10', 'CHNGHOW11',
                     'CHNGHOW12', 'WHYCHNGD1', 'WHYCHNGD2', 'WHYCHNGD3',
                     'WHYCHNGD4', 'WHYCHNGD5', 'WHYCHNGD6', 'WHYCHNGD7',
                     'WHYCHNGD8', 'WHYCHNGD9', 'WHYCHNGD10', 'WHYCHNGD11',
                     'WHYCHNGD12', 'WHYCHNGD13', 'SPNDSRC1', 'SPNDSRC2',
                     'SPNDSRC3', 'SPNDSRC4', 'SPNDSRC5', 'SPNDSRC6', 'SPNDSRC7',
                     'SPNDSRC8', 'FEWRTRIPS', 'FEWRTRANS', 'PLNDTRIPS',
                     'CURFOODSUF', 'CHILDFOOD', 'FOODSUFRSN1', 'FOODSUFRSN2',
                     'FOODSUFRSN3', 'FOODSUFRSN4', 'FOODSUFRSN5', 'FREEFOOD',
                     'WHEREFREE1', 'WHEREFREE2', 'WHEREFREE3', 'WHEREFREE4',
                     'WHEREFREE5', 'WHEREFREE6', 'WHEREFREE7', 'SNAP_YN', 'TSPNDFOOD',
                     'TSPNDPRPD', 'ANXIOUS', 'WORRY', 'INTEREST', 'DOWN',
                     'HLTHINS1', 'HLTHINS2', 'HLTHINS3', 'HLTHINS4', 'HLTHINS5',
                     'HLTHINS6', 'HLTHINS7', 'HLTHINS8', 'PRIVHLTH', 'PUBHLTH',
                     'DELAY', 'NOTGET', 'PRESCRIPT', 'MH_SVCS', 'MH_NOTGET',
                     'TENURE', 'LIVQTR', 'RENTCUR', 'MORTCUR', 'MORTCONF',
                     'EVICT', 'FORCLOSE', 'ENROLL1', 'ENROLL2', 'ENROLL3',
                     'TEACH1', 'TEACH2', 'TEACH3', 'TEACH4', 'TEACH5',
                     'COMPAVAIL', 'COMP1', 'COMP2', 'COMP3', 'INTRNTAVAIL',
                     'INTRNT1', 'INTRNT2', 'INTRNT3', 'SCHLHRS', 'TSTDY_HRS',
                     'TCH_HRS', 'TNUM_PS', 'PSPLANS1', 'PSPLANS2', 'PSPLANS3',
                     'PSPLANS4', 'PSPLANS5', 'PSPLANS6', 'PSCHNG1', 'PSCHNG2',
                     'PSCHNG3', 'PSCHNG4', 'PSCHNG5', 'PSCHNG6', 'PSCHNG7',
                     'PSWHYCHG1', 'PSWHYCHG2', 'PSWHYCHG3', 'PSWHYCHG4',
                     'PSWHYCHG5', 'PSWHYCHG6', 'PSWHYCHG7', 'PSWHYCHG8',
                     'PSWHYCHG9', 'INCOME']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    df_true_values = [[2, 1, 5, 5, 1, 3, 1970, 4, -99, -99, -99, -99, -99, -99,
                      -99, -99, 1, -99, -99]]
    df_true_index = [56234]
    df_true_columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION',
                       'TBIRTH_YEAR','GETVACC', 'WHYNOT1', 'WHYNOT2', 'WHYNOT3',
                       'WHYNOT4', 'WHYNOT5','WHYNOT6', 'WHYNOT7', 'WHYNOT8',
                       'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    df_true = pd.DataFrame(df_true_values, index=df_true_index, columns=df_true_columns)

    columns = ['EGENDER', 'RRACE', 'EEDUC', 'MARITAL', 'KINDWORK', 'REGION', 'TBIRTH_YEAR',
               'GETVACC', 'WHYNOT1', 'WHYNOT2', 'WHYNOT3', 'WHYNOT4', 'WHYNOT5',
               'WHYNOT6', 'WHYNOT7', 'WHYNOT8', 'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    response = 'GETVACC'
    threshold = 2

    with pytest.raises(KeyError):
        df_test = clean.filter(df_in, columns, response, threshold)


def test_filter_nondf():
    df_in = "Not a DataFrame"
    columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION', 'TBIRTH_YEAR',
               'GETVACC', 'WHYNOT1', 'WHYNOT2', 'WHYNOT3', 'WHYNOT4', 'WHYNOT5',
               'WHYNOT6', 'WHYNOT7', 'WHYNOT8', 'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    response = 'GETVACC'
    threshold = 2

    with pytest.raises(TypeError):
        df_test = clean.filter(df_in, columns, response, threshold)


def test_replace_na_happy():
    df_in_values = [[2, 1, 5, 5, 1, 3, 1970, 4, -99, -99, -99, -99, -99, -99,
                      -99, -99, 1, -99, -99]]
    df_in_index = [56234]
    df_in_columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION',
                       'TBIRTH_YEAR','GETVACC', 'WHYNOT1', 'WHYNOT2', 'WHYNOT3',
                       'WHYNOT4', 'WHYNOT5','WHYNOT6', 'WHYNOT7', 'WHYNOT8',
                       'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    df_true_values = [[2, 1, 5, 5, 1, 3, 1970, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]
    df_true_index = [56234]
    df_true_columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION',
                       'TBIRTH_YEAR','GETVACC', 'WHYNOT1', 'WHYNOT2', 'WHYNOT3',
                       'WHYNOT4', 'WHYNOT5','WHYNOT6', 'WHYNOT7', 'WHYNOT8',
                       'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    df_true = pd.DataFrame(df_true_values, index=df_true_index, columns=df_true_columns)

    nulls = [-88,-99]
    other = 0

    df_test = clean.replace_na(df_in, nulls, other)

    assert df_test.equals(df_true)


def test_replace_na_sad():
    df_in_values = [[2, 1, 5, 5, 1, 3, 1970, 4, -99, -99, -99, -99, -99, -99,
                      -99, -99, 1, -99, -99]]
    df_in_index = [56234]
    df_in_columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION',
                       'TBIRTH_YEAR','GETVACC', 'WHYNOT1', 'WHYNOT2', 'WHYNOT3',
                       'WHYNOT4', 'WHYNOT5','WHYNOT6', 'WHYNOT7', 'WHYNOT8',
                       'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    df_true_values = [[2, 1, 5, 5, 1, 3, 1970, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]
    df_true_index = [56234]
    df_true_columns = ['EGENDER', 'RRACE', 'EEDUC', 'MS', 'KINDWORK', 'REGION',
                       'TBIRTH_YEAR','GETVACC', 'WHYNOT1', 'WHYNOT2', 'WHYNOT3',
                       'WHYNOT4', 'WHYNOT5','WHYNOT6', 'WHYNOT7', 'WHYNOT8',
                       'WHYNOT9', 'WHYNOT10', 'WHYNOT11']
    df_true = pd.DataFrame(df_true_values, index=df_true_index, columns=df_true_columns)

    nulls = [{'dict':'bad'},-99]
    other = [0,0,0]

    with pytest.raises(TypeError):
        df_test = clean.replace_na(df_in, nulls, other)


def test_replace_na_nondf():
    df_in = "Not a DataFrame"
    nulls = [-88,-99]
    other = 0

    with pytest.raises(TypeError):
        df_test = clean.replace_na(df_in, nulls, other)

import logging
import pickle

import pandas as pd
import numpy as np
import yaml
import sklearn.model_selection
from sklearn.preprocessing import OneHotEncoder
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)


def train(local_path, category_cols, response_cols, year_col, results_path,
          model_path, encoder_path, test_size, random_state, max_depth,
          n_estimators):
    '''Orchestration function to train, evaluate & save vaccine sentiment model

    Args:
        local_path (str): path to cleaned data
        category_cols (:obj:`list` of :obj:`str): columns representing categorical features
        response_cols (:obj:`list` of :obj:`str): columns representing response
        year_col (str): column name for birth year
        results_path (str): path to write model evaluation results to
        model_path (str): path to pickled model
        encoder_path (str): path to pickled encoder
        test_size (float): fraction of original data to split into test set
        random_state (int): random state for training model
        max_depth (int): max depth of trees in random forest model
        n_estimators (int): number of trees in random forest model

    Returns:
        None
    '''
    try:
        df = pd.read_csv(local_path)
    except FileNotFoundError:
        logger.error("File %s not found at ", local_path)
        logger.debug("Check path in the configuration file")
    enc = OneHotEncoder().fit(df[category_cols])
    features = enc.transform(df[category_cols])
    year = df[year_col].reset_index(drop=True)
    features = pd.concat([pd.DataFrame(features.toarray()),year], axis=1)
    response = np.array(df[response_cols])
    model = train_evaluate(features, response, results_path, test_size,
                           random_state, max_depth, n_estimators)
    pickle.dump(model, open(model_path, 'wb'))
    logger.info("Model saved to: %s", model_path)
    pickle.dump(enc, open(encoder_path, 'wb'))
    logger.info("OneHotEncoder saved to: %s", encoder_path)


def train_evaluate(features, response, results_path, test_size, random_state,
                   max_depth, n_estimators):
    '''Function to split data, train model, and evaluate model

    Args:
        features (pandas.core.frame.DataFrame): DataFrame holding feature variables
        response (numpy.ndarray): array holding responses for each individual
        results_path (str): path to write model evaluation results to
        test_size (float): fraction of original data to split into test set
        random_state (int): random state for training model
        max_depth (int): max depth of trees in random forest model
        n_estimators (int): number of trees in random forest model

    Returns:
        ovr (sklearn.multiclass.OneVsRestClassifier): multilabel random forest model
    '''
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
                                                        features, response,
                                                        test_size=test_size,
                                                        random_state=random_state)
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                   random_state=random_state)
    logger.debug("Model training")
    ovr = OneVsRestClassifier(model).fit(X_train,y_train)
    ypred_bin_test = ovr.predict(X_test)
    ypred_proba_test = ovr.predict_proba(X_test)
    auc = sklearn.metrics.roc_auc_score(y_test, ypred_proba_test)
    hamming_loss = sklearn.metrics.hamming_loss(y_test, ypred_bin_test)
    creport = sklearn.metrics.classification_report(y_test, ypred_bin_test,
                                                    output_dict=True)
    results = [creport, {"AUC": str(auc), "Hamming Loss": str(hamming_loss)}]
    with open(results_path, 'w') as file:
            outdoc = yaml.dump(results, file)
    logger.info("Model results written to: %s", results_path)

    return ovr


def get_model(model_path, encoder_path):
    '''Opens pickled model and encoder for the data

    Args:
        model_path (str): path to pickled model
        encoder_path (str): path to pickled encoder

    Returns:
        model (sklearn.multiclass.OneVsRestClassifier): multilabel random forest model
        encoder (sklearn.preprocessing._encoders.OneHotEncoder): encoder for categorical variables
    '''
    try:
        with open(model_path, "rb") as input_file:
            model = pickle.load(input_file)
    except FileNotFoundError:
        logger.error("File %s not found at ", model_path)
        logger.debug("Check path in the configuration file")
    except Exception as e:
        logger.error("General error reading file: ", e)
        logger.debug("Check file location for: %s", model_path)
    try:
        with open(encoder_path, "rb") as input_file:
            enc = pickle.load(input_file)
    except FileNotFoundError:
        logger.error("File %s not found at ", encoder_path)
        logger.debug("Check path in the configuration file")
    except Exception as e:
        logger.error("General error reading file: ", e)
        logger.debug("Check file location for: %s", encoder_path)

    return model, enc


def transform(encoder, cat_inputs, year):
    '''Transforms raw input into encoded input for model use

    Args:
        encoder (sklearn.preprocessing._encoders.OneHotEncoder): encoder for categorical variables
        cat_inputs (:obj:`list` of :obj:`str`): categorical inputs of individual
        year (int): birth year for individual

    Returns:
        test_new (2D :obj:`list` of :obj:`int): encoded inputs for model prediction
    '''
    test_new = encoder.transform([cat_inputs]).toarray()
    test_new = np.append(test_new[0],year)
    test_new = [test_new]
    return test_new


def predict_ind(model, encoder, cat_inputs, year):
    '''Predicts the probabilities for a new model
    Args:
        model (sklearn.multiclass.OneVsRestClassifier): multilabel random forest model
        encoder (sklearn.preprocessing._encoders.OneHotEncoder): encoder for categorical variables
        cat_inputs (:obj:`list` of :obj:`str`): categorical inputs of individual
        year (int): birth year for individual

    Returns:
        prediction (numpy.ndarray): array of predicted probabilities
    '''
    test_new = transform(encoder, cat_inputs, year)
    prediction = model.predict_proba(test_new)
    prediction = prediction[0]

    return prediction

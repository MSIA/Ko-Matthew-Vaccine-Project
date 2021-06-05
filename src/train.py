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
          model_path, encoder_path, test_size, random_state):
    '''Orchestration function to train and evaluate vaccine sentiment model

    Args:
        local_path ():
        category_cols ():
        response_col ():
        year_col ():
        results_path ():
        model_path ():
        encoder_path ():
        test_size ():
        random_state ():

    Returns:
        None
    '''
    df = pd.read_csv(local_path)
    enc = OneHotEncoder().fit(df[category_cols])
    features = enc.transform(df[category_cols])
    year = df[year_col].reset_index(drop=True)
    features = pd.concat([pd.DataFrame(features.toarray()),year], axis=1)
    response = np.array(df[response_cols])
    model = train_evaluate(features, response, results_path, test_size, random_state)
    pickle.dump(model, open(model_path, 'wb'))
    logger.info("Model saved to: %s", model_path)
    pickle.dump(enc, open(encoder_path, 'wb'))
    logger.info("OneHotEncoder saved to: %s", encoder_path)


def train_evaluate(features, response, results_path, test_size, random_state):
    '''Function to split data, train model, and evaluate model

    Args:
        features ():
        response ():
        results_path ():
        test_size ():
        random_state ():

    Returns:
        None
    '''
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
                                                        features, response,
                                                        test_size=test_size,
                                                        random_state=random_state)
    model = RandomForestClassifier()
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

    with open(model_path, "rb") as input_file:
        model = pickle.load(input_file)
    with open(encoder_path, "rb") as input_file:
        enc = pickle.load(input_file)

    return model, enc


def predict_ind(model, encoder, cat_inputs, year):

    test_new = encoder.transform([cat_inputs]).toarray()
    test_new = np.append(test_new[0],year)
    prediction = model.predict_proba([test_new])
    prediction = prediction[0]

    return prediction

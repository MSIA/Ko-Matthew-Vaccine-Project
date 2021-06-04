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
          model_path, encoder_path):

    df = pd.read_csv(local_path)
    enc = OneHotEncoder().fit(df[category_cols])
    features = enc.transform(df[category_cols])
    year = df[year_col].reset_index(drop=True)
    features = pd.concat([pd.DataFrame(features.toarray()),year], axis=1)
    response = np.array(df[response_cols])
    model = train_evaluate(features, response, results_path)
    pickle.dump(model, open(model_path, 'wb'))
    logger.info("Model saved to: %s", model_path)
    pickle.dump(model, open(encoder_path, 'wb'))
    logger.info("OneHotEncoder saved to: %s", encoder_path)


def train_evaluate(features, response, results_path):

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
                                                        features, response,
                                                        test_size=0.2,
                                                        random_state=123)
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

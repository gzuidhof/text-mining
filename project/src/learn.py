from __future__ import division
import dataset
import infer_topology
import numpy as np
import scipy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import f1_score, accuracy_score, classification_report, zero_one_loss, hamming_loss
from sklearn.externals import joblib

from tqdm import tqdm

def binary_y(y, val=0):
    return np.array([int(val in sample) for sample in y])

def multilabel_binary_y(y):
    label_list = dataset.load_labels()

    mlb = MultiLabelBinarizer(classes=range(len(label_list)))
    return mlb.fit_transform(y)

def multilabel_classifier(X_train, y_train):

    y_train_mlb = multilabel_binary_y(y_train)

    svc_ovr = Pipeline([('tfidf', TfidfVectorizer()),
                        #('vect', CountVectorizer()),
                        #('ovr-svc',OneVsRestClassifier(SVC(kernel='rbf'),n_jobs=-2)),
                        #('linear-ovr-svc',OneVsRestClassifier(LinearSVC(),n_jobs=3)),
                        ('linear-ovr-regression', OneVsRestClassifier(LogisticRegression(solver='liblinear'), n_jobs=-2))
                        #('mnb-ovr-clf', OneVsRestClassifier(MultinomialNB(), n_jobs=-2))
    ])

    print "Fitting model"
    svc_ovr.fit(X_train, y_train_mlb)
    print "Done, saving model to file"
    joblib.dump(svc_ovr, '../models/ovrmodel_ml.pkl')


def predict(X_test, y_test):
    print "Loading model"
    model = joblib.load('../models/ovrmodel_ml.pkl')

    print "Predicting"
    y_pred_proba = model.predict_proba(X_test)
    y_pred = model.predict(X_test)

    print "Saving predictions to file"
    joblib.dump(y_pred, '../models/pred_ml.pkl')
    joblib.dump(y_pred_proba, '../models/pred_ml_proba.pkl')

def improve_predictions(probability_predictions_file='../models/pred_ml_proba.pkl',
                            out_file='../models/pred_ml_improved.pkl',
                            use_infer_topology=True):


    print "> IMPROVING PREDICTIONS\n--- Forcing at least one label (most likely)"
    print "Loading probability predictions"
    y_pred_proba = joblib.load(probability_predictions_file)

    #Because we use a one-versus-rest classifier, there may be documents without any labels
    #We deal with this by adding the most likely labels

    y_pred_improved = np.zeros(y_pred_proba.shape, dtype=np.int_)
    print "Converting to binary predictions"
    y_pred = np.where(y_pred_proba >= 0.5, 1, 0)

    for i, (prediction, prediction_proba) in enumerate(tqdm(zip(y_pred, y_pred_proba))):
        if sum(prediction) == 0:
            most_likely_label_index = np.argmax(prediction_proba)
            y_pred_improved[i,most_likely_label_index] = 1
        y_pred_improved[i] += prediction

    print np.sum(np.subtract(y_pred_improved,y_pred)), "labels added"

    if use_infer_topology:
        print "> IMPROVING PREDICTIONS\n--- Topology rules"
        print "Loading train set y-values"
        y_train,filenames_train = dataset.load_train_y()

        rules = infer_topology.infer_topology_rules(y_train)
        y_pred_improved = infer_topology.apply_topology_rules(rules, y_pred_improved)

    print "Saving to file"
    joblib.dump(y_pred_improved, out_file)
    print "Done!\n---"

def evaluate_multilabel(y_test, label_list, predictions_file='../models/pred_ml.pkl'):

    y_test_mlb = multilabel_binary_y(y_test)
    y_pred = joblib.load(predictions_file)

    print "F1 score micro:", f1_score(y_test_mlb, y_pred, average='micro', labels=label_list)
    print "F1 score weighted:", f1_score(y_test_mlb, y_pred, average='weighted', labels=label_list)
    print "F1 score samples:", f1_score(y_test_mlb, y_pred, average='samples', labels=label_list)
    print "F1 score:", f1_score(y_test_mlb, y_pred, average=None, labels=label_list)

    print "Accuracy", accuracy_score(y_test_mlb, y_pred)

    print classification_report(y_test_mlb, y_pred, target_names=label_list, digits=5)

    print "Zero-one classification loss", zero_one_loss(y_test_mlb, y_pred)
    print "Hamming loss", hamming_loss(y_test_mlb, y_pred)

    im = y_test_mlb + y_pred*2
    scipy.misc.imsave('predictions.png',im)


if __name__ == '__main__':

    #Load data
    print "Loading labels"
    label_list = dataset.load_labels()

    print "Loading train set"
    X_train,y_train,filenames_train = dataset.load_train()
    print "Size of train set", len(X_train)
    multilabel_classifier(X_train,y_train)

    #Unload train set from memory
    del X_train, y_train, filenames_train

    print "Loading test set"
    X_test,y_test,filenames_test = dataset.load_test()
    print "Size of test set", len(X_test)

    predict(X_test,y_test)
    improve_predictions(use_infer_topology=True)
    #evaluate_multilabel(y_test, label_list, '../models/pred_ml_improved.pkl')
    evaluate_multilabel(y_test, label_list, '../models/pred_ml.pkl')

from __future__ import division
import dataset
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


from sklearn.metrics import f1_score, accuracy_score, classification_report, zero_one_loss
from sklearn.externals import joblib

from tqdm import tqdm

def binary_y(y, val=0):
    return np.array([int(val in sample) for sample in y])

def multilabel_binary_y(y):
    label_list = dataset.load_labels()

    mlb = MultiLabelBinarizer(classes=range(len(label_list)))
    return mlb.fit_transform(y)

def classifier_per_label(X_train,y_train,X_test,y_test):

    for x in range(25):

        y_train_binary = binary_y(y_train,x) #0,1 for current label
        y_test_binary = binary_y(y_test,x) #0,1 for current label
        print "----"
        print ">  LABEL", x, label_list[x], '('+str(1-np.mean(y_test_binary))+')'

        mnb = Pipeline([('vect', CountVectorizer()),
                              ('clf', MultinomialNB()),
        ])
        mnb_tfidf = Pipeline([('tfidf', TfidfVectorizer()),
                              ('clf', MultinomialNB()),
        ])


        sgd = Pipeline([('vect', CountVectorizer()),
                            ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                                alpha=1e-3, n_iter=5, random_state=42)),
        ])

        sgd_tfidf = Pipeline([('tfidf', TfidfVectorizer()),
                            ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                                alpha=1e-3, n_iter=5, random_state=42)),
        ])

        names = ['MultinomNB       ','MultinomNB TF-IDF','SGDSVM           ', 'SGDSVM TF-IDF    ']
        classifiers = [mnb,mnb_tfidf,sgd,sgd_tfidf]

        for clf, name in zip(classifiers, names):
            clf.fit(X_train, y_train_binary)

            print name, "      :", clf.score(X_test, y_test_binary)

def multilabel_classifier(X_train, y_train, X_test, y_test):

    y_train_mlb = multilabel_binary_y(y_train)
    y_test_mlb = multilabel_binary_y(y_test)

    svc_ovr = Pipeline([('tfidf', TfidfVectorizer()),
                        #('vect', CountVectorizer()),
                        #('ovr-svc',OneVsRestClassifier(SVC(kernel='rbf'),n_jobs=-2)),
                        #('linear-ovr-svc',OneVsRestClassifier(LinearSVC(),n_jobs=3)),
                        ('linear-ovr-regression', OneVsRestClassifier(LogisticRegression(solver='liblinear'), n_jobs=-2))
                        #('mnb-ovr-clf', OneVsRestClassifier(MultinomialNB(), n_jobs=-2))
    ])

    print "Fitting model"
    svc_ovr.fit(X_train, y_train_mlb)
    print "Done fitting, now predicting"
    joblib.dump(svc_ovr, '../models/ovrmodel_ml.pkl')


def predict(X_train, y_train, X_test, y_test):
    model = joblib.load('../models/ovrmodel_ml.pkl')
    y_pred_proba = model.predict_proba(X_test)
    y_pred = model.predict(X_test)

    joblib.dump(y_pred, '../models/pred_ml.pkl')
    joblib.dump(y_pred_proba, '../models/pred_ml_proba.pkl')

def improve_predictions(probability_predictions_file='../models/pred_ml_proba.pkl', out_file='../models/pred_ml_improved.pkl'):
    print "---\nForcing at least one label (most likely)"
    print "Loading probability predictions"
    y_pred_proba = joblib.load(probability_predictions_file)

    #Because we use a one-versus-rest classifier, there may be documents without any labels
    #We deal with this by adding the most likely labels

    y_pred_improved = np.zeros(y_pred_proba.shape)
    print "Converting to binary predictions"
    y_pred = np.where(y_pred_proba >= 0.5, 1, 0)

    for i, (prediction, prediction_proba) in enumerate(tqdm(zip(y_pred, y_pred_proba))):
        if sum(prediction) == 0:
            most_likely_label_index = np.argmax(prediction_proba)
            y_pred_improved[i,most_likely_label_index] = 1
        y_pred_improved[i] += prediction

    print np.sum(np.subtract(y_pred_improved,y_pred)), "labels added"

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

    print classification_report(y_test_mlb, y_pred, target_names=label_list)

    print "Zero-one classification loss", zero_one_loss(y_test_mlb, y_pred)

    im = y_test_mlb + y_pred*2
    scipy.misc.imsave('predictions.png',im)


if __name__ == '__main__':

    #Load data
    print "Loading labels"
    label_list = dataset.load_labels()
    print "Loading train set"

    #X_train,y_train,filenames_train = dataset.load_train()
    print "Loading test set"
    X_test,y_test,filenames_test = dataset.load_test()

    #print "Size of train set", len(X_train), ", Test set", len(X_test)

    #classifier_per_label(X_train,y_train,X_test,y_test)
    #multilabel_classifier(X_train,y_train,X_test,y_test)
    #predict(X_train,y_train,X_test,y_test)
    improve_predictions()
    evaluate_multilabel(y_test, label_list, '../models/pred_ml_improved.pkl')

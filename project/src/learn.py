import dataset
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

from sklearn.metrics import f1_score, accuracy_score, classification_report, zero_one_loss
from sklearn.externals import joblib


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
                        ('ovr-svc',OneVsRestClassifier(SVC(kernel='linear'),n_jobs=-2)),
    ])

    print "Fitting model"
    svc_ovr.fit(X_train, y_train_mlb)
    print "Done fitting, now predicting"
    joblib.dump(svc_ovr, '../models/ovrmodel_ml.pkl')
    y_pred = svc_ovr.predict(X_test)

    joblib.dump(y_pred, '../models/pred_ml.pkl')

def evaluate_multilabel(y_test, label_list):

    y_test_mlb = multilabel_binary_y(y_test)
    y_pred = joblib.load('../models/pred_ml.pkl')
    print len(y_pred)
    print len(y_test_mlb)

    print "F1 score micro:", f1_score(y_test_mlb, y_pred, average='micro', labels=label_list)
    print "F1 score weighted:", f1_score(y_test_mlb, y_pred, average='weighted', labels=label_list)
    print "F1 score samples:", f1_score(y_test_mlb, y_pred, average='samples', labels=label_list)
    print "F1 score:", f1_score(y_test_mlb, y_pred, average=None, labels=label_list)

    print "Accuracy", accuracy_score(y_test_mlb, y_pred)

    print classification_report(y_test_mlb, y_pred, target_names=label_list)

    print zero_one_loss(y_test_mlb, y_pred)

if __name__ == '__main__':

    #Load data
    label_list = dataset.load_labels()

    X_train,y_train,filenames_train = dataset.load_train()
    X_test,y_test,filenames_test = dataset.load_test()

    print "Size of train set", len(X_train), ", Test set", len(X_test)

    #classifier_per_label(X_train,y_train,X_test,y_test)
    #multilabel_classifier(X_train,y_train,X_test,y_test)
    evaluate_multilabel(y_test, label_list)

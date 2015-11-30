import dataset
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier



def make_binary_y(y, val=0):
    return np.array([int(val in sample) for sample in y])



if __name__ == '__main__':

    #Load data
    label_list = dataset.load_labels()

    X_train,y_train,filenames_train = dataset.load_train()
    X_test,y_test,filenames_test = dataset.load_test()

    print "Train set", len(X_train), "Test set", len(X_test)

    for x in range(25):

        y_train_binary = make_binary_y(y_train,x) #0,1 for current label
        y_test_binary = make_binary_y(y_test,x) #0,1 for current label
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

        #print "Actual:   ", y_test_binary
        #print "Predicted:", clf.predict(X_test)
        #print "Probabilities:", clf.predict_proba(X_test)
            print name, "      :", clf.score(X_test, y_test_binary)

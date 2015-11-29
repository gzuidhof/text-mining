import dataset
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def make_binary_y(y, val=0):
    return np.array([int(val in sample) for sample in y])


if __name__ == '__main__':
    X_train,y_train,filenames_train = dataset.load_train()
    y_train_binary = make_binary_y(y_train) #True or False, 0,1



    clf = Pipeline([('vect', CountVectorizer()),
                          ('tfidf', TfidfTransformer()),
                          ('clf', MultinomialNB()),
     ])


    clf.fit(X_train, y_train_binary)




    X_test,y_test,filenames_test = dataset.load_test()
    y_test_binary = make_binary_y(y_test) #True or False, 0,1

    print "Actual:   ", y_test_binary
    print "Predicted:", clf.predict(X_test)
    print "Probabilities:", clf.predict_proba(X_test)
    print "Accuracy:", clf.score(X_test, y_test_binary)

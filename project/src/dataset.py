import numpy as np
import pickle
from sklearn.cross_validation import train_test_split

DATA_FOLDER = '..\\data'
PROCESSED_FOLDER = '..\\data\\processed'


def create_dictionary():
    pass

def split_dataset():
    with open(DATA_FOLDER+'\\labels_int.p', 'r') as f:
        y_dict = pickle.load(f)
    with open(DATA_FOLDER+'\\processed.p', 'r') as f:
        x_dict = pickle.load(f)

    #Intersect the X and Y labels, only use those with both
    keys = sorted( set(y_dict.keys()).intersection(x_dict.keys()) )

    X = [x_dict[key] for key in keys]
    y = [(key, y_dict[key]) for key in keys]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    print 'Dataset split into trainset of ', len(X_train), 'and testset of', len(X_test)

    print 'Now writing to file'

    filenames=['x_train.p','x_test.p','y_train.p','y_test.p']
    data = [X_train, X_test, y_train, y_test]

    for filename, dat in zip(filenames, data):
        with open(PROCESSED_FOLDER+'\\'+filename, 'w') as f:
            pickle.dump(dat,f)
            
    print 'Done'

def load_train():
    with open(PROCESSED_FOLDER+'\\x_train.p', 'r') as f:
        X = pickle.load(f)
    with open(PROCESSED_FOLDER+'\\y_train.p', 'r') as f:
        y_tups = pickle.load(f)

    filenames, y = zip(*y_tups)

    return X,y,filenames

def load_test():
    with open(PROCESSED_FOLDER+'\\x_test.p', 'r') as f:
        X = pickle.load(f)
    with open(PROCESSED_FOLDER+'\\y_test.p', 'r') as f:
        y_tups = pickle.load(f)

    filenames, y = zip(*y_tups)

    return X,y,filenames


def load_labels():
    with open(DATA_FOLDER+'\\label_list.p', 'r') as f:
        label_list = pickle.load(f)
    return label_list

if __name__ == '__main__':
    split_dataset()

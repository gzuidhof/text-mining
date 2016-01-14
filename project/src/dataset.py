import numpy as np
import pickle
from sklearn.cross_validation import train_test_split

DATA_FOLDER = '../data/'
PROCESSED_FOLDER = '../data/processed/'

def create_dictionary():
    pass

def split_dataset(force_manual_evaluation_into_test=True):
    with open(DATA_FOLDER+'labels_int.p', 'r') as f:
        y_dict = pickle.load(f)
    with open(DATA_FOLDER+'processed.p', 'r') as f:
        x_dict = pickle.load(f)

    #Intersect the X and Y labels, only use those with both
    keys = sorted( set(y_dict.keys()).intersection(x_dict.keys()) )

    X = [x_dict[key] for key in keys]
    y = [(key, y_dict[key]) for key in keys]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.5)
    print 'Dataset split into trainset of ', len(X_train), 'and testset of', len(X_test)

    if force_manual_evaluation_into_test:
        import manual_classifications
        print "Moving certain docs to the test set (manually classified ones)"
        #Ensure certain documents are in the test set (the manually classified ones)
        n_moved = 0
        for x, y in zip(X_train, y_train):
            key, y_value = y
            if key in manual_classifications.FILES:
                X_train.remove(x)
                y_train.remove(y)
                X_test.append(x)
                y_test.append(y)
                n_moved += 1

        #Move the same amount the other way to keep the same split ratio
        move_to_train = zip(X_test, y_test)[:n_moved]
        X_test = X_test[n_moved:]
        y_test = y_test[n_moved:]

        for x,y in move_to_train:
            X_train.append(x)
            y_train.append(y)

        print n_moved, "moved over"
        print 'Dataset now trainset of ', len(X_train), 'and testset of', len(X_test)



    print 'Now writing to file'
    filenames=['x_train.p','x_test.p','y_train.p','y_test.p']
    data = [X_train, X_test, y_train, y_test]

    for filename, dat in zip(filenames, data):
        with open(PROCESSED_FOLDER+filename, 'w') as f:
            pickle.dump(dat,f)

    print 'Done'

def load_train():
    with open(PROCESSED_FOLDER+'x_train.p', 'r') as f:
        X = pickle.load(f)
    with open(PROCESSED_FOLDER+'y_train.p', 'r') as f:
        y_tups = pickle.load(f)

    filenames, y = zip(*y_tups)

    return X,y,filenames

def load_train_y():
    with open(PROCESSED_FOLDER+'y_train.p', 'r') as f:
        y_tups = pickle.load(f)

    filenames, y = zip(*y_tups)
    return y,filenames

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

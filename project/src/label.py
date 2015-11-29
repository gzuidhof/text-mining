import pickle
from collections import Counter
import itertools

DATA_FOLDER = '..\\data'

#Looks at all labels, orders them by occurence, writes to file
if __name__ == '__main__':
    with open(DATA_FOLDER+'\\labels.p','r') as label_file:
        label_dict = pickle.load(label_file)
        labels = list(itertools.chain.from_iterable(label_dict.values()))
        #print Counter(labels).most_common()
        label_list = zip(*Counter(labels).most_common())[0]

        with open(DATA_FOLDER+'\\label_list.p','w') as f:
            pickle.dump(label_list,f)

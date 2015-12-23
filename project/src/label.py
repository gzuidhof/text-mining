import pickle
from collections import Counter, OrderedDict
import itertools

DATA_FOLDER = '../data/'

#Looks at all labels, orders them by occurence, writes to file
if __name__ == '__main__':
    with open(DATA_FOLDER+'labels.p','r') as label_file:
        label_dict = pickle.load(label_file)

        #Remove double entries
        label_dict = {k:list(set(v)) for k,v in label_dict.iteritems()}
        labels = list(itertools.chain.from_iterable(label_dict.values()))

        for label in Counter(labels).most_common():
		    print label

        label_list = zip(*Counter(labels).most_common())[0]

        with open(DATA_FOLDER+'label_list.p','w') as f:
            pickle.dump(label_list,f)

        label_dict_as_int = {}

        #instead of string labels, save the index of the label in the label list
        label_dict_as_int = {k:[label_list.index(x) for x in v] for k,v in label_dict.iteritems()}
        ordered = OrderedDict(sorted(label_dict_as_int.items()))

        with open(DATA_FOLDER+'\\labels_int.p','w') as f:
            pickle.dump(ordered,f)

        #Determine the frequency of 1, 2, 3 or more labels on individual documents
        label_counts = [len(v) for v in label_dict.values()]
        print Counter(label_counts)

        for v in label_dict.values():
            if len(v)>3:
                print v

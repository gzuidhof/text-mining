from __future__ import division
import pickle
import dataset
import numpy as np

from tqdm import tqdm

DATA_FOLDER = '../data/'


def infer_topology_rules(y_values=None, verbose=False):
    if y_values is None:
        with open(DATA_FOLDER+'labels_int.p', 'r') as f:
            y_dict = pickle.load(f)
            y_values = y_dict.values()

    print "Infering topology from {0} classifications".format(len(y_values))


    label_list = dataset.load_labels()
    n_labels = len(label_list)

    topology_rules = []

    for from_label in range(n_labels):
        n = 0
        counts = np.zeros((31,), dtype=np.int_)

        if verbose:
            print "Now doing ", label_list[from_label]

        for labeling in y_values:
            if not from_label in labeling:
                continue

            n+=1
            for x in labeling:
                counts[x] += 1

        for to_label, count in enumerate(counts):
            if n == 0: #Let's not draw any conclusions from 0 occurences
                continue
            if to_label == from_label: #A label will always occur with itself, ignore
                continue

            if count == n:

                topology_rules.append( (from_label, to_label) )

                if verbose:
                    #print "Label {0} -> {1} ({2})".format(from_label, index, count)
                    print "{0} -> {1} ({2})".format(label_list[from_label], label_list[to_label], count)

    print "Done.",len(topology_rules), "rules inferred."
    return topology_rules

def apply_topology_rules(rules, predictions):
    print "Applying topology rules"
    predictions_improved = np.zeros(predictions.shape, dtype=np.int_)

    for rule in tqdm(rules):
        from_label, to_label = rule

        for i, prediction in enumerate(predictions):
            #If from_label is present, then to_label must be present

            if prediction[from_label] == 1 and prediction[to_label] == 0:
                #print "F",prediction
                predictions_improved[i,to_label] = 1
                #print "T",predictions_improved[i]


    for i, prediction in enumerate(predictions):
        predictions_improved[i] += prediction

    print np.sum(np.subtract(predictions_improved,predictions)), "labels added"
    return predictions_improved

def print_topology(rules):

    label_list = dataset.load_labels()

    root_nodes = set([y for x,y in rules])
    tree = {root:[] for root in root_nodes}

    for rule in rules:
        from_label, to_label = rule
        tree[to_label].append(from_label)

    for parent, children in tree.iteritems():
        print label_list[parent]
        for child in children:
            print "  >", label_list[child]

if __name__ == "__main__":

    with open(DATA_FOLDER+'labels_int.p', 'r') as f:
        y_dict = pickle.load(f)

    rules = infer_topology_rules(y_dict.values(), verbose=False)
    print_topology(rules)

    y, _ = dataset.load_train_y()
    rules = infer_topology_rules(y, verbose=False)
    print_topology(rules)

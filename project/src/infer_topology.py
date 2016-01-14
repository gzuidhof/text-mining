from __future__ import division
import pickle
import dataset
import numpy as np

DATA_FOLDER = '../data/'


def infer_topology_rules(y_values, verbose=False):
    print "Infering topology from {0} labelings".format(len(y_values))
    label_list = dataset.load_labels()
    n_labels = len(label_list)

    topology_rules = []

    for from_label in range(n_labels):
        n = 0
        counts = np.zeros((31,), dtype=np.int_)

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
                #print "Label {0} -> {1} ({2})".format(from_label, index, count)
                topology_rules.append( (from_label, to_label) )

                if verbose:
                    print "{0} -> {1} ({2})".format(label_list[from_label], label_list[to_label], count)

    print "Done.",len(topology_rules), "rules inferred."
    return topology_rules

if __name__ == "__main__":

    with open(DATA_FOLDER+'labels_int.p', 'r') as f:
        y_dict = pickle.load(f)

    infer_topology_rules(y_dict.values())

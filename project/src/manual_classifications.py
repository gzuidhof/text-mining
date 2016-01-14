import pickle
import dataset
import learn
from sklearn.metrics import f1_score, precision_score, recall_score, zero_one_loss, hamming_loss
from sklearn.externals import joblib
import numpy as np
import infer_topology

DATA_FOLDER = '../data/'

FILES = [72102652, 72102581, 88703198, 72120955, 76674874, 89433288, 80114536, 94086649,
87366150, 87366200, 76745162, 114499672, 115989647, 80045894, 88814249,
74177349, 85300096, 94087262, 103763713, 112385287, 74177295, 111392832, 117338702, 105317679]
FILES = map(str, FILES)
label_list = dataset.load_labels()


CLASSIFICATIONS = {
"72102652":["Personen- en familierecht"],
"72102581":["Personen- en familierecht"],
"88703198":["Personen- en familierecht"],
"72120955": ["Civiel recht"], #Burgerlijk recht; verzekeringsrecht
"76674874": ["Civiel recht"], #Huurrecht/Woonrecht
"89433288": ["Strafrecht"], #Strafrecht/Strafvordering
"80114536": ["Strafrecht"],#Strafrecht/Strafvordering
"87366150": ["Bestuursrecht"], #/Staatsrechts
"87366200": ["Burgerlijk procesrecht"], #Burgerlijke rechtsvordering
"76745162": ["Burgerlijk procesrecht"], #Burgerlijke rechtsvordering
"114499672":["Civiel recht"], #Burgerlijk recht
"94086649": ["Bestuursrecht", "Strafrecht"],  #Strafrecht/strafvordering
"115989647":["Bestuursrecht"], #Staats-en Bestuursrecht
"80045894": ["Arbeidsrecht"], #Arbeids/Sociaal recht
"88814249": ["Strafrecht"], #Strafrecht/Strafvordering
"74177349": ["Goederenrecht"], #Goederenrecht
"85300096": ["Insolventierecht"], #Faillisementsrecht
"94087262": ["Insolventierecht", "Civiel recht"], #Faillisementsrecht; Burgerlijk recht
"103763713":["Intellectueel-eigendomsrecht"], #Intellectuele Eigendom
"112385287":["Intellectueel-eigendomsrecht"], #Intellectuele Eigendom
"74177295": ["Intellectueel-eigendomsrecht"], #Intellectuele Eigendom
"111392832":["Arbeidsrecht", "Civiel recht"], #Arbeids/Sociaal Recht; Burgerlijk Recht
"117338702":["Burgerlijk procesrecht"], #Burgerlijke rechtsvordering
"105317679":["Insolventierecht"] #Faillisementsrecht
}


#Convert to label indices instead of text
for f in FILES:
    CLASSIFICATIONS[f] = [label_list.index(x) for x in CLASSIFICATIONS[f]]

def print_manual_classifications():
    with open(DATA_FOLDER+'labels_int.p', 'r') as f:
        y_dict = pickle.load(f)

    for f in FILES:
        if f in y_dict:
            print f, y_dict[f], CLASSIFICATIONS[f]
            #for x in MANUAL_PREDICTIONS[f]:
                #print x
                #print label_list .index(x)
        else:
            print f, "Not in dataset"

def compare_manual_vs_model():

    with open(DATA_FOLDER+'labels_int.p', 'r') as f:
        y_dict = pickle.load(f)

    print "Loading test data"
    X_test,y_test,filenames_test = dataset.load_test()
    y_pred = joblib.load('../models/pred_ml_improved.pkl')

    relevant = []
    for pred, correct, filename in zip(y_pred, y_test, filenames_test):
        if filename in FILES:
            relevant.append((pred,correct,filename, CLASSIFICATIONS[filename]))

    model_predictions, correct, filename, manual_predictions = zip(*relevant)
    manual_predictions = learn.multilabel_binary_y(manual_predictions)
    model_predictions = np.array(model_predictions)
    correct = learn.multilabel_binary_y(correct)

    rules = infer_topology.infer_topology_rules()
    improved_manual = infer_topology.apply_topology_rules(rules, manual_predictions)

    prediction_names = ["MODEL","MANUAL","IMPROVED_MANUAL"]
    predictions = [model_predictions, manual_predictions, improved_manual]

    for name, pred in zip(prediction_names, predictions):

        print "\n{}\n--".format(name)
        print "Zero-one classification loss", zero_one_loss(correct, pred)
        print "Hamming loss", hamming_loss(correct, pred)
        print "F1 score weighted :", f1_score(correct, pred, average='weighted', labels=label_list)
        print "Precision weighted:", precision_score(correct, pred, average='weighted', labels=label_list)
        print "Recall weighted   :", recall_score(correct, pred, average='weighted', labels=label_list)

if __name__ == "__main__":
    #print_manual_classifications()
    compare_manual_vs_model()

import pickle
import dataset

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
"74177349": ["Insolventierecht", "Goederenrecht"], #Faillisementsrecht; Goederenrecht
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
    #for x in MANUAL_PREDICTIONS[f]:
        #print MANUAL_PREDICTIONS[f]
        #print f, "Label", x, " - ", label_list.index(x)

    CLASSIFICATIONS[f] = [label_list.index(x) for x in CLASSIFICATIONS[f]]

del label_list

if __name__ == "__main__":

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

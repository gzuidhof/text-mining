import pandas as pd
import glob
import pickle
from collections import OrderedDict

INPUT_FOLDER = '../data/frogged'
DATA_FOLDER = '../data'

#PoS filter #http://ilk.uvt.nl/menno/files/docs/p_lrec_nlp4ugc12.pdf
FILTER = ['LET','TW','LID','VG', 'VZ','SPEC(symb)']
#LET (Leesteken aka Punctiation)
#TW (Telwoord aka Number/ordinal)
#LID (Lidwoord aka Determiner)
#VG (Voegwoord aka conjunction)
#VZ (Voortzetsel aka Preposition)
#SPEC(symb) (Symbool aka Symbol)

def filter_dataframe(df):
    for filter_term in FILTER:
        df = df[~df['PoS'].str.startswith(filter_term)]
    return df

#Processes a single file
def process(filepath):

    df = pd.read_csv(filepath, sep='\t', index_col=False, header=None, names=['TokenNumber','Token','Lemma','Morph','PoS','PoSConfidence', 'x1', 'x2', 'x3','x4','x5'])
    df = df.drop(['x1','x2','x3','x4','x5'],axis=1)
    df = df.drop(['PoSConfidence','Token','Morph'],axis=1)
    df = filter_dataframe(df)

    as_string = " ".join(list(df['Lemma']))
    lowercased = as_string.lower()
    return lowercased

if __name__ == '__main__':
    files = glob.glob(INPUT_FOLDER+'/*.frog.out')

    lemmatized = {}
    for i, filepath in enumerate(files):
        file_id = filepath.split('\\')[-1].split('.')[0]

        lemmatized[file_id] = process(filepath)
        if i%100 == 0:
            print i,'/',len(files)

    #Order by key
    ordered = OrderedDict(sorted(lemmatized.items()))

    for k,v in ordered.iteritems():
        print k, v[:65]


    with open(DATA_FOLDER+'\\processed.p','w') as f:
        pickle.dump(ordered,f)
    print "Done!"

from __future__ import division
import pandas as pd
import glob
import pickle
import sys
import util
from collections import OrderedDict
from multiprocessing.pool import ThreadPool, Pool

INPUT_FOLDER = '../data/frogged/'
DATA_FOLDER = '../data/'

#PoS filter #http://ilk.uvt.nl/menno/files/docs/p_lrec_nlp4ugc12.pdf
FILTER = tuple(['LET','TW','LID','VG', 'VZ','SPEC(symb)','BW','VNW'])
#LET (Leesteken aka Punctiation)
#TW (Telwoord aka Number/ordinal)
#LID (Lidwoord aka Determiner)
#VG (Voegwoord aka conjunction)
#VZ (Voortzetsel aka Preposition)
#SPEC(symb) (Symbool aka Symbol)

def filter_dataframe(df):
    df = df[~df['PoS'].str.startswith(FILTER)]
    return df

#Processes a single file
def process(filepath):

    df = pd.read_csv(filepath, sep='\t', index_col=False, header=None, names=['TokenNumber','Token','Lemma','Morph','PoS','PoSConfidence', 'x1', 'x2', 'x3','x4','x5'])
    df = df.drop(['x1','x2','x3','x4','x5'],axis=1)
    df = df.drop(['PoSConfidence','Token','Morph'],axis=1)
    df = filter_dataframe(df)

    #Join the lemmas together
    as_string = " ".join( [str(val) for val in list(df['Lemma'])])
    #Lowercase
    lowercased = as_string.lower()
    return lowercased

def filter_and_lemma(chunk_size=2000):
    files = glob.glob(INPUT_FOLDER+'*.frog.out')

    lemmatized = {}

    #Split all files in the list into chunks
    file_chunks = util.chunks(files, chunk_size)

    for i, chunk in enumerate(file_chunks):
        pool = Pool(processes=util.CPU_COUNT)
        filtered_lemmatized = pool.map(process, chunk)
        pool.close()

        for filename, value in zip(chunk, filtered_lemmatized):
            file_id = util.filename_without_extension(filename, '.frog.out')
            lemmatized[file_id] = value

        print i+1, '/', len(file_chunks)

    #Order by key
    ordered = OrderedDict(sorted(lemmatized.items()))

    with open(DATA_FOLDER+'processed.p','w') as f:
        pickle.dump(ordered,f)
    print "Done!"

if __name__ == '__main__':
    filter_and_lemma()

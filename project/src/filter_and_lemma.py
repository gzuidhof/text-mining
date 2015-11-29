import pandas as pd
import glob

INPUT_FOLDER = '../data/frogged'
OUTPUT_FOLDER = '../data/lemma'

#PoS filter #http://ilk.uvt.nl/menno/files/docs/p_lrec_nlp4ugc12.pdf
FILTER = ['LET','TW','LID','VG', 'VZ']
#LET (Leesteken aka Punctiation)
#TW (Telwoord aka Number/ordinal)
#LID (Lidwoord aka Determiner)
#VG (Voegwoord aka conjunction)
#VZ (Voortzetsel aka Preposition)

def filter_dataframe(df):
    for filter_term in FILTER:
        df = df[~df['PoS'].str.startswith(filter_term)]
    return df

if __name__ == '__main__':
    files = glob.glob(INPUT_FOLDER+'/*.frog.out')
    print files

    one = files[1]
    #df = pd.read_csv(one, sep='\t', index_col=False, header=0, names=['TokenNumber','Token','Lemma','Morph','PoS','PoSConfidence'])
    df = pd.read_csv(one, sep='\t', index_col=False, header=None, names=['TokenNumber','Token','Lemma','Morph','PoS','PoSConfidence', 'x1', 'x2', 'x3','x4','x5'])
    df = df.drop(['x1','x2','x3','x4','x5'],axis=1)
    df = df.drop(['PoSConfidence','Token','Morph'],axis=1)
    print len(df)
    df = filter_dataframe(df)
    print len(df), df

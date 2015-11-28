import xmltodict
import glob
import unicodedata
import pickle
import codecs
from collections import Counter, OrderedDict

RAW_DATA_FOLDER = '..\\data\\raw'
PLAINTEXT_FOLDER = '..\\data\\plaintext'
DATA_FOLDER = '..\\data'

#Nonsense files (website sources, PDFs)
BLACKLIST = ['111251559.xml']
for x in range(95484218,95484250):
    BLACKLIST.append(str(x)+'.xml')
BLACKLIST = map(lambda x: RAW_DATA_FOLDER+'\\'+x, BLACKLIST)

#Only used for debugging (for checking whether all relevant text is extracted)
NONSENSE_KEYS = ['@lang','@id','@xml:space','@xmlns','@role','@mark','@xmlns:xsd',
'@xmlns:xsi','@xmlns:xlink', '@linkend','@label','@cols','@colname','@fileref','@align','@scale',
'@width','@height','@format','@numeration','@depth', '@namest','@nameend', '@xmlns:rs',
'superscript','@morerows','@rowsep']

#Recursively retrieves plain text from XML structure
def as_plain_text(node, text_so_far):

    if type(node) not in [list,dict,OrderedDict]:
        #print node
        return

    if type(node) is list:
        for child in node:
            if child is not None and type(child) not in [list,dict,OrderedDict]:
                text_so_far.append(child)
            as_plain_text(child, text_so_far)
        return

    for key, value in node.iteritems():
        if type(value) in [list,dict,OrderedDict]:
            as_plain_text(value, text_so_far) #Expand node
        else:
            if key in ['para','title','#text','nr','bridgehead'] and value is not None:
                text_so_far.append(value)
            elif key not in NONSENSE_KEYS and value is not None:
                print "UNEXPECTED KEY/VALUE", key, value



if __name__ == '__main__':

    filenames = glob.glob(RAW_DATA_FOLDER+'/*.xml')
    filenames = [x for x in filenames if x not in BLACKLIST]

    all_labels = []
    conclusion_labels = []
    verdict_labels = []

    label_dict = {}

    for i, filepath in enumerate(filenames):
        with open(filepath) as fd:

            #Filename without extension
            file_id = filepath.split('\\')[-1][:-4]

            #print i, filename

            obj = xmltodict.parse(fd.read())
            root = obj['open-rechtspraak']
            metadata = root['rdf:RDF']

            if 'uitspraak' in root:
                content = root['uitspraak']
                is_verdict = True
            else:
                content = root['conclusie']
                is_verdict = False

            #############
            # Extract labels
            #############

            description = metadata['rdf:Description']

            if type(description) is list:
                description = description[0]
            law_areas = description['dcterms:subject']

            if type(law_areas) is not list:
                law_areas = [law_areas]

            text_labels = []
            for x in law_areas:
                labels = x['#text'].split('; ')
                all_labels += labels
                text_labels += labels

                if is_verdict:
                    verdict_labels += labels
                else:
                    conclusion_labels += labels

            label_dict[file_id] = text_labels

            #############
            # Extract content as plain text
            #############

            plain_text = []
            as_plain_text(content, plain_text)

            with codecs.open(PLAINTEXT_FOLDER+'\\'+file_id+'.txt', 'w', 'utf-8') as f:
                 for line in plain_text:
                        print>>f, line
                #f.writelines(plain_text) Does not append newlines :<

            #with open(PLAINTEXT_FOLDER+'\\'+file_id+'.txt', 'w') as f:
            #    plain_text_ascii = [unicodedata.normalize('NFKD',line).encode('ascii','ignore')
            #        for line in plain_text]
#
            #    for line in plain_text_ascii:
            #        print>>f, line

        #Print progress
        if i % 100 == 0:
            print i, '/', len(filenames)

    #Write labels to file
    with open(DATA_FOLDER+'\\labels.p','w') as f:
        pickle.dump(label_dict, f)



    print '\n---overall'
    #print set(all_labels)
    print len(set(all_labels))
    print Counter(all_labels)

    print '\n---conclusion'
    #print set(conclusion_labels)
    print len(set(conclusion_labels))
    print Counter(conclusion_labels)

    print '\n---verdict\n'
    #print set(verdict_labels)
    print len(set(verdict_labels))
    print Counter(verdict_labels)

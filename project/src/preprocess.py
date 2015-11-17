import xmltodict
import glob
from collections import Counter

DATA_FOLDER = '..\\data'

#Nonsense files (website sources, PDFs)
BLACKLIST = ['111251559.xml']
for x in range(95484218,95484250):
    BLACKLIST.append(str(x)+'.xml')
BLACKLIST = map(lambda x: DATA_FOLDER+'\\'+x, BLACKLIST)

if __name__ == '__main__':

    filenames = glob.glob(DATA_FOLDER+'/*.xml')
    filenames = [x for x in filenames if x not in BLACKLIST]

    all_labels = []
    conclusion_labels = []
    verdict_labels = []

    for i, filename in enumerate(filenames):
        with open(filename) as fd:

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

            description = metadata['rdf:Description']

            if type(description) is list:
                description = description[0]
            law_areas = description['dcterms:subject']

            if type(law_areas) is not list:
                law_areas = [law_areas]

            for x in law_areas:
                labels = x['#text'].split('; ')
                all_labels += labels

                if is_verdict:
                    verdict_labels += labels
                else:
                    conclusion_labels += labels

        if i % 100 == 0:
            print i, '/', len(filenames)

    print '\n---overall'
    print set(all_labels)
    print len(set(all_labels))
    print Counter(all_labels)

    print '\n---conclusion'
    print set(conclusion_labels)
    print len(set(conclusion_labels))
    print Counter(conclusion_labels)

    print '\n---verdict\n'
    print set(verdict_labels)
    print len(set(verdict_labels))
    print Counter(verdict_labels)

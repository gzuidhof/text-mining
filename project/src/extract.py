from __future__ import division
import xmltodict
import glob
import pickle
import codecs
import util
import os, sys
from collections import Counter, OrderedDict
from multiprocessing.pool import ThreadPool, Pool

RAW_DATA_FOLDER = '../data/raw/'
PLAINTEXT_FOLDER = '../data/plaintext/'
DATA_FOLDER = '../data/'

#Nonsense files (website sources, PDFs)
BLACKLIST = ['111251559.xml','100410518.xml','100410517.xml',
'100410520.xml','101269578.xml','103382656.xml','105316443.xml','105316475.xml',
'106383445.xml','107272081.xml','107272273.xml','107731834.xml','108448680.xml',
'108525279.xml','109900347.xml','110300759.xml','113314243.xml','113629960.xml']
for x in range(95484218,95484250):
    BLACKLIST.append(str(x)+'.xml')
BLACKLIST = map(lambda x: RAW_DATA_FOLDER+x, BLACKLIST)
BLACKLIST = [os.path.normpath(path) for path in BLACKLIST]

#Only used for debugging (for checking whether all relevant text is extracted)
NONSENSE_KEYS = ['@lang','@id','@xml:space','@xmlns','@role','@mark','@xmlns:xsd',
'@xmlns:xsi','@xmlns:xlink', '@linkend','@label','@cols','@colname','@fileref','@align','@scale',
'@width','@height','@format','@numeration','@depth', '@namest','@nameend', '@xmlns:rs',
'@morerows','@rowsep','@valign','@xmlns:nsxlink','@nsxlink:href', '@border', '@colwidth']

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
            if key in ['para','title','#text','nr','bridgehead','alt','subscript','superscript'] and value is not None:
                text_so_far.append(value)
            elif key not in NONSENSE_KEYS and value is not None:
                print "UNEXPECTED KEY/VALUE", key, value

def extract_plaintext(filepath, outpath):
    with open(filepath) as fd:

        #Filename without extension
        file_id = util.filename_without_extension(filepath)
        plain_text = []

        try:
            obj = xmltodict.parse(fd.read())
            root = obj['open-rechtspraak']
            metadata = root['rdf:RDF']

            #############
            # Extract content as plain text
            #############

            if 'inhoudsindicatie' in root:
                summary = root['inhoudsindicatie']
                as_plain_text(summary, plain_text)

            if 'uitspraak' in root:
                content = root['uitspraak']
                as_plain_text(content, plain_text)

            if 'conclusie' in root:
                content = root['conclusie']
                as_plain_text(content, plain_text)

            #print filepath
            #Write to outfile
            with codecs.open(outpath+file_id+'.txt', 'w', 'utf-8') as f:
                 for line in plain_text:
                        print>>f, line

        except KeyError, e:
            #Skip silently

            #print "ERROR:", sys.exc_info()[0]
            #print "Skipping faulty:", filepath
            #print "file_id:", file_id
            return
        except:
            print "ERROR:", sys.exc_info()[0]
            print "file_id:", file_id
            return



def extract_labels(filepath):
    with open(filepath) as fd:

        #Filename without extension
        file_id = util.filename_without_extension(filepath)

        try:
            obj = xmltodict.parse(fd.read())
            root = obj['open-rechtspraak']
            metadata = root['rdf:RDF']

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
                text_labels += labels

            return text_labels

        except KeyError, e:
            #Skip silently

            #print "ERROR:", sys.exc_info()[0]
            #print "Skipping faulty:", filepath
            #print "file_id:", file_id
            return
        except:
            print "ERROR:", sys.exc_info()[0]
            print "file_id:", file_id
            return

def extract_all_labels(filenames, out_filepath=DATA_FOLDER+'labels.p', chunk_size=2000):
    print "EXTRACTING ALL LABELS INTO {0}".format(out_filepath)
    all_labels = []
    label_dict = {}

    filenames_chunks = util.chunks(filenames, chunk_size)

    for i, chunk in enumerate(filenames_chunks):
        pool = Pool(processes=util.CPU_COUNT)
        chunk_labels = pool.map(extract_labels, chunk)
        pool.close()

        for filepath, labels in zip(chunk, chunk_labels):
            if labels is not None:
                file_id = util.filename_without_extension(filepath)
                label_dict[file_id] = labels
                all_labels += labels

        print i+1, '/', len(filenames_chunks)

    #Write labels to file
    with open(out_filepath,'w') as f:
        pickle.dump(label_dict, f)

    print '\nLabels:'
    print len(set(all_labels))
    print Counter(all_labels)


#Necessary for multiprocess map function, which can only have one variable
#as input, so we encode it in one tuple
#
#Using a partial function did not work, as that can not be pickled.
def __extract_plaintext_as_tuple(filename_outfolder_tuple):
    filename, out_folder = filename_outfolder_tuple
    return extract_plaintext(filename, out_folder)


def extract_all_plaintext(filenames, out_folder=PLAINTEXT_FOLDER):
    print "EXTRACTING PLAINTEXT FROM {0} FILES INTO {1}".format(len(filenames),out_folder)

    #Zip the filename input with the output folder
    tuple_input = zip(filenames, [out_folder]*len(filenames))

    pool = Pool(processes=util.CPU_COUNT)
    #pool = Pool(processes=1)
    num_tasks = len(filenames)
    for i, _ in enumerate(pool.imap_unordered(__extract_plaintext_as_tuple, tuple_input), 1):
        sys.stderr.write('\rdone {0:%}'.format(i/num_tasks))
    pool.close()

    print "\nDONE"

if __name__ == '__main__':
    in_folder = RAW_DATA_FOLDER
    out_folder = PLAINTEXT_FOLDER

    todo_filenames = util.todo_filepaths(in_folder,'.xml', out_folder,'.txt', blacklist=BLACKLIST)

    all_filenames = util.todo_filepaths(in_folder,'.xml', blacklist=BLACKLIST)
    extract_all_plaintext(todo_filenames, out_folder)
    #extract_all_labels(all_filenames, DATA_FOLDER+'labels.p')

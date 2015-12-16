from __future__ import division
import sys
import time
import frog

import glob

def duration_to_string(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

if __name__ == '__main__':
    INPUT_FOLDER = '../data/plaintext/'
    OUTPUT_FOLDER = '../data/frogged/'

    files = glob.glob(INPUT_FOLDER+'*.txt')
    #print(files)
    seen = []
    start_time = time.time()

    frog = frog.Frog(frog.FrogOptions(parser=False,mwu=False,ner=False,morph=False,chunking=False), "/etc/frog/frog.cfg")

    for i, filename in enumerate(files):
        with open(filename,'r') as in_file:
            output = frog.process_raw(in_file.read())
        print ('> PROCESSING', filename, str(len(seen))+'/'+str(len(files)))

        seen.append(filename)

        #Timings (estimation of time remaining)
        runtime = time.time() - start_time
        per_document_time = runtime/len(seen)
        remaining_time = (len(files)-len(seen))*per_document_time
        total_time = remaining_time+runtime


        print ("RUNTIME", duration_to_string(runtime),
         "("+duration_to_string(per_document_time)+")",
          'REMAINING', duration_to_string(remaining_time),
           'TOTAL', duration_to_string(total_time))

        frogged_filename = filename.split('/')[-1].split('.txt')[0]

        with open(OUTPUT_FOLDER+frogged_filename+'.frog.out', 'w') as f:
            f.write(output)

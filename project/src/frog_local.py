from __future__ import division
import sys
import time
import frog
import glob
import util
import pickle
import os
from multiprocessing.pool import Pool

def duration_to_string(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


def frog_process_files(files, verbose=True):
    seen = []
    start_time = time.time()

    frogger = frog.Frog(frog.FrogOptions(parser=False,mwu=False,ner=False,morph=False,chunking=False, numThreads=8), "/etc/frog/frog.cfg")

    for i, filename in enumerate(files):
        with open(filename,'r') as in_file:
            output = frogger.process_raw(in_file.read())

        if verbose:
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

        frogged_filename = util.filename_without_extension(filename, '.txt')

        with open(OUTPUT_FOLDER+frogged_filename+'.frog.out', 'w') as f:
            f.write(output)

if __name__ == '__main__':
    INPUT_FOLDER = '../data/plaintext/'
    OUTPUT_FOLDER = '../data/frogged/'

    files = util.todo_filepaths(INPUT_FOLDER, '.txt', OUTPUT_FOLDER, '.frog.out')

    if os.path.exists('../data/frog_todo.p', 'r'):
        print ("USING FROG TODO!")
        with open('../data/frog_todo.p') as f:
            files = pickle.load(f)


    n_processes = 1
    print ("N_CPU", util.CPU_COUNT, " N PROCESSES", n_processes)

    file_chunks = util.split(files, n_processes)

    pool = Pool(processes=n_processes)
    pool.map(frog_process_files, file_chunks)
    pool.join()
    pool.close()

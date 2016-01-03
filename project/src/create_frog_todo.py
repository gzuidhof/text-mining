import os
import pickle
import util

INPUT_FOLDER = '../data/plaintext/'
OUTPUT_FOLDER = '../data/frogged/'

files = util.todo_filepaths(INPUT_FOLDER, '.txt', OUTPUT_FOLDER, '.frog.out')
files = sorted(files)
print "N files TODO:", len(files), files[:10]
with open('../data/_frog_todo.p','wb') as f:
    pickle.dump(files, f)

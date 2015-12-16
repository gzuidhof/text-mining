import glob
import os
import multiprocessing
CPU_COUNT = multiprocessing.cpu_count()



def filename_without_extension(filepath, extension='.xml'):
    return filepath.split('\\')[-1][:-1*len(extension)]

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def todo_filepaths(in_folder, in_extension, out_folder=None, out_extension=None, blacklist=[]):
    in_filenames = glob.glob(in_folder+'*'+in_extension)

    if out_folder is not None:
        out_filenames = glob.glob(out_folder+'*'+out_extension)
    else:
        out_filenames = []

    #Just in case
    in_filenames = map(os.path.normpath, in_filenames)
    out_filenames = map(os.path.normpath, out_filenames)
    blacklist = map(os.path.normpath, blacklist)

    s = set(blacklist)
    in_filenames = [x for x in in_filenames if x not in blacklist]

    in_ids = [filename_without_extension(n, in_extension) for n in in_filenames]
    out_ids= [filename_without_extension(n, out_extension) for n in out_filenames]

    #Dictionary from filename without extension to full input path
    in_dict = {file_id: file_path for file_id, file_path in zip(in_ids, in_filenames)}

    print "input: {0} ({1}) {2}".format(in_folder, in_extension, len(in_filenames))
    print "output: {0} ({1}) {2}".format(out_folder, out_extension, len(out_filenames))

    done = set(out_ids)
    todo_ids = [x for x in in_ids if x not in done]

    print "todo: {0}\n\n".format(len(todo_ids))

    return [in_dict[todo_id] for todo_id in todo_ids]

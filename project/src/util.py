import multiprocessing
CPU_COUNT = multiprocessing.cpu_count()


def filename_without_extension(filepath, extension='.xml'):
    return filepath.split('\\')[-1][:-1*len(extension)]

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

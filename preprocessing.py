import pickle
import subprocess
import re
import glob

DUMP_FILE = 'detexedsources.dump'
def read_tex_sources():
    tex_data={}
    dataset_path = [
        "dataset/calculus/*/*.tex",
        "dataset/discover_physics/*/*.tex",
        "dataset/fundamentals-of-calculus/*/*.rbtex",
        "dataset/general_relativity/*/*.rbtex",
        "dataset/special_relativity/*/*.rbtex",
        "dataset/ThinkCPP/book/ch*.tex",
        "dataset/ThinkJava/thinkjava.tex",
        "dataset/javajavajava/texfiles/*.tex",
        "dataset/lm/lm/qm/*.rbtex",
        "dataset/lm/lm/vw/*.rbtex" 
    ]

    for path in dataset_path:
        for filename in glob.glob(path):
            try:
                process = subprocess.Popen(['detex', filename], stdout=subprocess.PIPE)
            except FileNotFoundError:
                raise FileNotFoundError("Please verify that detex is installed on your system. https://github.com/pkubowicz/opendetex")

            output, err = process.communicate()
            tex_data[filename] = str(output)
            tex_data[filename] = ' '.join(tex_data[filename].split('\\n'))
        
    return tex_data

def dump_detex_data():
    tex_data_dict = read_tex_sources()
    fd = open(DUMP_FILE,'wb')
    pickle.dump(tex_data_dict,fd)
    fd.close()
    print('Processed %d source files and dumped data' % len(tex_data_dict))

def read_detex_data():
    fd = open(DUMP_FILE, 'rb')
    data_dict = pickle.load(fd)
    return data_dict


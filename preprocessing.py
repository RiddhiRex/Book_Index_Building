import pickle
import subprocess
import re
import glob

DUMP_FILE = 'detexedsources.dump'
def get_source_files():
    '''
    This function returns the list of source tex files
    '''
    source_files = []

    dataset_path = [
        'dataset/calculus/*/*.tex',
        'dataset/discover_physics/*/*.tex',
        'dataset/fundamentals-of-calculus/*/*.rbtex',
        'dataset/general_relativity/*/*.rbtex',
        'dataset/special_relativity/*/*.rbtex',
        'dataset/ThinkCPP/book/ch*.tex',
        'dataset/ThinkJava/thinkjava.tex',
        'dataset/javajavajava/texfiles/*.tex',
        'dataset/lm/lm/qm/*.rbtex',
        'dataset/lm/lm/vw/*.rbtex',
        'dataset/*.tex' 
    ]

    for path in dataset_path:
        for filename in glob.glob(path):
            source_files.append(filename)

    return source_files

def get_plain_text(filename):
    '''
    This function takes a tex source filename as input and returns content of 
    file converted to plain text
    '''
    try:
        process = subprocess.Popen(['detex', filename], stdout=subprocess.PIPE)
    except FileNotFoundError:
        raise FileNotFoundError('Please verify that detex is installed on your system. https://github.com/pkubowicz/opendetex')

    output, err = process.communicate()
    output = str(output)
    output = output.replace('\\n',' ')
    
    return output

def dump_detex_data():
    '''
    This function dumps a dictionary of {filename: {plaintext: <>}} into DUMP_FILE
    '''
    properties_dict = {}
    source_files = get_source_files()

    for f in source_files:
        properties_dict[f] = {'plaintext' : get_plain_text(f) }

    fd = open(DUMP_FILE,'wb')
    pickle.dump(properties_dict,fd)
    fd.close()

    print('Processed %d source files and dumped data' % len(properties_dict))

def read_detex_data():
    '''
    Reads the data dumped back into dictionary
    '''
    fd = open(DUMP_FILE, 'rb')
    properties_dict = pickle.load(fd)
    return properties_dict

def feature_extraction(tex_source):
    '''
    Input:
        tex_source - tex source (str)
    Returns:
        A dictionary where each key represents a feature and value is a list of 
        words that exhibit that feature. 
        Eg:

        {
        'indicies' : ['Apple','Banana',.....],
        'sections' : ['Fruits', 'Veggies', ...],
        .
        .
        .
        }
    '''
    features_dict = {}

    indices = set(re.findall(r'\\index{(.*)}',tex_source))
    # We will include sub indexing, formatting inside indexing, labels etc for final model
    indices = [re.sub(r'(}.*?index|}.*?label|!).*','',string) for string in indices]

    sections = set(re.findall(r'\\section{(.*)}',tex_source))
    sections = [re.sub(r'(}.*?index|}.*?label|!).*','',string) for string in sections]

    subsections = set(re.findall(r'\\subsection{(.*)}',tex_source))
    subsections = [re.sub(r'(}.*?index|}.*?label|!).*','',string) for string in subsections]
    
    italicized = re.findall(r'\\emph{(.*?)}',tex_source)
    italicized.extend(re.findall(r'\\textit{(.*)}',tex_source))
    #italicized.extend(re.findall(r'\\em([^}].*)',tex_source))
    
    
    bold = re.findall(r'\\textbf{(.*)}',tex_source)
    
    underline = re.findall(r'\\uline{(.*)}',tex_source)
    underline.extend(re.findall(r'\\uwave{(.*)}',tex_source))
    
    large = re.findall(r'(\\large|\\Large|\\LARGE|\\huge|\\Huge)',tex_source)

    features_dict['indices'] = indices
    features_dict['sections'] = sections
    features_dict['subsections'] = subsections
    features_dict['italicized'] = italicized
    features_dict['bold'] = bold
    features_dict['underline'] = underline
    features_dict['large'] = large

    return features_dict

def populate_properties():
    '''
    This function reads the dict that is dumped by dump_detex_data
    and for each key (file), updates the value with feature list
    '''
    # Read the dump that is prepopulated
    feature_dict = read_detex_data()
    
    for filename in feature_dict.keys():
        fd =  open(filename)
        tex_source = fd.read()
        feature_dict[filename].update(feature_extraction(tex_source))
    
    return feature_dict

# def get_dataframe_from_properties():

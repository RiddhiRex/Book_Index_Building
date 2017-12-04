import nltk, collections
import pandas as pd
import numpy as np


def generate_dataframe(filename,feat_dict,feature_list_from_tex):
    df = pd.DataFrame()
    candidate_list = feat_dict["candidate_list"]
    frequency = collections.Counter()
    for w in candidate_list:
        frequency[w] += 1
        
    tagged = nltk.pos_tag(frequency.keys())
    
    notpos = ['VB','VBP','PRP','IN','RB','DT','WDT','WP','WRB','UH','TO','RBR','RBS','POS','MD','EX','WP$','PRP$','$','CC','LS','PDT','RP','VBZ', 'CD','JJS','JJR']
    w1 = list(filter(lambda word_tag: word_tag[1]  not in notpos, tagged))
    
    word = []
    pos = []
    count = []

    
    for each in w1:
        word.append(each[0])
        pos.append(each[1])
    df['word']=word
    df['pos']=pos
    for each in word:
        count.append(frequency[each])
    df['wordcount'] = count
    cols = ['NN','NNP','NNS','VB','VBG','VBD','VBN','FW','NNPS','JJ']
    df1 = pd.DataFrame(0, index=np.arange(len(df['word'])), columns=cols)
    df2 = pd.concat([df, df1], axis=1)
    
    for idx, row in df2.iterrows():
        pos = row['pos']
        df2.set_value(idx, pos, 1)
    
    for feat in feature_list_from_tex:
        df2[feat] = 0
        df2.loc[df2['word'].isin(feat_dict[feat]),feat]=1
    df2["filename"] = filename
    return df2

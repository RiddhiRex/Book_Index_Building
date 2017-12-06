import nltk, collections
import numpy as np
from nltk.collocations import *
from nltk.corpus import stopwords
import subprocess
import pandas as pd
import re
from sklearn.externals import joblib
import random
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, accuracy_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

import seaborn as sns
import matplotlib.pyplot as plt

import candidate_list_gen
import dataframe_generation
import Classifier
import math
import index_generator
import preprocessing

n = sys.argv[1]
evaluation_files = []
evaluation_files.extend(sys.argv[2])
# This reads the *.tex sources and dumps them to a file
preprocessing.dump_detex_data()
feature_list_from_tex = ["indices","sections","subsections","large","underline","italicized","bold"]
feature_dict = preprocessing.populate_properties()
df = pd.DataFrame([])
for filename in feature_dict:
    feature_dict[filename]["candidate_list"] = candidate_list_gen.process_text(feature_dict[filename]["plaintext"])
    df = df.append(dataframe_generation.generate_dataframe(filename,feature_dict[filename],feature_list_from_tex))
df = dataframe_generation.add_tf_idf(df)

test_files = ["dataset/discover_physics/ch02/ch02.tex","dataset/general_relativity/ch03/ch03.rbtex","dataset/general_relativity/ch05/ch05.rbtex","dataset/calculus/ch07/ch07.tex","dataset/fundamentals-of-calculus/ch05/ch05.rbtex","dataset/discover_physics/ch05/ch05.tex"]

non_train_files = test_files + evaluation_files


df_test = pd.DataFrame([])
df_train = pd.DataFrame([])
df_evaluation = pd.DataFrame([])

df_test = df.loc[df.filename.isin(test_files),]

df_train = df.loc[~df.filename.isin(non_train_files),]
df_train = df_train.append([df_train[df_train.indices==1]]*100)

df_evaluation = df.loc[df.filename.isin(evaluation_files),]

feature_list = ['NN', 'NNP', 'NNS', 'VBG', 'VBD', 'VBN','VBZ', 'VBP', 'VB', 'CD', 'JJ', 'JJS', 'JJR', 'FW', 'NNPS','sections', 'subsections', 'large', 'underline','tf-idf','italicized', 'bold']


x_train = df_train[feature_list]
x_test = df_test[feature_list]

y_train = df_train["indices"]
y_test = df_test["indices"]


#rfc= RandomForestClassifier()
rfc =  MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)

rfc.fit(x_train, y_train)

pred_test = rfc.predict(x_test)

df_test["pred"] = pred_test
#Evaluate

x_eval = df_evaluation[feature_list]
y_eval = df_evaluation["indices"]
pred_evaluation = rfc.predict(x_eval)
pred_prob = rfc.predict_proba(x_eval)

index_prob = [ele[1] for ele in pred_prob]

df_evaluation["pred"] = pred_evaluation
df_evaluation["pred_prob"] = index_prob
df_pred_indices = df_evaluation[df_evaluation["pred"]==1]
df_pred_indices = df_pred_indices[["word","pred_prob"]].sort_values("pred_prob",ascending=False)
df_pred_indices = df_pred_indices.head(n)
print(df_pred_indices)

# DSF_BookIndexBuilding
Objective:
The purpose of the project is to build a tool that applies the principles of data science to
automatically build back-of-the-book indices. The input provided by the user is the number of
words to be generated in the index and the tex source file for which index will be automatically
generated.

Data sources:
We initially considered using papers from arXiv.org as the main source for data for this project.
However, we found that the number of papers with indices were less. Therefore we used tex

source of textbooks that were available online as our primary data source. We have used
textbooks from domains such as physics, mathematics, computer science. This was done to
make sure that the model that we build doesn’t overfit a particular domain. We faced encoding
issues while processing some of the books. We had to resolve them to make the data sources
usable.

Data Preprocessing:
A particular challenge is this task is that a very small number of words in a given source file will
be present in the index. As a result the ‘index-word’ class will have significantly less members
than the ‘non-index-word’ class.

We attempt to address this by having a ‘Candidate list’ of words which is a list of candidate or
potential index words. To put it simply, the candidate list will have only those words or n-grams
that have a probability > 0 to be in index. If we can ascertain that a word will not be in the
index, we do not add it to the candidate list.

In an ideal scenario, the candidate list will have each and every word that is a part of index and
other words that have a good chance to be in the index. We are generating the candidate list by
passing the data through the following pipeline:

● Convert to plain text : As a first step in the pipeline, we convert the tex source to plain
text. This is done by integrating the detex tool into our pipeline.

● Tokenization : This process splits up the strings into substrings and phrases by using
delimiters such as white spaces, line endings and punctuations. We used the tokenizer
provided by the NLTK module to achieve this.

● Stop word removal: Stop words are frequently occurring words in common language
such as: of, it, the, so, thus; these do not contribute to the context or idea being
conveyed in the text. Instead, they are used to connect phrases and sentences. As such,
these shouldn’t be part of the candidate list. Stop words account for nearly 20-30% of a
file and removing them is a crucial step in the pipeline. We are using the NLTK’s
stopwords corpus.

● Removing symbols and numerical values: Since we are using academic literature as data
source, numerical values and symbols also constitute a good portion of the text. These
are removed as well since they generally don’t go into the index.

● Bigrams : Since indices are not always single words, we would need the candidate list to
contain n-grams as well. We have populated the candidate list with only single words
and bigrams.

● Filtering by POS : We observed that certain Parts of Speech never appear in the indices,
thus having them in the candidate list is of little use.



Feature extraction:
We combine the candidate lists of each source file into a unified dataset where each row
represents a word from a candidate list. A point to note is that multiple rows can have the same
word appearing in them as long as they come from different source files. i.e, the word column
in our dataset is not unique, but the (word,source_file) pair of each row is unique.
Under the assumption that the authors capitalize, underline or italicize only the word that is a
central idea of the passage, we rely on special formatting to measure a word’s significance. We
achieved this by parsing the tex source file and checking for the tags such as: \section,
\subsection, \headings,\uline,\emph,\textit,\textbf, and \Large.


Features of the Baseline model:
Features used to building the baseline model are listed below:
word, pos, wordcount, NN, NNP, NNS, VBG, VBD, VBN, VBZ, VBP, VB, CD, CC, LS, JJ, JJS, JJR, PDT,
PRP, RP, FW, NNPS,, section, subsection, italicized, bold, underline, large.


Results of the baseline model:
True Positives : 12
False Positives : 467
True Negatives : 5649
False Negatives : 37
Accuracy is 0.91
Precision is 0.025
Recall is 0.24
F score is 0.045

Drawbacks of the baseline model:
● Only TF was being used as a feature ignoring the Inverse Document Frequency (IDF).
● Pruning done when generating candidate list is insufficient.
● Imbalance between the number of samples in the index class and the non-index class.
● Poor recall value.

Extended baseline model:
We used a Multilayer Perceptron(MLP) network to build our extended baseline model. The
model generates the probability of the sample for each class in the data set. We use this
probability value to rank the list of indices predicted by our model.
As mentioned earlier, we observed that the number of index-words is very less compared to
the number of non-index words in the candidate list. Even after pruning the candidate list using
the aforementioned steps, the ratio didn’t improve significantly. In order to balance class size
between index-words class and non-index words class, we duplicate the rows of index words
during training.
Term Frequency(TF) is the frequency of a word in a document. However, there are some words
which are not significant to the topic of the document but occur frequently in all documents,
like 'example', 'is', 'so', etc. Using the term frequency alone as a feature doesn’t provide good
results since such common words usually have a high Term Frequency per document. So, we
have added TF-IDF as a new feature for the extended baseline model. Inverse Document
Frequency(IDF) reduces the significance of frequently occuring words in the document set but
increases the significance of words that occur rarely[8]. TF-IDF is the product of TF and IDF.

Results of extended baseline model:
True Positives:53
False Positives:1382
True Negatives:8081
False Negatives :13
Accuracy is 0.854
Precision is 0.036
Recall is 0.803
F Score is 0.071

The results above show a significant improvement over the baseline model. The recall value for
the index class is 0.8 for the extended baseline model whereas the baseline model had a recall
value of 0.24.

Evaluation:
We kept aside a document from the dataset to evaluate the results of our model. In the data
processing phase, 2039 candidate words were generated for this document. Out of these, 255
words were selected as index-worthy by the model. Out of the 16 index words present in the
document, 10 index words were predicted by the model. Also, 9 of these predicted words are
part of the top 100 index-worthy words ranked based on the probability of the sample being in
the index class. 3 out of the top 10 words in the ranked list of predicted index words are actual
index words in the document.


Areas of improvement:
As the evaluation results show, the tool does well in predicting the index words. The ranking
mechanism also helps us to reduce the number of false positives. But there is scope for
improvement in the following areas:

1) Improving the scoring function to make sure that most of the actual index fall in the top
30% of the ranked predictions.

2) The tool currently finds the predicted words in the latex source and marks them as index
using \index{} tag. This fails when the predicted word is part of macro names or other
keywords.


Reference:
1. Can Back-of-the-Book Indexes be Automatically Created?
[http://delivery.acm.org/10.1145/2510000/2505627/p1745-wu.pdf]
2. Syntactic approaches to automatic book indexing
[www.aclweb.org/anthology/P88-1025]
3. Investigations in Unsupervised Back-of-the-Book Indexing
[web.eecs.umich.edu/~mihalcea/papers/csomai.flairs07.pdf]
4. Creating a Testbed for the Evaluation of Automatically Generated Back-of-the-book
Indexes [web.eecs.umich.edu/~mihalcea/papers/csomai.cicling06.ps]
5. Preprocessing Techniques for Text Mining
[www.researchgate.net/publication/273127322_Preprocessing_Techniques_for_Text_
Mining]
6. Tokenizing Words and Sentences with NLTK
[www.pythonprogramming.net/tokenizing-words-sentences-nltk-tutorial/]
7. Data structures and algorithms for indexing.
[www.cl.cam.ac.uk/teaching/1314/InfoRtrv/lecture2.pdf]
8. tf-idf wiki [https://en.wikipedia.org/wiki/Tf%E2%80%93idf]

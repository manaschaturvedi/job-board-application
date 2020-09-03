import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re
import pickle


def pre_process(text):
    # lowercase
    text=text.lower()
    #remove tags
    text=re.sub("<!--?.*?-->","",text)
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)

    return text


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results


def get_stop_words(stop_file_path):
    """load stop words """
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

df = pd.read_csv('data/github-jobs.csv')
df = df.fillna('')
df['job_info'] = df['job_role'] + ' ' + df['description']
df['job_info'] = df['job_info'].apply(lambda x : pre_process(x))

# print(df['job_info'].iloc[0])
 
#load a set of stop words
stopwords = get_stop_words("resources/stopwords.txt")
 
#get the text column 
docs = df['job_info'].tolist()

#create a vocabulary of words, 
#ignore words that appear in 85% of documents, 
#eliminate stop words
cv = CountVectorizer(max_df=0.85, stop_words=stopwords)
word_count_vector = cv.fit_transform(docs)

# 10 words from our vocabulary (total: 5140 words)
print(list(cv.vocabulary_.keys())[:10])

tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

# pickling the models
with open('count_vectorizer.pickle', 'wb') as fh:
   pickle.dump(cv, fh)

with open('tf_idf_model.pickle', 'wb') as fh:
   pickle.dump(tfidf_transformer, fh)

# extracting keywords from a job description

# you only needs to do this once, this is a mapping of index to 
feature_names = cv.get_feature_names()

job_description = 'Python Developer Strong experience in specialized analytics tools and technologies Python, R, SQL.\
Experience with object-oriented Python development.\
Understanding of database technologies and data storage approaches including but not limited to MySQL, Postgres, MongoDB, HBase, and Redis.\
Experience in Agile software development methodologies.\
Identify the right modeling approach(es) for given scenario and articulate why the approach fits.\
Assess data availability and modeling feasibility.\
Evaluate model fit and based on business / function scenario.\
Good interpersonal communication skills and influencing skills.\
Eagerness to learn and ability to work with limited supervision.'

tf_idf_vector=tfidf_transformer.transform(cv.transform([job_description]))

#sort the tf-idf vectors by descending order of scores
sorted_items=sort_coo(tf_idf_vector.tocoo())
 
#extract only the top n; n here is 3
keywords = extract_topn_from_vector(feature_names,sorted_items, 10)
 
# now print the results
print("\n=====Doc=====")
print(job_description)
print("\n===Keywords===")
for k in keywords:
    print(k,keywords[k])

import pickle


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
    
    print(feature_vals)

    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results, feature_vals


cv = open ("count_vectorizer.pickle", "rb")
count_vectorizer = pickle.load(cv)

tf = open ("tf_idf_model.pickle", "rb")
tfidf_transformer = pickle.load(tf)

feature_names = count_vectorizer.get_feature_names()

job_description = 'Python Developer Strong experience in specialized analytics tools and technologies Python, R, SQL.\
Experience with object-oriented Python development.\
Understanding of database technologies and data storage approaches including but not limited to MySQL, Postgres, MongoDB, HBase, and Redis.\
Experience in Agile software development methodologies.\
Identify the right modeling approach(es) for given scenario and articulate why the approach fits.\
Assess data availability and modeling feasibility.\
Evaluate model fit and based on business / function scenario.\
Good interpersonal communication skills and influencing skills.\
Eagerness to learn and ability to work with limited supervision.'

tf_idf_vector=tfidf_transformer.transform(count_vectorizer.transform([job_description]))

#sort the tf-idf vectors by descending order of scores
sorted_items=sort_coo(tf_idf_vector.tocoo())
 
#extract only the top n; n here is 3
keyword_scores, keywords = extract_topn_from_vector(feature_names, sorted_items, 5)
 
# # now print the results
# print("\n=====Doc=====")
# print(job_description)
# print("\n===Keywords===")
# for k in keywords:
#     print(k,keywords[k])
print(keyword_scores)
print(keywords)
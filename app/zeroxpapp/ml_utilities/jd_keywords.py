import pickle


class JDTopKeywords:
    cv = open ("zeroxpapp/ml_utilities/count_vectorizer.pickle", "rb")
    count_vectorizer = pickle.load(cv)
    tf = open ("zeroxpapp/ml_utilities/tf_idf_model.pickle", "rb")
    tfidf_transformer = pickle.load(tf)
    feature_names = count_vectorizer.get_feature_names()

    def __init__(self, job_description):
        self.job_description = job_description

    def sort_coo(self, coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def extract_topn_from_vector(self, sorted_items, topn=10):
        """get the feature names and tf-idf score of top n items"""
        #use only topn items from vector
        sorted_items = sorted_items[:topn]
    
        score_vals = []
        feature_vals = []
        
        # word index and corresponding tf-idf score
        for idx, score in sorted_items:
            #keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(JDTopKeywords.feature_names[idx])

        #create a tuples of feature,score
        #results = zip(feature_vals,score_vals)
        results= {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]]=score_vals[idx]
        
        return results, feature_vals
    
    def fetch_top_keywords(self):
        tf_idf_vector=JDTopKeywords.tfidf_transformer.transform(
            JDTopKeywords.count_vectorizer.transform([self.job_description])
        )
        #sort the tf-idf vectors by descending order of scores
        sorted_items = self.sort_coo(tf_idf_vector.tocoo())
        #extract only the top n; n here is 5
        keyword_scores, keywords = self.extract_topn_from_vector(sorted_items, 10)
        return ','.join(keywords)


# job_description = 'Python Developer Strong experience in specialized analytics tools and technologies Python, R, SQL.\
# Experience with object-oriented Python development.\
# Understanding of database technologies and data storage approaches including but not limited to MySQL, Postgres, MongoDB, HBase, and Redis.\
# Experience in Agile software development methodologies.\
# Identify the right modeling approach(es) for given scenario and articulate why the approach fits.\
# Assess data availability and modeling feasibility.\
# Evaluate model fit and based on business / function scenario.\
# Good interpersonal communication skills and influencing skills.\
# Eagerness to learn and ability to work with limited supervision.'
# obj = JDTopKeywords(job_description)
# print(obj.fetch_top_keywords())
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer,HashingVectorizer
from sklearn.naive_bayes import BernoulliNB

class Model:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier = BernoulliNB()
        
    def train(self,train_data, targets):
        train_data = self.vectorizer.fit_transform(train_data)
        self.classifier.fit(train_data, targets)
    
    def predict(self, phrases):
        predictions = [self.classifier.predict(self.vectorizer.transform([phrase])) for phrase in phrases]
        return predictions
    
class Model1(Model):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = BernoulliNB()

class Model2(Model):
    def __init__(self):
        self.vectorizer = HashingVectorizer(n_features = 2**18)
        self.classifier = BernoulliNB()
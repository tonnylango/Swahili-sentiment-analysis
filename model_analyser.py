from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt

from ml2 import Model1,Model, Model2

#given a list of file names, organize the data in a list
def organize_data(filenames):
    processed_data = []
    for filename in filenames:    
        with open(filename, "r") as file:
            for line in file.read().split('\n'):
                if len(line.split("\t")) == 2 and line.split("\t")[1] != "":
                    processed_data.append(line.split("\t"))
        
    return processed_data

def load_data(filename, polarity = 1):
    data = []
    with open(filename, "r", encoding = 'utf8',errors = 'ignore') as file:
        #data = [[line, polarity] for line in file.read().split('\n') ]
        for line in file.read().split('\n'):
            data.append([line, polarity])
    return data

def evaluate_model(inputs, outputs, model, n_folds):
    inputs_copy = np.array(inputs)
    outputs_copy = np.array(outputs)
    kf = KFold(n_splits = n_folds) #define the split
    scores = list()
    
    for train_index, test_index in kf.split(inputs):
        inputs_train, inputs_test = inputs_copy[train_index], inputs_copy[test_index]
        outputs_train, outputs_test = outputs_copy[train_index], outputs_copy[test_index]
        model.train(inputs_train, outputs_train)
        predictions = model.predict(inputs_test)
        accuracy = accuracy_score(outputs_test,predictions)
        scores.append(accuracy)
    return scores

def graph():
    m = evaluate_model(X, y, Model(), 10)
    m1 = evaluate_model(X, y, Model1(), 10)
    m2 = evaluate_model(X, y, Model2(), 10)
    x = np.arange(0,20)
    plt.plot(x, m, label = "model")
    plt.plot(x, m1, label = "model1")
    plt.plot(x, m2, label = "model2")
    
    plt.xlabel('scores')
    plt.ylabel('x')
    
    plt.legend("Model")
    
    plt.legend()
    
    plt.show()

from joblib import dump
def save_model( model, filename):
    dump(model, filename)

if __name__ == '__main__':
    base_directory = 'C:\\Users\\tonny\\Desktop\\project\\swahili-sentiment-analysis\\'
    file1 = base_directory + "positive.txt"
    file2 = base_directory + "negative.txt"
    file3 = base_directory + "positive1.txt"
    file4 = base_directory + "negative1.txt"
    file5 = base_directory + "positive2.txt"
    file6 = base_directory + "negative2.txt"
    #file3 = base_directory + "yelp_labelled.txt"
    files = [file1, file2]
    data1 = load_data(file1, polarity =  1) + load_data(file3, polarity =  1) + load_data(file5, polarity =  1)
    data2 = load_data(file2, polarity =  0) + load_data(file4, polarity =  0) + load_data(file6, polarity =  0)
    data = np.vstack((data1, data2 ))
    #specify the data
    X = data[:,0]
    #specify the target labels
    y = data[:,-1]
    #Split the data up in train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)
    model = Model1()
    model.train(X_train, y_train)
    predictions = model.predict(X_test)
    print("accuracy:", accuracy_score(y_test,predictions))
    cm = confusion_matrix(y_test, predictions)
    print(cm)
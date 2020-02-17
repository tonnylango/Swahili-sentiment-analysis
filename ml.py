from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB

def display_result(value):
    phrase, result = value
    result = "Phrase positive" if result[0] == '1' else "Phrase negative"
    print(phrase, ":", result)

def analyse_phrase(classifier,vectorizer, phrase):
    return phrase, classifier.predict(vectorizer.transform([phrase]))

def get_data_from_sources():
    base_directory = "C:\\Users\\tonny\\Desktop\\project stuff\\IA-master\\ClassificacaoComentariosComNaiveBayes\\Datasets\\"
    
    with open(base_directory + "imdb_labelled.txt", "r") as archive_text:
        data = archive_text.read().split('\n')
        
    with open(base_directory + "amazon_cells_labelled.txt", "r") as archive_text:
        data += archive_text.read().split('\n')

    with open(base_directory + "yelp_labelled.txt", "r") as archive_text:
        data += archive_text.read().split('\n')
        
    return data

def data_processing(data):
    processed_data = []
    for d in data:
        if len(d.split("\t")) == 2 and d.split("\t")[1] != "":
            processed_data.append(d.split("\t"))
            
    return processed_data

def divide_data_for_training_and_validation(data):
    total_amount = len(data)
    percentage_of_training = 0.75
    train = []
    validate = []
    
    for index in range(0, total_amount):
        if index < total_amount * percentage_of_training:
            train.append(data[index])
        else:
            validate.append(data[index])
    return train, validate

def pre_processing():
    data = get_data_from_sources()
    processed_data =  data_processing(data)
    
    return divide_data_for_training_and_validation(processed_data)

def perform_training(train_logs, vectorizer):
    train_comments = [train_log [0] for train_log in train_logs]
    train_responses = [train_log[1] for train_log in train_logs]
    
    train_comments = vectorizer.fit_transform(train_comments)
    
    return BernoulliNB().fit(train_comments, train_responses)

def perform_simple_evaluation(logs_for_evaluation):
    evaluation_comments = [log_for_evaluation[0] for log_for_evaluation in logs_for_evaluation]
    evaluation_responses = [log_for_evaluation[1] for log_for_evaluation in logs_for_evaluation]
    
    total = len(evaluation_comments)
    hits = 0
    for index in range(0,total):
        analysed_result = analyse_phrase(classifier, vectorizer, evaluation_comments[index])
        phrase, result = analysed_result
        hits += 1 if result[0] == evaluation_responses[index] else 0
    
    return hits * 100 / total

def perform_complete_evaluation(logs_for_evaluation):
    evaluation_comments = [log_for_evaluation[0] for log_for_evaluation in logs_for_evaluation]
    evaluation_responses = [log_for_evaluation[1] for log_for_evaluation in logs_for_evaluation]
    
    total = len(evaluation_comments)
    true_positives = 0
    true_negatives = 0
    false_positives =0
    false_negatives =0
    
    for index in range(0, total):
        analysed_result = analyse_phrase(classifier, vectorizer, evaluation_comments[index])
        phrase, result = analysed_result
        if result[0] == '0':
            true_negatives  += 1 if evaluation_responses[index]  == '0' else 0
            false_negatives += 1 if evaluation_responses[index] != '0' else 0
        else:
            true_positives += 1 if evaluation_responses[index]  == '1' else 0
            false_positives += 1 if evaluation_responses[index]  != '1' else 0
            
    return (true_positives * 100 / total,
            true_negatives * 100 / total,
            false_positives * 100 / total,
            false_negatives * 100 / total
            )
        
records_of_training, records_for_evaluation = pre_processing()
vectorizer = CountVectorizer(binary = 'true') 
classifier = perform_training(records_of_training, vectorizer)

display_result(analyse_phrase(classifier, vectorizer, "this is the best movie"))
display_result(analyse_phrase(classifier, vectorizer, "this is the worst movie"))
display_result(analyse_phrase(classifier, vectorizer, "awesome!"))
display_result(analyse_phrase(classifier, vectorizer, "10/10"))
display_result(analyse_phrase(classifier, vectorizer, "So bad"))

percentage_hits = perform_simple_evaluation(records_for_evaluation)
information_analysis = perform_complete_evaluation(records_for_evaluation)

true_positives, true_negatives, false_positives, false_negatives = information_analysis

print("The model had a hit rate of", percentage_hits,"%")

print("Where", true_positives, "% are true positives")
print("and", true_negatives, "% are true negatives")

print("and", false_positives, "% are false positives")
print("and", false_negatives, "% are false negatives")
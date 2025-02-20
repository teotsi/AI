import re
from decimal import *
from os import listdir
from os.path import isfile, join

# DataSet = []
delim = ";"  # delimiter for .csv file
header = ";Accuracy;Precision;Recall;F1 Score"  # header for .csv file


def filereader(x, data_type):
    training_data = []
    path = data_type + "/part"
    for i in range(1, x):
        training_data += [path + str(i) + "/" + f for f in listdir(path + str(i)) if isfile(join(path + str(i), f))]

    words = [0]
    dataset.append(words)
    i = 1
    for t in range(1, len(training_data) + 1):
        file = [training_data[t - 1]]
        dataset.append(file)
    for f in training_data:
        if 'spmsg' in f:
            dataset[i][0] = "spam"
        else:
            dataset[i][0] = "ham"
        with open(f, 'r') as MailFile:
            for line in MailFile:
                for word in re.findall(r'\w+', line):
                    try:
                        index = dataset[0].index(word)
                        dataset[i][index] = True
                    except ValueError:
                        dataset[0].append(word)
                        for c in range(1, len(training_data) + 1):
                            dataset[c].append(False)
                        dataset[i][len(dataset[0]) - 1] = True
        i += 1


def training():
    words_num = len(dataset[0])
    emails_num = len(dataset)
    prob_array = [[0 for x in range(2)] for y in range(words_num)]

    for i in range(words_num):
        for j in range(1, emails_num):
            if dataset[j][i]:
                if dataset[j][0] == "spam":
                    prob_array[i][0] += 1
                else:
                    prob_array[i][1] += 1
    return prob_array


def naive_bayes(file, prob_array):
    getcontext().prec = 30
    email = open(file, 'r')
    p_yes = Decimal(1)
    p_no = Decimal(1)
    i = 0
    sum_yes = 0
    sum_no = 0
    for line in email:
        for word in re.findall(r'\w+', line):
            i += 1
            try:
                index = dataset[0].index(word)
                p_yes *= Decimal(prob_array[index][0]) / Decimal(prob_array[0][0])
                p_no *= Decimal(prob_array[index][1]) / Decimal(prob_array[0][1])
                if i % 3 == 0:
                    sum_yes += p_yes
                    sum_no += p_no
                    p_yes = Decimal(1)
                    p_no = Decimal(1)
            except ValueError:
                continue
    total_yes = Decimal(sum_yes) / Decimal(i / 3)
    total_no = Decimal(sum_no) / Decimal(i / 3)
    total = Decimal(total_yes) + Decimal(total_no)
    prob_spam = total_yes / total
    return prob_spam


document_types = [
    ("bare", 0.6203),
    ("lemm", 0.6169),
    ("lemm_stop", 0.775),
    ("stop", 0.775),
]

if __name__ == '__main__':
    getcontext().prec = 30
    with open("output.csv", "w") as output:
        for document_type, threshold in document_types:
            output.write(f"{document_type}{header}\n")
            for i in range(2, 12):
                print(f"Set: {document_type} number of parts: {i - 1:d}")
                dataset = []
                output.write(f"{i - 1:d}{delim}")
                total_spam_mo = Decimal(0)
                total_ham_mo = Decimal(0)
                print("Creating dataset...")
                filereader(i, document_type)
                print("Dataset creation is complete. ")
                print("Training begins...")
                sum_words = training()
                print("Training is complete.")
                print("Checking emails...")
                files = []
                my_path = document_type + "/part10/"
                false_positive = false_negative = true_positive = true_negative = miss = 0
                files += [my_path + f for f in listdir(my_path) if isfile(join(my_path, f))]
                spam_count = ham_count = 0
                for f in files:
                    prob = naive_bayes(f, sum_words)
                    if prob > threshold:
                        if 'spmsg' not in f:
                            miss += 1
                            false_positive += 1
                        else:
                            true_positive += 1
                    else:
                        if 'spmsg' in f:
                            miss += 1
                            false_negative += 1
                        else:
                            true_negative += 1
                    if 'spmsg' in f:
                        spam_count += prob
                    else:
                        ham_count += prob

                accuracy = 1 - miss / len(files)
                precision = true_positive / (true_positive + false_positive)
                recall = true_positive / (true_positive + false_negative)
                f1_score = 2 * true_positive / (2 * true_positive + false_positive + false_negative)
                print(f"Accuracy: {accuracy:f}")
                print(f"Precision: {precision:f}")
                print(f"Recall: {recall:f}")
                print(f"F1 score: {f1_score:f}")
                print(f"Avg spam: {spam_count / Decimal(49):f}\nAvg ham: {ham_count / Decimal(291):f}")
                output.write(f"{accuracy:f}{delim}{precision:f}{delim}{recall:f}{delim}{f1_score:f}\n")
            output.write("\n")

import re
from decimal import *
from os import listdir
from os.path import isfile, join

# DataSet = []
delim = ";"  # delimiter for .csv file
header = ";Accuracy;Precision;Recall;F1 Score"  # header for .csv file


def filereader(x, data_type):
    TrainingData = []
    path = data_type + "/part"
    for i in range(1, x):
        TrainingData += [path + str(i) + "/" + f for f in listdir(path + str(i)) if isfile(join(path + str(i), f))]

    words = [0]
    DataSet.append(words)
    i = 1
    for t in range(1, len(TrainingData) + 1):
        file = [TrainingData[t - 1]]
        DataSet.append(file)
    for f in TrainingData:
        if 'spmsg' in f:
            DataSet[i][0] = "spam"
        else:
            DataSet[i][0] = "ham"
        with open(f, 'r') as MailFile:
            for line in MailFile:
                for word in re.findall(r'\w+', line):
                    try:
                        index = DataSet[0].index(word)
                        DataSet[i][index] = True
                    except ValueError:
                        DataSet[0].append(word)
                        for c in range(1, len(TrainingData) + 1):
                            DataSet[c].append(False)
                        DataSet[i][len(DataSet[0]) - 1] = True
        i += 1


def training():
    words_num = len(DataSet[0])
    emails_num = len(DataSet)
    prob_array = [[0 for x in range(2)] for y in range(words_num)]

    for i in range(words_num):
        for j in range(1, emails_num):
            if DataSet[j][i]:
                if DataSet[j][0] == "spam":
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
                index = DataSet[0].index(word)
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


if __name__ == '__main__':
    getcontext().prec = 30
    types = ["bare", "lemm", "lemm_stop", "stop"]
    probs = [0.6203, 0.6169, 0.775, 0.775]
    output = open("output.csv", "w")

    for j in types:
        type_of_data = j
        threshold = probs[types.index(j)]
        output.write("%s%s\n" % (type_of_data, header))
        for i in range(2, 12):
            print("Set: %s number of parts: %i" % (type_of_data, i - 1))
            DataSet = []
            output.write("%i%s" % (i - 1, delim))
            total_spam_mo = Decimal(0)
            total_ham_mo = Decimal(0)
            print("Creating dataset...")
            filereader(i, type_of_data)
            print("Dataset creation is complete. ")
            print("Training begins...")
            sum_words = training()
            print("Training is complete.")
            print("Checking emails...")
            files = []
            mypath = type_of_data + "/part10/"
            false_positive = false_negative = true_positive = true_negative = miss = 0
            files += [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]
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
            print("Accuracy: %f" % accuracy)
            print("Precision: %f" % precision)
            print("Recall: %f" % recall)
            print("F1 score: %f" % f1_score)
            print("Avg spam: %f\nAvg ham: %f" % (spam_count / Decimal(49), ham_count / Decimal(291)))
            output.write("%f%s%f%s%f%s%f\n" % (
                accuracy, delim, precision, delim, recall, delim, f1_score))
        output.write("\n")
    output.close()

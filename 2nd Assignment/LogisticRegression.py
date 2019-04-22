import math
import re
from os import listdir
from os.path import isfile, join

DataSet = []
spam_counter = 0
ham_counter = 0

spam_array = []


def filereader():
    TrainingData = []
    mypath = "bare/part"
    for counter_a in range(1, 10):  # Give a range
        TrainingData += [mypath + str(counter_a) + "/" + f for f in listdir(mypath + str(counter_a)) if
                         isfile(join(mypath + str(counter_a), f))]

    words = [0]
    DataSet.append(words)
    i = 1
    for t in range(1, len(TrainingData) + 1):
        file = [TrainingData[t - 1]]
        DataSet.append(file)
    for f in TrainingData:
        if 'spmsg' in f:
            DataSet[i][0] = 'spam'
            global spam_counter
            spam_counter += 1
        else:
            DataSet[i][0] = 'ham'
            global ham_counter
            ham_counter += 1
        with open(f, 'r') as MailFile:
            for line in MailFile:
                for word in re.findall(r'\w+', line):
                    flag = False
                    if word in DataSet[0]:
                        DataSet[i][DataSet[0].index(word)] += 1
                        flag = True
                    if flag == False:
                        DataSet[0].append(word)
                        for c in range(1, len(TrainingData) + 1):
                            DataSet[c].append(0)
                        DataSet[i][DataSet[0].index(word)] += 1
        i += 1


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def calc_spam_array():
    words_num = len(DataSet[0])
    email_num = len(DataSet)
    spam_array = [0 for y in range(words_num)]
    for em in range(1, email_num):
        for i in range(words_num):
            if DataSet[em][i] != 0:
                if DataSet[em][0] == 'spam':
                    spam_array[i] += 1

    return spam_array


def prediction(b, email):
    words_num = len(DataSet[0])
    email_num = len(DataSet)
    y = 0

    for i in range(1, words_num):
        y = y + (b[i] * DataSet[email][i])

    y = sigmoid(y)

    if y >= 0.32:
        return 1
    else:
        return 0


def calc_cost(email_num, b):
    cost = 0
    email = 1
    for i in range(1, email_num):
        if DataSet[i][0] == 'spam':
            cost = cost + math.pow(prediction(b, email) - 1, 2)
        else:
            cost = cost + math.pow(prediction(b, email) - 0, 2)
        email = email + 1
    cost = cost / (-email_num)

    return cost


def training(spm, alpha=0.1, iterations=20):
    words_num = len(DataSet[0])
    email_num = len(DataSet)
    coefficients = [0 for y in range(words_num)]

    for i in range(iterations):
        cost = calc_cost(email_num, coefficients)

        for em in range(1, email_num):
            w = prediction(coefficients, em)
            for j in range(0, len(coefficients)):
                if DataSet[em][0] == 'spam':
                    coefficients[j] = coefficients[j] + alpha * ((w - 1) * spm[j])
                else:
                    coefficients[j] = coefficients[j] + alpha * ((w - 0) * spm[j])
                coefficients[j] = coefficients[j] / email_num

    return coefficients


def find_words(file, weight, spam):
    word_sum = 0
    with open(file, 'r') as MailFile:
        for line in MailFile:
            for word in re.findall(r'\w+', line):

                try:
                    index = DataSet[0].index(word)
                    word_sum = word_sum + weight[index] * spam[index]

                except ValueError:
                    continue
    word_sum = sigmoid(word_sum)

    return word_sum


if __name__ == '__main__':

    print("Creating dataset...")
    filereader()
    print("Dataset creation is complete. ")
    print("Training begins...")
    spm = calc_spam_array()
    weights = training(spm)

    print("Training is complete.")
    print("Checking email...")
    files = []
    mypath = "bare/part10/"
    k = z = miss = file_counter = 0
    false_positive = false_negative = true_positive = true_negative = 0
    email = 1
    files += [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]

    spam_total = 0
    ham_total = 0

    ham_sum = 0
    spam_sum = 0

    arr = []
    for f in files:
        prob = find_words(f, weights, spm)

        if prob < 0.5:
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

        email = email + 1
        file_counter = file_counter + 1
    print("Misses: %i/%i" % (miss, len(files)))
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    f1_score = 2 * true_positive / (2 * true_positive + false_positive + false_negative)
    print(precision)
    print(recall)
    print(f1_score)

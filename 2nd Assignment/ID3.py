import re
from os import listdir
from os.path import isfile, join

from Node import *
from Tree import *

DataSet = []
TestingDataSet = []


def filereader():
    TrainingData = []
    mypath = "lemm/part"
    for i in range(1, 10):
        TrainingData += [mypath + str(i) + "/" + f for f in listdir(mypath + str(i)) if
                         isfile(join(mypath + str(i), f))]
    words = [0]
    DataSet.append(words)
    i = 1
    for t in range(1, len(TrainingData) + 1):
        file = [TrainingData[t - 1]]
        DataSet.append(file)
    for f in TrainingData:
        if ('spmsg' in f):
            DataSet[i][0] = "spam"
        else:
            DataSet[i][0] = "ham"
        with open(f, 'r') as MailFile:
            for line in MailFile:
                for word in re.findall(r'\w+', line):
                    try:
                        index = DataSet[0].index(word)
                        if DataSet[i][index] == 0:
                            DataSet[i][index] += 1
                    except ValueError:
                        DataSet[0].append(word)
                        for c in range(1, len(TrainingData) + 1):
                            DataSet[c].append(0)
                        DataSet[i][len(DataSet[0]) - 1] += 1

        i += 1


def MakingTestingDataSet():
    TestingFiles = []
    mypath = "lemm/part10/"
    TestingFiles += [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]
    words = [0]
    TestingDataSet.append(words)
    for t in range(1, len(TestingFiles) + 1):
        file = [TestingFiles[t - 1]]
        TestingDataSet.append(file)
    i = 1
    for f in TestingFiles:
        if ('spmsg' in f):
            TestingDataSet[i][0] = "spam"
        else:
            TestingDataSet[i][0] = "ham"
        with open(f, 'r') as MailFile:
            for line in MailFile:
                for word in re.findall(r'\w+', line):
                    try:
                        index = TestingDataSet[0].index(word)
                        if TestingDataSet[i][index] == 0:
                            TestingDataSet[i][index] += 1
                    except ValueError:
                        TestingDataSet[0].append(word)
                        for c in range(1, len(TestingFiles) + 1):
                            TestingDataSet[c].append(0)
                        TestingDataSet[i][len(TestingDataSet[0]) - 1] += 1
        i += 1


def accuracy():
    count = 0
    for f in TestingDataSet:
        if f[0] != 0:
            if f[0] == f[1]:
                count += 1
    return count * (100 / (len(TestingDataSet) - 1))


tp = 0
tn = 0
fp = 0
fn = 0


def precision():
    global tp
    global tn
    global fp
    global fn
    for f in TestingDataSet:
        if f[0] != 0:
            if f[0] == f[1] and f[0] == "spam":
                tp += 1
            elif f[0] != f[1] and f[0] == "ham":
                tn += 1
            elif f[0] != f[1] and f[0] == "spam":
                fp += 1
            elif f[0] == f[1] and f[0] == "ham":
                fn += 1
    return tp / (tp + fp)


def recall():
    return tp / (tp + fn)


def f1():
    if recall() == 0 and precision() == 0:
        return 0.0
    return 2 * (precision() * recall()) / (precision() + recall())


if __name__ == '__main__':
    filereader()
    print("The DataSet has been created")
    head = Node(0)
    usedlist = []
    treehead = Treemaker(DataSet, head, usedlist)
    print("The tree has been created")
    MakingTestingDataSet()
    for f in TestingDataSet:
        searching(f, TestingDataSet, treehead, DataSet)
    print("Accuracy: " + str(accuracy()))
    print("Precision: " + str(precision()))
    print("Recall: " + str(recall()))
    print("F1: " + str(f1()))

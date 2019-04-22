from ID3 import *
import math
from Node import *


def entropy(list, word=0, value=0):
    if word == 0:
        spams = 0
        hams = 0
        for f in list:
            if f[0] != 0:
                if f[0] == "spam":
                    spams += 1
                else:
                    hams += 1
        if hams == 0 and spams == 0:
            return 0
        pham = hams / (hams + spams)
        pspam = spams / (hams + spams)
        if pham == 0:
            factor1 = 0
        else:
            factor1 = (pham * math.log(pham, 2))
        if pspam == 0:
            factor2 = 0
        else:
            factor2 = (pspam * math.log(pspam, 2))
        return -factor1 - factor2
    else:
        spams = 0
        hams = 0
        i = list[0].index(word)
        for f in list:
            if f[0] != 0:
                if f[i] == value:
                    if f[0] == "spam":
                        spams += 1
                    else:
                        hams += 1
        if hams == 0 and spams == 0:
            return 0
        pham = hams / (hams + spams)
        pspam = spams / (hams + spams)
        if pham == 0:
            factor1 = 0
        else:
            factor1 = (pham * math.log(pham, 2))
        if pspam == 0:
            factor2 = 0
        else:
            factor2 = (pspam * math.log(pspam, 2))
        return -factor1 - factor2


def InfoGain(list, word1, value1=0, word2=0):
    if word2 == 0:
        zeros = 0
        aces = 0
        i = list[0].index(word1)
        for f in list:
            if f[0] != 0:
                if f[i] == 0:
                    zeros += 1
                else:
                    aces += 1
        if zeros == 0 and aces == 0:
            pzero = 0
            pace = 0
        else:
            pzero = zeros / (zeros + aces)
            pace = aces / (zeros + aces)
        return entropy(list) - (pzero * entropy(list, word1)) - (pace * entropy(list, word1, 1))
    else:
        zeros = 0
        aces = 0
        i = list[0].index(word1)
        j = list[0].index(word2)
        for f in list:
            if f[0] != 0:
                if f[i] == value1:
                    if f[j] == 0:
                        zeros += 1
                    else:
                        aces += 1
        if zeros == 0 and aces == 0:
            pzero = 0
            pace = 0
        else:
            pzero = zeros / (zeros + aces)
            pace = aces / (zeros + aces)
        return entropy(list) - (pzero * entropy(list, word1)) - (pace * entropy(list, word1, 1))


def Treemaker(list, head, usedlist):
    if head.data == 0:
        max = -1
        spams = 0
        maxword = "0"
        for f in list:
            if f[0] != 0:
                if f[0] == "spam":
                    spams += 1
        if spams == len(list) - 1:
            head.add_child("spam")
        elif spams == 0:
            head.add_child("ham")
        else:
            for w in list[0]:
                if w != 0:
                    info = InfoGain(list, w)
                    if max < info:
                        max = info
                        maxword = w
            usedlist.append(maxword)
        head = Node(maxword)
        Treemaker(list, head, usedlist)
    else:
        max = -1
        maxword = "0"
        spamsl = 0
        hamsl = 0
        countl = 0
        spamsm = 0
        hamsm = 0
        countm = 0
        noless = False
        i = list[0].index(head.data)
        for f in list:
            if f[0] != 0:
                if f[i] == 0:
                    countl += 1
                    if f[0] == "spam":
                        spamsl += 1
                    else:
                        hamsl += 1
                else:
                    countm += 1
                    if f[0] == "spam":
                        spamsm += 1
                    else:
                        hamsm += 1
        if countl != 0:
            if hamsl == 0:
                child = Node("spam")
                head.add_child(child)
            elif spamsl == 0:
                child = Node("ham")
                head.add_child(child)
            elif countl != 0:
                if (spamsl * (100 / countl) >= 90.0):
                    child = Node("spam")
                    head.add_child(child)
                elif (hamsl * (100 / countl) >= 90.0):
                    child = Node("ham")
                    head.add_child(child)
                else:
                    i = list[0].index(head.data)
                    for f in list:
                        if f[i] == 1:
                            list.remove(f)
                    for w in list[0]:
                        if w != 0:
                            if w not in usedlist:
                                info = InfoGain(list, head.data, 0, w)
                                if max < info:
                                    max = info
                                    maxword = w
                    usedlist.append(maxword)
                    child = Node(maxword)
                    head.add_child(child)
        else:
            noless = True
        max = -1
        maxword = "0"
        if countm != 0:
            if spamsm == 0:
                child = Node("ham")
                head.add_child(child)
            elif hamsm == 0:
                child = Node("spam")
                head.add_child(child)
            elif countm != 0:
                if (spamsm * (100 / countm) >= 90.0):
                    child = Node("spam")
                    head.add_child(child)
                elif (hamsm * (100 / countm) >= 90.0):
                    child = Node("ham")
                    head.add_child(child)
                else:
                    i = list[0].index(head.data)
                    for f in list:
                        if f[i] == 0:
                            list.remove(f)
                    for w in list[0]:
                        if w != 0:
                            if w not in usedlist:
                                info = InfoGain(list, head.data, 1, w)
                                if max < info:
                                    max = info
                                    maxword = w
                    usedlist.append(maxword)
                    child = Node(maxword)
                    head.add_child(child)
        if noless == True:
            if (head.children[0].data != "spam") and (head.children[0].data != "ham"):
                Treemaker(list, head.children[0], usedlist)
        else:
            if (head.children[0].data != "spam") and (head.children[0].data != "ham"):
                Treemaker(list, head.children[0], usedlist)
            if len(head.children) > 1:
                if (head.children[1].data != "spam") and (head.children[1].data != "ham"):
                    Treemaker(list, head.children[1], usedlist)
    return head


def searching(f, list, head, Trainlist):
    if f[0] != 0:
        while True:
            if head.data not in list[0]:
                if head.data == "spam":
                    f[1] = "spam"
                    break
                elif head.data == "ham":
                    f[1] = "ham"
                    break
                head = head.children[0]
            elif head.data == "spam" or head.data == "ham":
                if head.data == "spam":
                    f[1] = "spam"
                    break
                elif head.data == "ham":
                    f[1] = "ham"
                    break
            elif len(head.children) == 2:
                if f[list[0].index(head.data)] == 0:
                    head = head.children[0]
                    if head.data == "spam":
                        f[1] = "spam"
                        break
                    elif head.data == "ham":
                        f[1] = "ham"
                        break
                elif f[list[0].index(head.data)] == 1:
                    head = head.children[1]
                    if head.data == "spam":
                        f[1] = "spam"
                        break
                    elif head.data == "ham":
                        f[1] = "ham"
                        break
            else:
                head = head.children[0]
                if head.data == "spam":
                    f[1] = "spam"
                    break
                elif head.data == "ham":
                    f[1] = "ham"
                    break


def printleafs(head):
    if not head.children:
        print(head.data)
    else:
        printleafs(head.children[0])
        printleafs(head.children[1])


def printTree(head, lor):
    if not head.children:
        print(lor + " " + head.data)
    else:
        print(lor + " " + head.data)
        if len(head.children) == 2:
            printTree(head.children[0], "left")
            printTree(head.children[1], "right")
        else:
            printTree(head.children[0], "lonely")

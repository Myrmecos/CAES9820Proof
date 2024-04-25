import copy
import pandas
import pandas as pd
import random as rd
import readchar
import math
from ultimateParaphraser import ultimate_paraphrase #comment out this part if paraphraser is not working properly


NUM_OF_CHOICES = 5

class FlashCard:
    wordArr = []
    doParaphrase = False;
    def __init__(self, yesPleaseParaphrase = False):
        rd.seed(42)
        self.doParaphrase = yesPleaseParaphrase

    def readFile(self, filePath, sheetName):
        file = pd.ExcelFile(filePath)
        sheet = pandas.read_excel(file, sheetName)
        terms = sheet["term"]
        explanation = sheet["explanation"]
        example = sheet["example"]
        self.wordArr = list(zip(terms, explanation, example))

    def printTupleAll(self):
        for i in self.wordArr:
            FlashCard.printTupleSingle(i)

    @staticmethod
    def generateChoiceAnswerPair(answerTuple, randomTuples):
        randomTuples.append(answerTuple)
        lngth = len(randomTuples)
        #shuffle pairs
        orderedTuples = list(zip(randomTuples, range(lngth))) #tuples with orders appended at back
        rd.shuffle(orderedTuples)
        ord = 0
        for i in range(lngth):
            if orderedTuples[i][1] == lngth - 1:
                ord = i
        lst = []
        for i in orderedTuples:
            lst.append(i[0])
        return lst, ord

    @staticmethod
    def generateChoiceAnswerString(answerTuple, randomTuples):
        lst, answerOrd = FlashCard.generateChoiceAnswerPair(answerTuple, randomTuples)
        lngth = len(lst)
        choiceList = []
        for i in range(lngth):
            choiceList.append(chr(ord("a") + i))
        retLst = list(zip(choiceList, lst))
        ans = choiceList[answerOrd]
        #result is: [('a', (word1:explanation1)), ('b', (word2, explanation2), ...)], 'c'
        return (retLst, ans)

    #fill distractionLst with incorrect answers
    def fillDistraction(self, distractionLst, ans):
        numberOfDistractions = min(NUM_OF_CHOICES - 1, len(self.wordArr))
        for i in range(numberOfDistractions):
            toAppend = rd.choice(self.wordArr)
            if (not (toAppend in distractionLst)) and not (toAppend == ans):
                distractionLst.append(toAppend)


    def paraphrase(self, myStr):
        if self.doParaphrase == True:
            return ultimate_paraphrase(myStr)
        return myStr;


    def startAskingQuestion(self, thisWord, choiceLst, ord, uncheckedLst):
        print("Explain: ", thisWord[0])
        input("press enter to see options: ")

        for i in choiceLst:
            print(i[0] + ". " + self.paraphrase(i[1][1]))
        print("------------------------------------")
        ans = input("if you want some hint, type \"h\".\nYour response: ")
        if (ans == "h"):
            print(thisWord[2])
            ans = input()
        if (ans != ord):
            uncheckedLst.append(thisWord)
            print("uh-oh. not correct.")
            print("the meaning of the word", thisWord[0], "is:", thisWord[1], ".")
            if (type(thisWord[2]) == str):
                print("an example:", thisWord[2])
            print("================================================")
            return 0
        else:
            print("correct!")
        print("================================================")
        return 1

    def flashRound(self):
        uncheckedLst = copy.deepcopy(self.wordArr)
        correctCnt = 0
        totalCnt = 0
        while (len(uncheckedLst) >0):
            print("remaining words: ", len(uncheckedLst))
            thisWord = uncheckedLst.pop(0)
            distractions = [] #ie. incorrect choices
            self.fillDistraction(distractions, thisWord) #fill in distraction list, ie generate incorrect choices
            choiceLst, ord = self.generateChoiceAnswerString(thisWord, distractions)
            correctCnt += self.startAskingQuestion(thisWord, choiceLst, ord, uncheckedLst) #append the choice back to unchecked list if answered incorrectly
            totalCnt += 1
        print("well done! you made it! The correct rate is " + str(correctCnt/totalCnt) * 100 + "%")
        return



    #tests
    def testGenerateChoiceAnswerString(self):
        gp = "hi"
        random_pairs = [1, 2, 3, 4]
        self.generateChoiceAnswerString(gp, random_pairs)

    def testGenerateChoiceAnswerPair(self):
        gp = "hi"
        random_pairs = [1, 2, 3, 4]
        lst, ret = self.generateChoiceAnswerPair(gp, random_pairs)
        print(lst, ret)

    @staticmethod
    def printTupleSingle(tup):
        print("term: ", tup[0])
        print("explanation: ", tup[1])
        print("example sentence: ", tup[2])
        print("================================")



def testReadFile():
    fc = FlashCard(False) #replace "Flase" with "True" to start paraphrasing
    fc.readFile("terminology.xlsx", "Sheet5")
    #fc.printTupleAll()
    lst = []
    fc.flashRound()


def main():
    print("hi")

if __name__ == "__main__":
    testReadFile()

# encoding: utf-8

# !/usr/bin/env python35

'''

@author: act'

@contact:2289818400@qq.com

@file: galaxy.py

@time: 2018/4/28 20:44

@desc:
'''

import re
import sys

romanNumsMapping = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


#出现4次错误的数据组合
errorCombineRule = ["IIIVI", "IIIXI", "IIILI", "IIICI", "IIIDI", "IIIMI", "XXXLX", "XXXCX", "XXXDX", "XXXMX", "CCCDC","CCCMC"]

unknownKeyValsMapping = {}
expressionMapping = {}

knownStatementList = []
tobeResolvedWithParamList = []
unknownStatementList = []
unknownVals = {}

def errorCombineRuleCheck(paramsStr):
    for errorRule in errorCombineRule:
        if paramsStr.count(errorRule)>0:
            return True

    return False

def checkCombineRule(paramsList):
    paramsStr = ''.join(paramsList)
    # D L V不能出现重复
    if paramsStr.count("D") > 1 or paramsStr.count("L") > 1 or paramsStr.count("V") > 1:
        return False
    elif paramsStr.count("IIII")>0 or paramsStr.count("XXXX")>0 or paramsStr.count("CCCC")>0 or paramsStr.count("MMMM")>0:
        # I X C M 连续出现次数超过3次，错误的数据
        return False
    elif (errorCombineRuleCheck(paramsStr)):
        # I X C M 可连续出现四次，并且组合有问题的情况
        return False
    else:
        return True

numsRomanMapping = {1: "I", 5: "V", 10: "X", 50: "L", 100: "C", 500: "D", 1000: "M"}

#是否可以进行减法
def canBeSubstracted(numFir,numSec):
    romanFirStr = numsRomanMapping[numFir]
    romanSecStr = numsRomanMapping[numSec]

    if romanSecStr == 'V' or romanSecStr == 'L' or romanSecStr == 'D':
        # V L D 不能被减
        return False
    elif (romanFirStr == 'V' or romanFirStr == 'X') and romanSecStr == 'I':
        #I 只能被V X 减
        return True
    elif (romanFirStr == 'L' or romanFirStr == 'C') and romanSecStr == 'X':
        # X只能被L C 减
        return True
    elif (romanFirStr == 'D' or romanFirStr == 'M') and romanSecStr == 'C':
        # C 只能被D M 减
        return True
    else:
        return False


def caculateKnownExp(paramsList):
    sum = 0
    count = len(paramsList)
    #用来记录位置
    pointLoc = 0
    while pointLoc+1<=count:
        if pointLoc+1<count and paramsList[pointLoc]<paramsList[pointLoc+1]:
            #是否可以进行减法
            if canBeSubstracted(paramsList[pointLoc+1],paramsList[pointLoc]):
                sum = sum+paramsList[pointLoc+1]-paramsList[pointLoc]
                pointLoc+=2
            else:
                sum = sum + paramsList[pointLoc]
                pointLoc +=1
        elif (pointLoc+1<count and paramsList[pointLoc]>=paramsList[pointLoc+1]) or pointLoc+1==count:
            sum = sum+paramsList[pointLoc]
            pointLoc +=1

    return sum



def analyticalExpressions():
    for exp in expressionMapping:
        #数字集合
        digExp = []
        #罗马数据集合
        romanExp = []
        expParams = re.split(r'\s+', exp)
        canConvertParams = expParams[:-1]
        for param in canConvertParams:
            digExp.append(romanNumsMapping[unknownKeyValsMapping[param]])
            romanExp.append(unknownKeyValsMapping[param])
        #校验表达式
        if checkCombineRule(romanExp):
            #计算已知的罗马序列
            knownSum = caculateKnownExp(digExp)
            unknownVals[expParams[-1]] =[expressionMapping[exp], knownSum]
        else:
            #带有未知数的表达式有问题，退出
            print("the expression with unkown param is error")
            sys.exit()

    returnLinesList = []
    #返回how much is ?
    for statement in  knownStatementList:
         digExp = []
         romanExp = []
         expParams = re.split(r'\s+', statement)
         for x in expParams:
             digExp.append(romanNumsMapping[unknownKeyValsMapping[x]])
             romanExp.append(unknownKeyValsMapping[x])
         if checkCombineRule(romanExp):
             knownSum = caculateKnownExp(digExp)
             returnLinesList.append(statement+'is '+str(knownSum)+'\n')
         else:
            #带有未知数的表达式有问题，打印
            returnLinesList.append(statement+'is ? -----Expression does not match rule \n')
            print("Expression does not match rule")

    #返回带有未知数
    for statement in tobeResolvedWithParamList:
         digExp = []
         romanExp = []
         expParams = re.split(r'\s+', statement)
         canConvertParams = expParams[:-1]
         for x in canConvertParams:
             digExp.append(romanNumsMapping[unknownKeyValsMapping[x]])
             romanExp.append(unknownKeyValsMapping[x])
         if checkCombineRule(romanExp):
             knownSum = caculateKnownExp(digExp)
             quest = unknownVals[expParams[-1]][0]*knownSum//(unknownVals[expParams[-1]][1])
             returnLinesList.append(statement+'is '+str(quest)+' Credits\n')
         else:

             returnLinesList.append(statement+'is ?Credits ------Expression does not match rule \n')
             print("Expression does not match rule")

    return returnLinesList

def initData():
    global unknownKeyValsMapping
    unknownKeyValsMapping = {}
    global expressionMapping
    expressionMapping = {}
    global knownStatementList
    knownStatementList = []
    global tobeResolvedWithParamList
    tobeResolvedWithParamList = []
    global unknownStatementList
    unknownStatementList = []
    global unknownVals
    unknownVals = {}


def analyticalText(lines):
    for line in lines:
        if re.match(r"([a-zA-Z]+)\s+is\s+([I|V|X|L|C|D|M]$)", line):
            #参数赋值
            rs = re.match(r"([a-zA-Z]+)\s+is\s+([I|V|X|L|C|D|M]$)", line)
            unknownKeyValsMapping[rs.group(1)] = rs.group(2)
        elif re.match(r"(([a-zA-Z]+)\s+)+is\s+([1-9][0-9]+)\s+Credits$", line):
            rs = re.match(r"(([a-zA-Z]+)\s+)+is\s+([1-9][0-9]+)\s+Credits$", line)
            expre = re.split(r'\s+is\s+', line)[0]
            expressionMapping[expre] = int(rs.groups()[-1])
        elif re.match(r'how\s+much\s+is\s+([a-zA-Z]+\s+)+\?$', line):
            tobeExp = re.split(r'\s+is\s+', line)[1].replace("?","")
            knownStatementList.append(tobeExp.rstrip())
        elif re.match(r"how\s+many\s+Credits\s+is\s+([a-zA-Z]+\s+)+\?$", line):
            #表达式在is后
            tobeExp = re.split(r'\s+is\s+', line)[1].replace("?","")
            tobeResolvedWithParamList.append(tobeExp.rstrip())
        elif re.match(r"how\s+([0-9a-zA-Z\.\-\']+\s+)+\?$", line):
            unknownStatementList.append("I have no idea what you are talking about")
        else:
            print('invalid statement')
            continue

    return analyticalExpressions()


def readText(txt_path):
    try:
        initData()
        with open(txt_path,'r') as f:
            lines = f.readlines()
            if len(lines)==0:
                print("file is empty")
                sys.exit(-1)
            newLines = analyticalText(lines)
            textFilePathList = txt_path.split('.')

            with open(textFilePathList[0]+"_output."+textFilePathList[1], 'w') as wf:
                wf.writelines(newLines+unknownStatementList)
    except Exception as e:
        print('system error :',e.message)

if __name__=='__main__':
    readText('D:/pypro/galaxy.txt')








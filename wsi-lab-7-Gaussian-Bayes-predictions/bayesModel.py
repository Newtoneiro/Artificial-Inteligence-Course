import numpy as np
from candidate import Candidate

def getProbOfClass(dataset: list) -> list:
    """
    Returns the dictionary containing the info of evidence about class frequency, based on dataset
    """
    classes = list(set([candidate.getClass() for candidate in dataset]))
    clsDict = dict.fromkeys(classes)
    for cls in classes:
        clsDict[cls] = 0

    for candidate in dataset:
        clsDict[candidate.getClass()] += 1

    for cls in classes:
        clsDict[cls] /= len(dataset)
    
    return clsDict


def getMeanAndVariance(dataset: list) -> list:
    """
    Returns mean and variance values for each attribute of candidate in dataset
    """
    classes = list(set([candidate.getClass() for candidate in dataset]))
    attrCount = len(dataset[0].getAttributes())
    
    clsDict = dict.fromkeys(classes)
    for cls in classes:
        clsDict[cls] = [[] for _ in range(attrCount)]
    
    for candidate in dataset:
        for attr in range(attrCount):
            clsDict[candidate.getClass()][attr].append(candidate.getAttribute(attr))
    
    for cls in classes:
        for attr in range(attrCount):
            m = sum(clsDict[cls][attr])/len(clsDict[cls][attr])
            v = sum((x - m)**2 for x in clsDict[cls][attr])/len(clsDict[cls][attr])
            clsDict[cls][attr] = (m, v)
    
    return clsDict


def getPredictDict(candidate: Candidate, clsDict: dict, probOfClass: dict) -> float:
    """
    Returns dictionary with predictions resembling the bayes' model
    """
    predictDict = dict.fromkeys(clsDict.keys())
    for cls in clsDict.keys():
        predictDict[cls] = []
    
    for attr in range(len(candidate.getAttributes())):
        for cls in clsDict.keys():
            predictDict[cls].append(p(candidate.getAttribute(attr), clsDict[cls][attr]))
    
    for cls in clsDict.keys():
        prob = 0
        if cls in probOfClass.keys():
            prob = probOfClass[cls]
        for val in predictDict[cls]:
            prob *= val
        predictDict[cls] = prob

    return predictDict


def predict(candidate: Candidate, clsDict: dict, probOfClass: dict):
    """
    Returns the most likely prediction (class name)
    """
    predictDict = getPredictDict(candidate, clsDict, probOfClass)
    
    evidence = 0
    for cls in predictDict.keys():
        evidence += predictDict[cls]
    
    outputDict = dict.fromkeys(predictDict.keys(), 0)
    for cls in predictDict.keys():
        outputDict[cls] = (predictDict[cls]) / evidence
    
    maxVal = 0
    prediction = ''
    for cls in outputDict.keys():
        if outputDict[cls] > maxVal:
            maxVal = outputDict[cls]
            prediction = cls
    
    return prediction


def p(val: float, m_v: tuple):
    """
    Returns the p value used in getting the prediction resembling bayes' model
    """
    m, v = m_v
    return (1/np.sqrt(2 * np.pi)) * np.exp((-(val-m)**2)/2*v)
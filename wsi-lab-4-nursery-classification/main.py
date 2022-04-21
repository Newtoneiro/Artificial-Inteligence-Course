from candidate import Candidate
from math import log
from decisionTree import DecisionTreeNode
from visual import Visualization
from random import shuffle
import argparse
import sys

nursery_attributes = ["parents", "has_nurs", "form", "children", "housing", "finance", "social", "health"]
nursery_classes = ["not_recom", "recommend", "very_recom", "priority", "spec_prior"]


def getData(path: str) -> list:
    """
    Function used to fetch data from a file
    """
    data=[]
    try:
        with open(path, "r") as file_handle:
            for line in file_handle:
                attributes = [attr for attr in line.strip().split(',')]
                cls = attributes[-1]
                attributes.remove(cls)
                data.append(Candidate(attributes, cls))
        return data
    except (FileNotFoundError):
        print('File does not exist')
        return 0

# ID3

def getGeneralEntropy(dataset: list) -> float:
    """
    Returns general entropy for dataset
    """
    unique_classes = set([object.getClass() for object in dataset])
    unique_classes_count = dict.fromkeys(unique_classes, 0)

    for object in dataset:
        unique_classes_count[object.getClass()] += 1

    H = 0
    for cls in unique_classes_count.keys():
        H -= (unique_classes_count[cls]/len(dataset)) * log(unique_classes_count[cls]/len(dataset))

    return H


def getEntropyForAttributes(dataset: list, attr_indexes: list) -> list:
    """
    Returns the table of entropy for attributes given for current dataset
    """
    entropies = []
    unique_classes = set([object.getClass() for object in dataset])

    for i in attr_indexes:
        H = 0
        possible_attr = set([object.getAttribute(i) for object in dataset])
        
        possible_attr_count = dict.fromkeys(possible_attr, 0)
        for object in dataset:
            possible_attr_count[object.getAttribute(i)] += 1

        for attr in possible_attr:
            unique_classes_count = dict.fromkeys(unique_classes, 0)
            for object in dataset:
                if object.getAttribute(i) == attr:
                    unique_classes_count[object.getClass()] += 1
            
            H_attr = 0
            for cls in unique_classes_count.keys():
                if unique_classes_count[cls] > 0:
                    H_attr -= (unique_classes_count[cls]/possible_attr_count[attr]) * log(unique_classes_count[cls]/possible_attr_count[attr])
            
            H += (possible_attr_count[attr]/len(dataset)) * H_attr
        
        entropies.append(H)
    
    return entropies


def getMaxGainIndex(inf_gain: list) -> int:
    """
    Helper function for getting the index of max gain
    """
    max_gain = inf_gain[0]
    max_gain_index = 0
    for index, gain in enumerate(inf_gain[1:]):
        if gain > max_gain:
            max_gain = gain
            max_gain_index = index + 1
    return max_gain_index


def id3(dataset: list, attributes: list):
    """
    Main alghoritm part, function is called recursevly to build a decision tree starting in a root node
    """
    root = DecisionTreeNode()
    unique_classes = set([object.getClass() for object in dataset])
    if (len(unique_classes) == 1):
        root.isLeaf = True
        root.classValue = list(unique_classes)[0]
    elif not attributes:
        unique_classes_count = dict.fromkeys(unique_classes, 0)
        for object in dataset:
            unique_classes_count[object.getClass()] += 1
        root.isLeaf = True
        root.classValue = max(unique_classes_count, key=unique_classes_count.get)
    else:
        H = getGeneralEntropy(dataset)
        entropies = getEntropyForAttributes(dataset, attributes)
        inf_gain = [H - entropies[i] for i in range(0, len(entropies))]
        index = getMaxGainIndex(inf_gain)

        root.decidingAttr = attributes[index]
        possible_attr_values = set([object.getAttribute(attributes[index]) for object in dataset])
        for value in possible_attr_values:
            new_dataset = [object for object in dataset if object.getAttribute(attributes[index]) == value]
            new_node = id3(new_dataset, [attr for attr in attributes if attr != attributes[index]])
            
            new_node.count += len(new_dataset) # To eliminate bugs when testing object has unexpected value of given attribute 
            
            new_node.value = value
            root.childs.append(new_node)

    return root

# Analysys functions

def crossValidation(data: list, k: int, class_list: list, sum: bool=False, shuff: bool = False):
    """
    Perform and analyze the cross Validation of given dataset
    """
    if shuff:
        shuffle(data)
    partition = len(data) // k
    data_lists = [data[n * partition : (n+1) * partition] for n in range(0, k)]
    
    outcomes = []
    
    for test_index in range(0, k):
        test_data = data_lists[test_index]
        learn_data = []
        for i in range(0, k):
            if i != test_index:
                learn_data += data_lists[i]
        
        decisionTree = id3(learn_data, [i for i in range(0, len(data[0]._attributes))])
        confusion_matrix = getConfusionMatrix(test_data, decisionTree, class_list)
        outcomes.append(confusion_matrix)
    
    for matrix in outcomes:
        printMatrix(class_list, matrix, sum)


def analyseMatrix(class_list: list, matrix: list, sum:bool = False) -> list:
    """
    Function used to gain data from matrix for all of the attributes
    """
    outcome = []
    if sum:
        TP_A, FP_A, TN_A, FN_A = 0, 0, 0, 0
    for i, cls in enumerate(class_list):
        TP, FP, TN, FN = 0, 0, 0, 0
        TP = matrix[i][i]
        
        for row in range(0, len(matrix)):
            for col in range(0, len(matrix)):
                if (row != i and col != i):
                    TN += matrix[row][col]
                if (row == i and col != i):
                    FP += matrix[row][col]
                if (row != i and col == i):
                    FN += matrix[row][col]
        
        if sum:
            TP_A += TP
            FP_A += FP
            TN_A += TN
            FN_A += FN
        else:
            outcome.append(getMetrics(TP, TN, FP, FN))
    
    if sum:
        return(getMetrics(TP_A, TN_A, FP_A, FN_A))
    return outcome


def getMetrics(TP: int, TN: int, FP: int, FN: int):
    Recall = 1
    if (TP + FN != 0):
        Recall = TP / (TP + FN)
    Fallout = 1
    if ((FP + TN) != 0):
        Fallout = FP / (FP + TN)
    Precision = 1
    if (TP + FP != 0):
        Precision = TP / (TP + FP)
    Accuracy = 1
    if (TP + TN + FP + FN != 0):
        Accuracy = (TP + TN) / (TP + TN + FP + FN)
    F1 = 1
    if (Recall + Precision != 0):
        F1 = (2 * Precision * Recall) / (Recall + Precision)
    
    return  [Recall, Fallout, Precision, Accuracy, F1]
        

def getConfusionMatrix(test_data: list, decisionTree: DecisionTreeNode, class_list: list):
    """
    Calculating the confusion matrix from given dataset and decision tree
    """
    class_dict = {}
    confusion_matrix = []

    for i, val in enumerate(class_list):
        confusion_matrix.append([0 for element in class_list])
        class_dict[val] = i

    for object in test_data:
        predictedClass = decisionTree.getClass(object)
        confusion_matrix[ class_dict[object.getClass()] ][ class_dict[predictedClass] ] += 1
    
    return confusion_matrix


def printMatrix(class_list: list, confusion_matrix: list, sum:bool=False):
    """
    Function used to visualize the confusion matrixes
    """
    print(("{:^10}").format(''), end='')
    for val in class_list:
        print(("{:>12}").format(val), end='|')
    print('\n')
    for i, line in enumerate(confusion_matrix):
        print(("{:<10}").format(class_list[i]), end='|')
        for val in line:
            print((" {:>10} |").format(val), end='')
        print("\n")
    
    #Analyse
    outcome = analyseMatrix(class_list, confusion_matrix, sum)
    if sum:
        print(f"Rec: {round(outcome[0] * 100, 2)}% Fall: {round(outcome[1] * 100, 2)}% Prec: {round(outcome[2] * 100, 2)}% Acc: {round(outcome[3] * 100, 2)}% F1: {round(outcome[4] * 100, 2)}%")
        return
    for element in outcome:
        print(f"cls: {element[0]} Rec: {element[1]} Fall: {element[2]} Prec: {element[3]} Acc: {element[4]} F1: {element[5]}")


def analyseData(data: list):
    """
    Used to analyse data for amount of unique attributes segregated by classes
    """
    unique_classes = list(set([object.getClass() for object in data]))
    attributes_count = dict.fromkeys(unique_classes)
    
    for object in data:
        if not attributes_count[object.getClass()]:
            for i, cls in enumerate(unique_classes):
                attributes_count[cls] = []
                for attr in object._attributes:
                    attributes_count[cls].append({})
        i = 0
        for attr in object._attributes:
            if not attr in attributes_count[object.getClass()][i].keys():
                attributes_count[object.getClass()][i][attr] = 1
            else:
                attributes_count[object.getClass()][i][attr] += 1
            i += 1
    
    for stuff, val in attributes_count.items():
        print(stuff)
        for values in val:
            print(values)
        print("\n")


def main(cross_validation: int):
    data = getData("nursery.txt")
    if not data:
        return

    unique_classes = list(set([object.getClass() for object in data]))
    unique_classes.sort()
    
    crossValidation(data, cross_validation, unique_classes, True, True)

    # For visualisation, too complicated to trigger in argparse
    # root = id3(data, [i for i in range(0, len(data[0]._attributes))])
    # visualize = Visualization(800, 800, root, nursery_attributes)
    # visualize.show()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-K', '--K', type=int, required=True, help='number of partitions in cross validation')
    args = parser.parse_args()
    main(args.K)


from bayesModel import predict

def getConfusionMatrix(testData: list, classList: list, clsDict: dict, probOfClass: dict):
    """
    Calculating the confusion matrix from given dataset and decision tree
    """
    classDict = {}
    confusionMatrix = []

    for i, val in enumerate(classList):
        confusionMatrix.append([0 for element in classList])
        classDict[val] = i

    for object in testData:
        predictedClass = predict(object, clsDict, probOfClass)
        confusionMatrix[ classDict[object.getClass()] ][ classDict[predictedClass] ] += 1
    
    return confusionMatrix


def analyseMatrix(classList: list, matrix: list) -> list:
    """
    Function used to gain data from matrix for all of the attributes
    """
    TP_A, FP_A, TN_A, FN_A = 0, 0, 0, 0
    for i, cls in enumerate(classList):
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
        
        TP_A += TP
        FP_A += FP
        TN_A += TN
        FN_A += FN
    
    return(getMetrics(TP_A, TN_A, FP_A, FN_A))


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


def printMatrix(classList: list, confusionMatrix: list):
    """
    Function used to visualize the confusion matrixes
    """
    print(("{:^16}").format(''), end='')
    for val in classList:
        print(("{:17}").format(val), end='|')
    print('\n')
    for i, line in enumerate(confusionMatrix):
        print(("{:<15}").format(classList[i]), end='|')
        for val in line:
            print((" {:>15} |").format(val), end='')
        print("\n")
    
    outcome = analyseMatrix(classList, confusionMatrix)
    print(f"Rec: {round(outcome[0] * 100, 2)}% Fall: {round(outcome[1] * 100, 2)}% Prec: {round(outcome[2] * 100, 2)}% Acc: {round(outcome[3] * 100, 2)}% F1: {round(outcome[4] * 100, 2)}%")
    return
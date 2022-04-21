from confusionMatrix import getConfusionMatrix, printMatrix
from bayesModel import getProbOfClass, getMeanAndVariance
from candidate import Candidate
import random
import sys


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


def main():
    # Seed stuff
    seed = 0
    if not seed:
        seed = random.randrange(sys.maxsize)  
    random.seed(seed)
    print(f"The seed is : {seed}")
    
    #Parameters
    shuffle = 0
    test_train_proportion = 0.9
    path = "data.txt"

    #Get Data
    dataset = getData(path)

    if shuffle:
        random.shuffle(dataset)
    trainset = dataset[int(test_train_proportion * len(dataset)):]
    testset = dataset[:int(test_train_proportion * len(dataset))]

    #Get necessary datastructs
    probOfClass = getProbOfClass(trainset)
    clsDict = getMeanAndVariance(dataset)
    classList = [cls for cls in clsDict.keys()]
    
    #Analyse alghoritm
    confusionMatrix = getConfusionMatrix(dataset, classList, clsDict, probOfClass)
    printMatrix(classList, confusionMatrix)


if __name__ == "__main__":
    main()
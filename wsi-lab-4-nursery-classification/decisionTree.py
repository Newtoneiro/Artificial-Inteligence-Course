from candidate import Candidate

class DecisionTreeNode:
    """
    Single decisionTree node
    """
    def __init__(self):
        self.isLeaf = False # Is is a leaf Node
        self.classValue = None  # If its a leaf node, then what's the class prediction
        
        self.value = None   # Attribute value that led the object to this node
        self.decidingAttr = None    # Next deciding attribute which will decide the next step to take
        self.childs = []    # List of possible nodes to go to
    
    def getClass(self, object: Candidate):
        """
        This function is used to guess the class of given candidate based on decision tree
        """
        outcome = None
        if self.isLeaf:
            return self.classValue
        else:
            deciding_attribute = object.getAttribute(self.decidingAttr)
            for child in self.childs:
                if deciding_attribute == child.value:
                    outcome = child.getClass(object)
            if outcome is None: # If the value of attribute does not appear in tree
                outcome = self.childs[0].getClass(object)
        return outcome



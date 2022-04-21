class Candidate:
    """
    General class for containing info of single data unit (attributes and designated class)
    """
    def __init__(self, attributes:list, cls: str):
        self._attributes = [float(a) for a in attributes]
        self._cls = cls
    
    def getClass(self):
        """
        Returns the designated Class
        """
        return self._cls
    
    def getAttributes(self):
        """
        Returns the designated Attributes
        """
        return self._attributes
    
    def getAttribute(self, i: int):
        """
        Returns the attribute attached to corresponding index
        """
        return self._attributes[i]

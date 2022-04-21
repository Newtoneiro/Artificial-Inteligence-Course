class Candidate:
    """
    General class for containing info of single data unit (attributes and designated class)
    """
    def __init__(self, attributes:list, cls: str):
        self._attributes = attributes
        self._cls = cls
    
    def getClass(self):
        """
        Returns the designated Class
        """
        return self._cls
    
    def getAttribute(self, i: int):
        """
        Returns the attribute attached to corresponding index
        """
        return self._attributes[i]
    
    def __str__(self):
        """
        Debugging stuff
        """
        return f'pa: {self._parents} hn: {self._has_nurs} fo: {self._form} ch: {self._children} ho: {self._housing} fi: {self._finance} so: {self._social} he:{self._health} class: {self._cls}'

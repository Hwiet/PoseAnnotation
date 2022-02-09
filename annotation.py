from typing import List
from pose import Pose

"""
Interface for implementing read and write from a particular
annotation format
"""
class Annotation:
    def __init__(self, filename):
        self.fp = open(filename) # file pointer


    def write(self, poses):
        """Write pose data into whatever format"""
        raise NotImplementedError()

    
    def load(self) -> List[Pose]:
        """Read pose data from this particular format"""
        raise NotImplementedError()

    
    def __del__(self):
        self.fp.close()
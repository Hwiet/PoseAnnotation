from collections import namedtuple
from typing import Dict, List


Edge = namedtuple("Edge", ['joint1', 'joint2'])


class Joint:
    keys = []

    def __init__(self, position, name):
        self.position = position
        self.name = name
        self.data = dict()
        self.data['position'] = position
        self.data['name'] = name


    def __hash__(self):
        return hash(self.id)


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented


class Pose():
    joint_cls = Joint

    
    def __init__(self, joints: List[joint_cls]):
        self.joints = joints
        self.data = dict()


    def __len__(self):
        return len(self.joints)


    def __lt__(self, other):
        return len(self.joints) < len(other.joints)


    def __le__(self, other):
        return len(self.joints) <= len(other.joints)


    def __ge__(self, other):
        return len(self.joints) >= len(other.joints)


    def __gt__(self, other):
        return len(self.joints) > len(other.joints)


    def get_edges(self):
        return NotImplementedError


    def update_joint(self, key, x, y):
        self.joints[key].position = [x, y]


    def to_string(self):
        return NotImplementedError


class PoseNetJoint(Joint):
    keys = ['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']


    def __init__(self, confidence, name, cell, is_valid, position, id):
        super().__init__(position, name)
        self.data['cell'] = cell
        self.data['confidence'] = confidence
        self.data['is_valid'] = is_valid
        self.data['id'] = id


class PoseNetPose(Pose):
    joint_cls = PoseNetJoint


    def __init__(self, confidence=0, joints=list()):
        super().__init__(joints)
        self.data['confidence'] = confidence


    def get_edges(self):
        return [
            # edges on left side of the body
            Edge( self.joints[ 'left_hip' ], self.joints[ 'left_shoulder' ] ),
            Edge( self.joints[ 'left_shoulder' ], self.joints[ 'left_elbow' ] ),
            Edge( self.joints[ 'left_elbow' ], self.joints[ 'left_elbow' ] ),
            Edge( self.joints[ 'left_hip' ], self.joints[ 'left_knee' ] ),
            Edge( self.joints[ 'left_knee' ], self.joints[ 'left_ankle' ] ),
            # edges on left side of the body
            Edge( self.joints[ 'right_hip' ], self.joints[ 'right_shoulder' ] ),
            Edge( self.joints[ 'right_shoulder' ], self.joints[ 'right_elbow' ] ),
            Edge( self.joints[ 'right_elbow' ], self.joints[ 'right_wrist' ] ),
            Edge( self.joints[ 'right_hip' ], self.joints[ 'right_knee' ] ),
            Edge( self.joints[ 'right_knee' ], self.joints[ 'right_ankle' ] ),
            # edges that connect the left and right sides
            Edge( self.joints[ 'left_shoulder' ], self.joints[ 'right_shoulder' ] ),
            Edge( self.joints[ 'left_hip' ], self.joints[ 'right_hip' ])
        ]
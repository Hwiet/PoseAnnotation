from collections import namedtuple
from typing import Dict, List


Edge = namedtuple("Edge", ['joint1', 'joint2'])


class Joint:
    keys = []

    def __init__(self, position, id):
        self.position = position
        self.id = id


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


    def get_edges(self):
        return NotImplementedError


    def update_joint(self, key, x, y):
        self.joints[key].position = [x, y]


    def to_string(self):
        return NotImplementedError


class PoseNetJoint(Joint):
    keys = ['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']


    def __init__(self, confidence, name, cell, is_valid, position, id):
        super().__init__(position, id)
        self.cell = cell
        self.name = name
        self.confidence = confidence
        self.is_valid = is_valid
        self.position = position
        self.id = id


class PoseNetPose(Pose):
    joint_cls = PoseNetJoint


    def __init__(self, confidence, joints):
        super().__init__(joints)
        self.confidence = confidence


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
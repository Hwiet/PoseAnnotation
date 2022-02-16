from annotation import Annotation
from pose import PoseNetJoint, PoseNetPose
import jsonstream


class CustomFormat(Annotation):
    def write(self, poses):
        return NotImplementedError()


    def load(self):
        data = jsonstream.loads(self.fp.read())
        poses = []

        try:
            while True:
                n = next(data)
                if n == []:
                    poses.append(None)
                else:
                    poses.append(self.process_pose(n[0]))
        except StopIteration:
            return poses


    def process_pose(self, json_data):
        confidence = float(json_data['confidence'])
        joints = {}

        for x in json_data['joints']:
            if type(x) is dict:
                new_joint = PoseNetJoint(
                    cell=x['cell'],
                    is_valid=x['isValid'],
                    position=x['position'],
                    name=x['name'],
                    confidence=x['confidence'],
                    id=x['id'])

                joints[PoseNetJoint.keys[x['name']]] = new_joint

        return PoseNetPose(confidence, joints)
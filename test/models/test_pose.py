from models.pose import PoseModel

import sys
import unittest
from PyQt5.QtWidgets import QApplication
from io import StringIO
from fastjsonschema import JsonSchemaException
import jsonstream


class TestPoseModel(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.model = PoseModel()
        self.model.setScheme("schema/PoseNet_Pose.json")
        self.source = '[][][][][{"joints":[4,{"cell":{"yIndex":10,"xIndex":17},"isValid":true,"id":"5081DA54-DBEE-422F-9727-AED7D7829CD5","confidence":0.209228515625,"name":4,"position":[695.5750487329434,219.26809210526315]},12,{"cell":{"yIndex":15,"xIndex":15},"isValid":true,"id":"D9B65995-7B9C-4373-B973-A7672080BEF7","confidence":0.9072265625,"name":12,"position":[618.78167641325535,342.70833333333331]},6,{"cell":{"yIndex":11,"xIndex":16},"isValid":true,"id":"2867E36E-33D4-4EBE-ADA2-187F1B3B4853","confidence":0.5380859375,"name":6,"position":[655.16569200779725,237.72478070175438]},5,{"cell":{"yIndex":11,"xIndex":18},"isValid":true,"id":"ADE23344-B60F-4FBF-9140-F2DFEE8C1D48","confidence":0.57666015625,"name":5,"position":[707.3196881091618,243.42105263157893]},16,{"cell":{"yIndex":24,"xIndex":15},"isValid":false,"id":"EFC2132C-8AF1-45F4-9C59-9F0703366DAD","confidence":0.00383758544921875,"name":16,"position":[599.28880360623782,541.70641447368416]},14,{"cell":{"yIndex":19,"xIndex":15},"isValid":true,"id":"E3F68C02-7539-4599-AC71-826835F66F11","confidence":0.68896484375,"name":14,"position":[583.24561403508767,416.16228070175436]},0,{"cell":{"yIndex":10,"xIndex":17},"isValid":true,"id":"26F7FFBE-2BCD-43D1-9EA5-719AE9B11F57","confidence":0.364013671875,"name":0,"position":[687.59746588693952,217.45614035087718]},3,{"cell":{"yIndex":10,"xIndex":18},"isValid":true,"id":"D9403869-C930-4E0F-8018-516C9ED767E4","confidence":0.3037109375,"name":3,"position":[711.17933723196882,218.5361842105263]},9,{"cell":{"yIndex":10,"xIndex":17},"isValid":true,"id":"A482C13B-27B0-4140-B1FE-B6572A4A3C34","confidence":0.7734375,"name":9,"position":[696.79337231968805,229.01864035087718]},7,{"cell":{"yIndex":12,"xIndex":18},"isValid":true,"id":"385B48EB-D0F5-4985-8480-A31430B40897","confidence":0.8876953125,"name":7,"position":[718.70042945906425,267.08607456140351]},13,{"cell":{"yIndex":19,"xIndex":17},"isValid":true,"id":"A8440DBB-7FF1-467B-898F-1A75462A27DA","confidence":0.36474609375,"name":13,"position":[689.29824561403507,417.16008771929825]},11,{"cell":{"yIndex":15,"xIndex":17},"isValid":true,"id":"B70A4402-77E2-4D6B-A564-46BE6AC07130","confidence":0.90283203125,"name":11,"position":[660,342.87280701754383]},2,{"cell":{"yIndex":10,"xIndex":17},"isValid":true,"id":"7B3EF7A7-28D3-47DB-9142-D54775A92E58","confidence":0.2177734375,"name":2,"position":[693.00194931773876,214.75328947368419]},8,{"cell":{"yIndex":12,"xIndex":16},"isValid":true,"id":"10FE87D4-B7E0-4FEC-BA57-27B0EA031896","confidence":0.75,"name":8,"position":[620.77972709551659,264.69572368421052]},1,{"cell":{"yIndex":9,"xIndex":17},"isValid":true,"id":"52330448-CC1E-4BBA-BCC6-BEEF122AD1D4","confidence":0.2481689453125,"name":1,"position":[693.95711500974653,213.26754385964912]},15,{"cell":{"yIndex":20,"xIndex":17},"isValid":true,"id":"","confidence":0.1219482421875,"name":15,"position":[701.61793372319687,466.01973684210526]},10,{"cell":{"yIndex":11,"xIndex":17},"isValid":true,"id":"7928442B-6D21-4408-91AB-66A44AD3EB2F","confidence":0.646484375,"name":10,"position":[663.22612085769981,236.13486842105263]}],"confidence":0.50005744485294112}]'
        self.model.setUp(StringIO(self.source))

    def test_set_up_success_null(self):
        model = PoseModel()
        io = StringIO("[]")
        self.assertEqual(model.setUp(io), 1)

    def test_frame_count(self):
        self.assertEqual(self.model.frameCount(), 5)

    def test_joint_count(self):
        self.assertEqual(self.model.jointCount(), 17)

    def test_pose_count(self):
        self.assertEqual(self.model.poseCount(), 1)

    def test_next_valid_frame(self):
        self.assertEqual(self.model.nextValidFrame(), 4)

    def test_pose_data(self):
        index = self.model.pose(0)
        self.assertAlmostEqual(
            self.model.frameData(4, 'confidence', index),
            0.50005744485294112
        )

    def test_joint_data(self):
        index = self.model.joint(5, 0)
        self.assertEqual(
            self.model.frameData(4, 'id', index),
            'ADE23344-B60F-4FBF-9140-F2DFEE8C1D48'
        )
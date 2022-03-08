from views import JointGraphicsItem
from models import PoseModel

import sys
import unittest
from PyQt5.QtWidgets import QApplication
from io import StringIO
from fastjsonschema import JsonSchemaException
import jsonstream
import json


class TestJointItem(unittest.TestCase):
    def setUp(self):
        app = QApplication(sys.argv)
        self.model = PoseModel()

        with open("schema/PoseNet_Pose.json") as fp:
            scheme = json.load(fp)
            self.model.setScheme(scheme)

        with open("schema/PoseNet_Joints") as fp:
            self.model.setJointNames(fp)

        source = '[][][][{"joints":[4,{"cell":{"yIndex":8,"xIndex":18},"isValid":true,"id":"3AC34600-7947-44F1-B367-830046AD831A","confidence":0.32421875,"name":4,"position":[699.69785575048729,188.73355263157893]},12,{"cell":{"yIndex":17,"xIndex":16},"isValid":true,"id":"C251B15A-6CB3-4FEE-8D05-57E56A0FB031","confidence":0.89599609375,"name":12,"position":[629.69785575048729,372.01754385964909]},6,{"cell":{"yIndex":11,"xIndex":17},"isValid":true,"id":"F7177259-ED50-4EA0-A9C9-AD3831DD5E47","confidence":0.63818359375,"name":6,"position":[676.97733918128654,241.46381578947367]},16,{"cell":{"yIndex":27,"xIndex":16},"isValid":true,"id":"3624C269-4ED9-4CF9-AC50-9BB20F004DA1","confidence":0.56640625,"name":16,"position":[640.71150097465886,604.60389254385962]},5,{"cell":{"yIndex":11,"xIndex":17},"isValid":true,"id":"01055FB1-337F-4B04-85F6-6DCB382F2BDE","confidence":0.488525390625,"name":5,"position":[681.73732943469781,237.48903508771929]},14,{"cell":{"yIndex":22,"xIndex":16},"isValid":true,"id":"","confidence":0.9638671875,"name":14,"position":[647.68518518518511,500.31798245614033]},0,{"cell":{"yIndex":9,"xIndex":19},"isValid":true,"id":"78D48B9E-C25C-48D5-84AE-132EC8FD3F76","confidence":0.490234375,"name":0,"position":[752.28070175438597,198.17160087719296]},3,{"cell":{"yIndex":0,"xIndex":0},"isValid":false,"id":"","confidence":0,"name":3,"position":[0,0]},9,{"cell":{"yIndex":18,"xIndex":18},"isValid":true,"id":"294AAE83-CD91-43D9-AA08-E3DA3EC0BC02","confidence":0.69873046875,"name":9,"position":[728.14814814814815,413.18530701754383]},7,{"cell":{"yIndex":14,"xIndex":18},"isValid":true,"id":"4F055A39-918E-40E8-938A-B9FC60613326","confidence":0.51806640625,"name":7,"position":[712.10526315789468,321.01425438596488]},13,{"cell":{"yIndex":22,"xIndex":17},"isValid":true,"id":"35A2889A-620D-4464-B281-CDA76B13C686","confidence":0.91064453125,"name":13,"position":[678.37841130604284,499.39967105263156]},11,{"cell":{"yIndex":16,"xIndex":16},"isValid":true,"id":"16F8788C-D84C-4BCA-839E-D9F7C7E38571","confidence":0.8466796875,"name":11,"position":[645.65302144249506,368.78289473684208]},2,{"cell":{"yIndex":8,"xIndex":18},"isValid":true,"id":"8515FB1A-6D77-4D08-BBA3-B416670BF248","confidence":0.19970703125,"name":2,"position":[732.03703703703695,187.61513157894737]},8,{"cell":{"yIndex":15,"xIndex":17},"isValid":true,"id":"72A0C2C9-D9D3-4EA3-B696-2691F3E48713","confidence":0.87451171875,"name":8,"position":[697.58284600389857,326.84210526315786]},1,{"cell":{"yIndex":8,"xIndex":18},"isValid":false,"id":"FF093CF7-FA44-420B-963C-B7038E9580B3","confidence":0.03485107421875,"name":1,"position":[727.73391812865498,185.47697368421052]},15,{"cell":{"yIndex":27,"xIndex":16},"isValid":true,"id":"AB34F156-A905-4642-A1DD-D2AEEAA0BB08","confidence":0.72412109375,"name":15,"position":[639.08503898635479,601.51041666666663]},10,{"cell":{"yIndex":19,"xIndex":18},"isValid":true,"id":"69D33961-5F25-4105-B8A5-E9CBE03FE794","confidence":0.86181640625,"name":10,"position":[727.99707602339174,416.0361842105263]}],"confidence":0.58833582261029416}][][{"joints":[4,{"cell":{"yIndex":10,"xIndex":17},"isValid":true,"id":"5081DA54-DBEE-422F-9727-AED7D7829CD5","confidence":0.209228515625,"name":4,"position":[695.5750487329434,219.26809210526315]},12,{"cell":{"yIndex":15,"xIndex":15},"isValid":true,"id":"D9B65995-7B9C-4373-B973-A7672080BEF7","confidence":0.9072265625,"name":12,"position":[618.78167641325535,342.70833333333331]},6,{"cell":{"yIndex":11,"xIndex":16},"isValid":true,"id":"2867E36E-33D4-4EBE-ADA2-187F1B3B4853","confidence":0.5380859375,"name":6,"position":[655.16569200779725,237.72478070175438]},5,{"cell":{"yIndex":11,"xIndex":18},"isValid":true,"id":"ADE23344-B60F-4FBF-9140-F2DFEE8C1D48","confidence":0.57666015625,"name":5,"position":[707.3196881091618,243.42105263157893]},16,{"cell":{"yIndex":24,"xIndex":15},"isValid":false,"id":"EFC2132C-8AF1-45F4-9C59-9F0703366DAD","confidence":0.00383758544921875,"name":16,"position":[599.28880360623782,541.70641447368416]},14,{"cell":{"yIndex":19,"xIndex":15},"isValid":true,"id":"E3F68C02-7539-4599-AC71-826835F66F11","confidence":0.68896484375,"name":14,"position":[583.24561403508767,416.16228070175436]},0,{"cell":{"yIndex":10,"xIndex":17},"isValid":true,"id":"26F7FFBE-2BCD-43D1-9EA5-719AE9B11F57","confidence":0.364013671875,"name":0,"position":[687.59746588693952,217.45614035087718]},3,{"cell":{"yIndex":10,"xIndex":18},"isValid":true,"id":"D9403869-C930-4E0F-8018-516C9ED767E4","confidence":0.3037109375,"name":3,"position":[711.17933723196882,218.5361842105263]},9,{"cell":{"yIndex":10,"xIndex":17},"isValid":true,"id":"A482C13B-27B0-4140-B1FE-B6572A4A3C34","confidence":0.7734375,"name":9,"position":[696.79337231968805,229.01864035087718]},7,{"cell":{"yIndex":12,"xIndex":18},"isValid":true,"id":"385B48EB-D0F5-4985-8480-A31430B40897","confidence":0.8876953125,"name":7,"position":[718.70042945906425,267.08607456140351]},13,{"cell":{"yIndex":19,"xIndex":17},"isValid":true,"id":"A8440DBB-7FF1-467B-898F-1A75462A27DA","confidence":0.36474609375,"name":13,"position":[689.29824561403507,417.16008771929825]},11,{"cell":{"yIndex":15,"xIndex":17},"isValid":true,"id":"B70A4402-77E2-4D6B-A564-46BE6AC07130","confidence":0.90283203125,"name":11,"position":[660,342.87280701754383]},2,{"cell":{"yIndex":10,"xIndex":17},"isValid":true,"id":"7B3EF7A7-28D3-47DB-9142-D54775A92E58","confidence":0.2177734375,"name":2,"position":[693.00194931773876,214.75328947368419]},8,{"cell":{"yIndex":12,"xIndex":16},"isValid":true,"id":"10FE87D4-B7E0-4FEC-BA57-27B0EA031896","confidence":0.75,"name":8,"position":[620.77972709551659,264.69572368421052]},1,{"cell":{"yIndex":9,"xIndex":17},"isValid":true,"id":"52330448-CC1E-4BBA-BCC6-BEEF122AD1D4","confidence":0.2481689453125,"name":1,"position":[693.95711500974653,213.26754385964912]},15,{"cell":{"yIndex":20,"xIndex":17},"isValid":true,"id":"","confidence":0.1219482421875,"name":15,"position":[701.61793372319687,466.01973684210526]},10,{"cell":{"yIndex":11,"xIndex":17},"isValid":true,"id":"7928442B-6D21-4408-91AB-66A44AD3EB2F","confidence":0.646484375,"name":10,"position":[663.22612085769981,236.13486842105263]}],"confidence":0.50005744485294112}]'
        self.model.setUp(StringIO(source))
        index = self.model.joint(4, 0)
        self.item = JointGraphicsItem(index)

    def test_name(self):
        self.assertEqual(self.item.label(), 'right_ear')

    def test_index(self):
        self.assertEqual(self.item.index(), 4)

    def test_load_pos(self):
        self.assertAlmostEqual(self.item.loadPos(3), [699.69785575048729,188.73355263157893])

    def test_set_pos(self):
        self.assertTrue(self.item.setPos([100, 200], 0))
        self.assertAlmostEqual(
            [100, 200],
            self.item.loadPos(0)
        )
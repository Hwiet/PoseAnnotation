import python_jsonschema_objects as pjs
import jsonstream
import json
import logging
logging.basicConfig(level=logging.DEBUG, filename="log.txt", filemode='w')

with open("supported_models/PoseNet/schema.json") as fp:
    builder = pjs.ObjectBuilder(json.load(fp))
ns = builder.build_classes()
Klass = ns.PosenetPose

with open('test/fixtures/annotation1-1.txt') as fp:
    it = jsonstream.load(fp)
    while True:
        poses = next(it)
        if poses != []:
            k = Klass(**poses[0])
            k.joints.joint
            break

import unittest
from entities.pose import BaseData, Pose
import fastjsonschema
from fastjsonschema import JsonSchemaException
from functools import partial

class TestPose(unittest.TestCase):
    def setUp(self):
        """Note that the top level of the schema should have a
        'raequired' attribute, or else it will say that an empty object
        is valid."""
        self.validate_nested = fastjsonschema.compile({
            "type": "object",
            "properties": {
                "joints": {
                    "type": "array",
                    "items": { "$ref": "#/$defs/joint" }
                },
                "confidence": { "type": "number" }
            },
            "required": [ "joints", "confidence" ],
            "$defs": {
                "joint": {
                    "type": "object",
                    "properties": {
                        "name": { "type": "integer" },
                        "position": { "type": "array", "items": { "type": "number" }, "minItems": 2 }
                    },
                    "required": [ "name", "position" ]
                }
            }
        })

    def test_create_success(self):
        pose = Pose({ # wrap object in a list
            "joints": [
                { "name": 1, "position": [ 0, 0 ] },
                { "name": 2, "position": [ 0, 1 ] },
            ],
            "confidence": 0.1
        }, self.validate_nested)

    def test_create_fail(self):
        fixture_data = [
            {
                "joints": [
                    {
                        "name": "1", # not an integer
                        "position": [ 0, 2 ]
                    }
                ],
                "confidence": 0.1
            }
        ]

        for f in fixture_data:
            with self.assertRaises(JsonSchemaException):
                self.pose = Pose(f, self.validate_nested)
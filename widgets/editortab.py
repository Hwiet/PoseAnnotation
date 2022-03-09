from PyQt5.QtCore import (
    pyqtSlot
)

from PyQt5.QtWidgets import (
    QTabWidget
)

from models import (
    PoseModel
)

from graphics import (
    PoseView,
    Controller
)

from multimedia import (
    MediaPlayer
)

import json

class EditorTab:
    MODELS_PATH = 'supported_models/'
    CONSTANT_FILE = 'constants.json'
    SCHEMA_FILE = 'schema.json'

    def __init__(self, file, poseModel):
        """Editor tab.

        Args:
            file (_type_): _description_
            poseModel (str): name of the pose model.
        """
        # Get constants

        with open(f'{MODELS_PATH}{poseModel}/{CONSTANT_FILE}') as fp:
            doc = json.load(fp)
            keypoints = doc['keypoints']
            chain = doc['pose_chain']

        self.model = PoseModel()
        self.poseview = PoseView(model, keypoints, chain)

        self.player = MediaPlayer(file)
        self.player.setVideoOutput(poseview.videoItem())
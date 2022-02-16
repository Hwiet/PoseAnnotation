from re import X
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# from PyQt5.QtCore import QDir, Qt, QUrl
from pose import Joint
from annotated_media import AnnotatedVideo, AnnotatedImage
from typing import List


class PoseEditor():
    def __init__(self, media) -> QWidget:
        return NotImplementedError()


    def get_widget(self):
        return self.widget


    @property
    def poses(self):
        return self.media.poses

    
    def update_joint(self):
        pass


    def zoom():
        return NotImplementedError()


    def pan():
        return NotImplementedError()


    def overwrite():
        self.new_annotation.write()


class VideoPoseEditor(PoseEditor):
    def __init__(self, media: AnnotatedVideo):
        self.current_frame = 0
        self.widget = PoseWidget(QDir.current().absoluteFilePath(media.filename), media.poses)


    @property
    def current_pose(self):
        try:
            return media.keyframes.index(self.current_frame)
        except ValueError:
            return None

    
    def prev_keyframe(self):
        return NotImplementedError()


    def next_keyframe(self):
        return NotImplementedError()


    def play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()


    def pause(self):
        return NotImplementedError()


    def to_frame(self, n):
        return NotImplementedError()


class ImagePoseEditor(PoseEditor):
    def __init__(self, media: AnnotatedImage):
        super().__init__(media)

class makeLines(QGraphicsView):
    def __init__(self, poses):
        self.scene = self.scene = QGraphicsScene()
        self.poses = poses
        self.drawLines()
    def lineDrawer(self, x1, y1, x2, y2):
        self.scene.addLine(x1, y1, x2, y2)
    def drawLines(self):
        pose = self.poses[0]
        for joint_name in pose.joint_cls.keys:#Theese first three lines are unessecary, unsure better way for now.
            pass
        #ankle to ankle    
        self.lineDrawer(*pose.joints['right_ankle'].position, *pose.joints['right_knee'].position)
        self.lineDrawer(*pose.joints['right_knee'].position, *pose.joints['right_hip'].position)
        self.lineDrawer(*pose.joints['right_hip'].position, *pose.joints['right_shoulder'].position)
        self.lineDrawer(*pose.joints['right_shoulder'].position, *pose.joints['right_ear'].position)
        self.lineDrawer(*pose.joints['right_ear'].position, *pose.joints['right_eye'].position)
        self.lineDrawer(*pose.joints['nose'].position, *pose.joints['left_eye'].position)
        self.lineDrawer(*pose.joints['left_eye'].position, *pose.joints['left_ear'].position)
        self.lineDrawer(*pose.joints['left_ear'].position, *pose.joints['left_shoulder'].position)
        self.lineDrawer(*pose.joints['left_shoulder'].position, *pose.joints['left_hip'].position)
        self.lineDrawer(*pose.joints['left_hip'].position, *pose.joints['left_knee'].position)
        self.lineDrawer(*pose.joints['left_hip'].position, *pose.joints['left_ankle'].position)
        #shoulders to wrists
        self.lineDrawer(*pose.joints['right_shoulder'].position, *pose.joints['right_elbow'].position)
        self.lineDrawer(*pose.joints['right_elbow'].position, *pose.joints['right_wrist'].position)
        self.lineDrawer(*pose.joints['left_shoulder'].position, *pose.joints['left_elbow'].position)
        self.lineDrawer(*pose.joints['left_elbow'].position, *pose.joints['left_wrist'].position)
        #connecting hips and soulders
        self.lineDrawer(*pose.joints['right_shoulder'].position, *pose.joints['left_shoulder'].position)
        self.lineDrawer(*pose.joints['right_hip'].position, *pose.joints['left_hip'].position)
class PoseWidget(QGraphicsView):
    def __init__(self, file, poses):
        super().__init__()
        self.poses = poses
        self.scene = QGraphicsScene()
        self.display = QVideoWidget()
        self.player = QMediaPlayer()

    def setUpScene(self):
        point_brush = QBrush(Qt.green, Qt.SolidPattern)
        point_size = 10
        pose = self.poses[0]
        self.points:List[JointWidget] = []
        makeLines(self.poses)
        self.scene.addWidget(self.display)
        self.player.setVideoOutput(self.display)
        self.player.setMedia(QMediaContent(QUrl(file)))

        self.player.setPosition(0)
        self.player.pause()

        # add joints
        point_size = 10
        pose = self.poses[0]
        self.points:List[JointWidget] = []
        for joint_name in pose.joint_cls.keys:
            point = JointWidget(*pose.joints[joint_name].position, point_size, point_size)
            self.points.append(point)
            self.scene.addItem(point)

        self.setScene(self.scene)

<<<<<<< Updated upstream
    def resizeEvent(self, event):
        self.fitInView(QRectF(self.display.rect()))
=======

    # def resizeEvent(self, event):
    #     self.fitInView(QRectF(self.display.rect()))
>>>>>>> Stashed changes
     

class JointWidget(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.funcs = []

    def registerCallback(self, func):
        self.funcs.append(func)


    def mouseMoveEvent(self, event):
        self.setPos(event.pos())
        for f in self.funcs: f(event.pos())


    def mousePressEvent(self, event):
        pass
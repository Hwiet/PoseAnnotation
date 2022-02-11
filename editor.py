from re import X
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pose import Joint
from annotated_media import AnnotatedVideo, AnnotatedImage
from typing import List


class PoseEditor():
    def __init__(self, media):
        self.media = media
        self.widget = PoseWidget(media.filename, media.poses)
        self.widget.show()


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
        super().__init__(media)
        self.current_frame = 0


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
        return NotImplementedError()


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
        self.scene = QGraphicsScene()
        self.image = self.scene.addPixmap(QPixmap(file))
        self.poses = poses
        self.setUpScene()
        self.setScene(self.scene)

    def setUpScene(self):
        point_brush = QBrush(Qt.green, Qt.SolidPattern)
        point_size = 10
        pose = self.poses[0]
        self.points:List[JointWidget] = []
        makeLines(self.poses)
        for joint_name in pose.joint_cls.keys:
            point = JointWidget(*pose.joints[joint_name].position, point_size, point_size)
            self.scene.addItem(point)
            self.points.append(point)

    def resizeEvent(self, event):
        self.fitInView(self.image, Qt.KeepAspectRatioByExpanding)
     

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
from collections import namedtuple
from annotation import Annotation
from custom_annotation import CustomFormat


"""
Class for encapsulating data about some image or video
"""
class AnnotatedMedia:
    def __init__(self, filename, annotation):
        self.annotation = annotation
        self.filename = filename
        self.poses = self.annotation.load()


    def write(self):
        """Write to annotation on disk"""
        raise NotImplementedError


    def load(self):
        """Load from annotation on disk"""
        raise NotImplementedError


class AnnotatedVideo(AnnotatedMedia):
    def __init__(self, filename, annotation, keyframes):
        self.keyframes = keyframes
        super().__init__(annotation, media_filename)


class AnnotatedImage(AnnotatedMedia):
    pass
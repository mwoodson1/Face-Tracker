import cv2
import rects
import utils


class Face(object):
    """Data on facial features such as eyes, nose and mouth"""

    def __init__(self):
        """A face will be composed of rectangles around important features"""
        self.faceRect = None;
        self.leftEyeRect = None;
        self.rightEyeRect = None;
        self.noseRect = None;
        self.mouthRect = None;

class FaceTracker(object):
    """A tracker for facial features"""

    def __init__(self,scaleFactor=1.2,minNeighbors=2,flags=cv2.cv.CV_HAAR_SCALE_IMAGE):
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.flags = flags

        self._faces = []

        self._faceClassifier = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')
        self._eyeClassifier = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
        self._mouthClassifier = cv2.CascadeClassifier('cascades/haarcascade_mcs_mouth.xml')
        self._noseClassifier = cv2.CascadeClassifier('cascades/haarcascade_mcs_nose.xml')

    @property
    def faces(self):
        """The tracked features"""
        return self._faces

    def update(self,image):
        """Update tracked features"""
        #TODO Track features
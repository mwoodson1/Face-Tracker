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

        self._faces = []

        if utils.isGray(image):
            image = cv2.equalizeHist(image)
        else:
            image = cv2.cvtColor(image,cv2.cv.CV_BGR2GRAY)
            cv2.equalizeHist(image,image)

        minSize = utils.widthHeightDivideBy(image,8)

        faceRects = self._faceClassifier.detectMultiScale(image,self.scaleFactor,self.minNeighbors,self.flags,
                                                          minSize)

        if faceRects is not None:
            for faceRect in faceRects:
                face = Face()
                face.faceRect = faceRect

                x,y,w,h = faceRect

                #Look for an eye
                searchRect = (x+w/7,y,w*2/7,h/2)
                face.leftEyeRect = self._detectOneObject(self._eyeClassifier,image,searchRect,64)

                #Look for other eye
                searchRect = (x+w*4/7,y,w*2/7,h/2)
                face.rightEyeRect = self._detectOneObject(self._eyeClassifier,image,searchRect,64)

                #Look for nose
                searchRect = (x+w/4,y+h/4,w/2,h/2)
                face.noseRect = self._detectOneObject(self._noseClassifier,image,searchRect,32)

                #Look for mouth
                searchRect = (x+w/6,y+h*2/3,w*2/3,h/3)
                face.mouthRect = self._detectOneObject(self._mouthClassifier,image,searchRect,16)

                self._faces.append(face)

    def _detectOneObject(self,classifier,image,rect,imageSizeToMinRatio):
        x,y,w,h = rect

        minSize = utils.widthHeightDivideBy(image,imageSizeToMinRatio)

        subImage = image[y:y+h,x:x+w]

        subRects = classifier.detectMultiScale(subImage,self.scaleFactor,self.minNeighbors,self.flags,minSize)

        if(len(subRects) == 0):
            return None

        subX,subY,subW,subH = subRects[0]
        return(x+subX,y+subY,subW,subH)

    def drawDebugRects(self,image):
        """Draw rectangles around the teacked facial features"""
        if utils.isGray(image):
            faceColor = 255
            leftEyeColor = 255
            rightEyeColor = 255
            noseColor = 255
            mouthColor = 255
        else:
            faceColor = (255,255,255)
            leftEyeColor = (0,0,255)
            rightEyeColor = (0,255,0)
            noseColor = (255,0,0)
            mouthColor = (255,255,0)

        for face in self.faces:
            rects.outlineRect(image,face.faceRect,faceColor)
            rects.outlineRect(image,face.leftEyeRect,leftEyeColor)
            rects.outlineRect(image,face.rightEyeRect,rightEyeColor)
            rects.outlineRect(image,face.noseRect,noseColor)
            rects.outlineRect(image,face.mouthRect,mouthColor)
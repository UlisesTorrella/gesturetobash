import pdb
from gestures.MovingGesture import MovingGesture
import inspect
import gestures


class GestureDetector:
    gestures = [c[1] for c in inspect.getmembers(gestures, inspect.isclass)]
    
    moving_gesture_flag = "$$ MOVING GESTURE $$"


    def findGesture(self, sample, imgH, imgW):
        g, c = None, None
        for gesture in self.gestures:
            if gesture().match(sample, imgH, imgW):
                if issubclass(gesture, MovingGesture):
                    return gesture, self.moving_gesture_flag
                else:
                    g, c = gesture, gesture.command
        return g, c
    
    def isGesture(self, gesture, sample, imgH, imgW, end=False):
        if gesture().match(sample, imgH, imgW, end):
            return True
        return False
        
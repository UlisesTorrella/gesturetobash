import inspect
import gestures


class GestureDetector:
    gestures = [c[1] for c in inspect.getmembers(gestures, inspect.isclass)]
    
    def findGesture(self, sample, imgH, imgW):
        for gesture in self.gestures:
            if gesture().match(sample, imgH, imgW):
                return gesture, gesture.command
        return None, None
        
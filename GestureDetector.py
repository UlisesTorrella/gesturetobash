
from gestures.fingergun import FingerGun


class GestureDetector:
    gestures = [FingerGun]

    def findGesture(self, sample, imgH, imgW):
        for gesture in self.gestures:
            if gesture().match(sample, imgH, imgW):
                return gesture
        return None
        

from gestures.ok import ok
from gestures.fingergun import FingerGun


class GestureDetector:
    gestures = [FingerGun, ok]

    commands ={
        FingerGun: "brave-browser",
        ok: "gedit"
    }

    def findGesture(self, sample, imgH, imgW):
        for gesture in self.gestures:
            if gesture().match(sample, imgH, imgW):
                return gesture, self.commands[gesture]
        return None, None
        
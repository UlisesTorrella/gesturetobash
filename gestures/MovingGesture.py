from gestures.Gesture import Gesture
import numpy as np

import pdb

class MovingGesture(Gesture):

    track = []

    displacement = {}



    xs = []
    ys = []
    zs = []
  
    end_xs = []
    end_ys = []
    end_zs = []
   
    command = "git status"

    def match_movement(self, tol, mov_tol, candidate_track, displacement):
        '''
        From a given track returns a match given a tolerance with the defined track
        this tolerance is compared to the mse between each function/track. 
        There are 3 functions to compare, x y and z for each 21 landmarks
        '''
        candidate_track = self.movements_to_candidate(candidate_track)
        msed = {
            'x': [],
            'y': [],
            'z': []
        }
        for i in range(21):
            for axis in msed.keys():
                n = len(self.track[i][axis])
                m = len(candidate_track[i][axis])
                x = [i/m for i in range(1, m+1)] # entre 0 y 1
                xp = [i/n for i in range(1, n+1)] 
                fp = self.track[i][axis]
                reference = np.interp(x=x, xp=xp, fp=fp)
                candidate = np.array(candidate_track[i][axis])
                # pdb.set_trace()
                mse = ((reference - candidate)**2).mean()
                msed[axis].append(mse)

        # Displacement
        displacement_error = {
            'x': 0,
            'y': 0,
            'z': 0
        }
        for axis in displacement_error.keys():
            n = len(self.displacement[axis])
            m = len(displacement[axis])
            x = [i/m for i in range(1, m+1)] # entre 0 y 1
            xp = [i/n for i in range(1, n+1)] 
            fp = self.displacement[axis]
            reference = np.interp(x=x, xp=xp, fp=fp)
            candidate = np.array(displacement[axis])
            # pdb.set_trace()
            mse = ((reference - candidate)**2).mean()
            # print(f"{axis}")
            # print(self.displacement[axis])
            # print(displacement[axis])
            # print(mse)
            if mse>mov_tol:
                print(f"{axis} : {mse}")
                return False

        return self.command


    def movements_to_candidate(self, movements):
        '''
        Takes a list of hands [[{x:,y:,z:}, ...] ...] 
        and returns a list of 21 items tracking each landmark:
        [{x:[...], y: [...], z: [...]} ... 21]
        '''
        landmark_track = []
        for i in range(21):
            xs, ys, zs = [], [], []
            for moment in movements:
                xs.append(moment['x'][i])
                ys.append(moment['y'][i])
                zs.append(moment['z'][i])
            landmark_track.append({
                'x': xs,
                'y': ys,
                'z': zs
            })
        # pdb.set_trace()
        return landmark_track

            
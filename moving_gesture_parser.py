import pdb
import cv2
import mediapipe as mp
from collections import deque
import sys
from countdown import countdown
  
from landmarks_utils import average_landmarks, compare_landmarks, scale_landmarks, is_same_gesture

if len(sys.argv)<3:
  print("You need to tellme the name of the gesture and the bash command to run")
  exit()

print("\033[92mHold your gesture until the process ends\033[0m")

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

last5 = deque(maxlen=5)
start_gesture_landmarks = []
# For webcam input:
cap = cv2.VideoCapture(0)

store_movement = False
movement = []
displacement = []

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    imgH, imgW, imgC = image.shape 
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      hand = results.multi_hand_landmarks[0]
      mp_drawing.draw_landmarks(
          image, hand, mp_hands.HAND_CONNECTIONS)
          
      landmarks = []
      for land_mark in hand.landmark:
        xPos, yPos, z = int(land_mark.x * imgW), int(land_mark.y * imgH), land_mark.z
        landmarks.append({'x': xPos, 'y': yPos, 'z': z})
      if len(last5)>1:
        cx, cy, cz = compare_landmarks(a=average_landmarks(last5), b=landmarks)
        if cx<1 and cy<1 and cz<0.5:
          
          if store_movement: 
            if not is_same_gesture(a=start_gesture_landmarks, b=landmarks):
              end_gesture_landmarks = landmarks
              break
          else:
            print("When the countdown ends start the movement")
            countdown(5)
            start_gesture_landmarks = landmarks
            store_movement = True
      last5.append(landmarks)
      if store_movement:
        movement.append(landmarks)
        displacement.append({
          'x': landmarks[0]['x'] / imgW,
          'y': landmarks[0]['y'] / imgH,
          'z': landmarks[0]['z']
        })
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

print(len(movement))

hands_in_time = [start_gesture_landmarks] + movement + [end_gesture_landmarks]
landmarks_in_time = []

for landmarks in hands_in_time:
  xs, ys, zs = [], [], []
  for mark in landmarks:
    xs.append(mark['x'])
    ys.append(mark['y'])
    zs.append(mark['z'])
  minx = min(xs)
  maxx = max(xs) - minx
  xs = [(x - minx)/maxx for x in xs]
  miny = min(ys)
  maxy = max(ys) - miny
  ys = [(y - miny)/maxy for y in ys]
  # minz = min(zs)
  # maxz = max(zs) - minz
  # zs = [(z - minz)/maxz for z in zs]
  landmarks_in_time.append({
    'x': xs,
    'y': ys,
    'z': zs
  })
  
# each entry tracks the movement of one landmark
landmark_track = []
for i in range(21):
  xs, ys, zs = [], [], []
  for moment in landmarks_in_time:
    xs.append(moment['x'][i])
    ys.append(moment['y'][i])
    zs.append(moment['z'][i])
  landmark_track.append({
    'x': xs,
    'y': ys,
    'z': zs
  })


# # You can query the movement in the x axis though time of the tip of  the thum like this
# print(landmark_track[4]['x'])


xs, ys, zs = [], [], []
for moment in displacement:
  xs.append(moment['x'])
  ys.append(moment['y'])
  zs.append(moment['z'])

minx = min(xs)
xs = [x-minx for x in xs]
miny = min(ys)
ys = [y-miny for y in ys]

displacement_track = {
    'x': xs,
    'y': ys,
    'z': zs
  }


start_scaled = scale_landmarks(start_gesture_landmarks)
end_scaled = scale_landmarks(end_gesture_landmarks)

_, name, *command = sys.argv

print("writing file...")
file = open(f"gestures/{name}.py", 'w')
file.write(
  f'''
from gestures.MovingGesture import MovingGesture
import numpy as np

class {name}(MovingGesture):
  command = {command}

  track = {landmark_track}

  displacement = {displacement_track}

  xs = {start_scaled['x']}
  ys = {start_scaled['y']}
  zs = {start_scaled['z']}

  end_xs = {end_scaled['x']}
  end_ys = {end_scaled['y']}
  end_zs = {end_scaled['z']}
  '''
)
file.close()


initfile = open(f"gestures/__init__.py", 'a')
initfile.write(f"\nfrom .{name} import {name} ")

print("Go try it runnign \033[92m python main.py \033[0m")


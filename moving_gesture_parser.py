import cv2
import mediapipe as mp
from collections import deque
import sys
from countdown import countdown
  
from landmarks_utils import average_landmarks, compare_landmarks

# if len(sys.argv)<3:
#   print("You need to tellme the name of the gesture and the bash command to run")
#   exit()

print("\033[92mHold your gesture until the process ends\033[0m")

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

last5 = deque(maxlen=5)
gesture_landmarks = []
# For webcam input:
cap = cv2.VideoCapture(0)

store_movement = False
movement = []

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
          print("Start recording movement until next stop:")
          if store_movement:
            end_gesture_landmarks = landmarks
            break
          print("When the countdown ends start the movement")
          countdown(5)
          gesture_landmarks = landmarks
          store_movement = True
      last5.append(landmarks)
      if store_movement:
        movement.append(landmarks)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

print(len(movement))

hands_in_time = [gesture_landmarks] + movement + [end_gesture_landmarks]
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

print("Go try it runnign \033[92m python main.py \033[0m")


print(landmark_track)
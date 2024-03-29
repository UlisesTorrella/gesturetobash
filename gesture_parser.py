import cv2
import mediapipe as mp
from collections import deque
import sys

from landmarks_utils import average_landmarks, compare_landmarks, scale_landmarks

if len(sys.argv)<3:
  print("You need to tellme the name of the gesture and the bash command to run")
  exit()

print("\033[92mHold your gesture until the process ends\033[0m")

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

last5 = deque(maxlen=5)
gesture_landmarks = []
# For webcam input:
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    imgH, imgW, imgC = image.shape 
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
    # Draw the hand annotations on the image.
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
          gesture_landmarks = landmarks
          break
      last5.append(landmarks)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

print("This are the landmarks of the scanned gesture")
print(gesture_landmarks)


scale_landmarks = scale_landmarks(gesture_landmarks)


_, name, *command = sys.argv

print("writing file...")
file = open(f"gestures/{name}.py", 'w')
file.write(
  f'''
from gestures.Gesture import Gesture


class {name}(Gesture):
  command = {command}

  xs = {scale_landmarks['x']}
  ys = {scale_landmarks['y']}
  zs = {scale_landmarks['z']}
  '''
)
file.close()

initfile = open(f"gestures/__init__.py", 'a')
initfile.write(f"\nfrom .{name} import {name} ")

print("Go try it runnign \033[92m python main.py \033[0m")
import gestures
from GestureDetector import GestureDetector
import cv2
import mediapipe as mp
import subprocess
import os
from landmarks_utils import scale_landmarks

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

skip = 0 # used to skip frames after a gesture is executed

detector = GestureDetector()
record_movement = False
movements = []
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
      continue
    if skip>0:
      skip -= 1
    else: 
      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
      imgH, imgW, imgC = image.shape 
      image.flags.writeable = False
      results = hands.process(image)
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      if results.multi_hand_landmarks:
        if record_movement:
          hand = results.multi_hand_landmarks[0]
          landmarks = []
          for land_mark in hand.landmark:
            xPos, yPos, z = int(land_mark.x * imgW), int(land_mark.y * imgH), land_mark.z
            landmarks.append({'x': xPos, 'y': yPos, 'z': z})
          landmarks = scale_landmarks(landmarks)
          movements.append(landmarks)
          if detector.isGesture(end_gesture, results.multi_hand_landmarks[0], imgH, imgW, True):
            record_movement = False
            if gesture().match_movement(0.05, movements):
              print("ESE SI")
            print(len(movements))
            movements = []
        else:
          gesture, command = detector.findGesture(results.multi_hand_landmarks[0], imgH, imgW)
          if gesture:
            if (command==GestureDetector.moving_gesture_flag):
              record_movement = True
              end_gesture = gesture
            else:
              pid = os.fork()
              if pid > 0:
                process = subprocess.Popen(command)
                output, error = process.communicate()
                exit              
              skip = 10

        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      cv2.imshow('MediaPipe Hands', image)
      if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()

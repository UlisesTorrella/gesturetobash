import pdb
import gestures
from GestureDetector import GestureDetector
import cv2
import mediapipe as mp
import subprocess
import os
from landmarks_utils import scale_landmarks
from collections import defaultdict 

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

skip = 0 # used to skip frames after a gesture is executed

detector = GestureDetector()
record_movement = False
movements = []
displacement = defaultdict(list)
movement_timer = 0

def fork_it():
  subprocess.call(command)        

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
    if record_movement:
      movement_timer+=1
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
          if movement_timer>50:
            print("timer expired")
            movement_timer = 0
            record_movement = False
            movements = []
            displacement = defaultdict(list)
          hand = results.multi_hand_landmarks[0]
          landmarks = []
          for land_mark in hand.landmark:
            xPos, yPos, z = int(land_mark.x * imgW), int(land_mark.y * imgH), land_mark.z
            landmarks.append({'x': xPos, 'y': yPos, 'z': z})
          displacement['x'].append(landmarks[0]['x']/imgW)
          displacement['y'].append(landmarks[0]['y']/imgH)
          displacement['z'].append(landmarks[0]['z'])
          landmarks = scale_landmarks(landmarks)
          movements.append(landmarks)
          if detector.isGesture(end_gesture, results.multi_hand_landmarks[0], imgH, imgW, True):
            record_movement = False
            minx = min(displacement['x'])
            displacement['x'] = [x-minx for x in displacement['x']]
            miny = min(displacement['y'])
            displacement['y'] = [y-miny for y in displacement['y']]
            command = gesture().match_movement(0.05, 0.05, movements, displacement)
            if command:
              fork_it()
            print(len(movements))
            movements = []
            displacement = defaultdict(list)
        else:
          gesture, command = detector.findGesture(results.multi_hand_landmarks[0], imgH, imgW)
          if gesture:
            if (command==GestureDetector.moving_gesture_flag):
              record_movement = True
              end_gesture = gesture
            else:
              fork_it()
              skip = 10


        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      cv2.imshow('MediaPipe Hands', image)
      if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()

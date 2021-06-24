from GestureDetector import GestureDetector
import cv2
import mediapipe as mp
import subprocess
import os

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

skip = 0 # used to skip frames after a gesture is executed

detector = GestureDetector()
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
        gesture, command = detector.findGesture(results.multi_hand_landmarks[0], imgH, imgW)
        if gesture:
          print(gesture.__name__)
          
          pid = os.fork()
          if pid > 0:
            process = subprocess.Popen(command.split())
            output, error = process.communicate()
            exit              
          skip = 10
          # break
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      cv2.imshow('MediaPipe Hands', image)
      if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()

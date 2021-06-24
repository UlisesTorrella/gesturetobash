import cv2
import mediapipe as mp
from collections import deque
import sys

if len(sys.argv)<3:
  print("You need to tellme the name of the gesture and the bash command to run")
  exit()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

last5 = deque(maxlen=5)
gesture_landmarks = []
# For webcam input:
cap = cv2.VideoCapture(0)

def average_landmarks(hands):
  result = []
  if len(hands)>1:
    for i in range(21):
      xs = [landmarks[i]['x'] for landmarks in hands]
      ys = [landmarks[i]['y'] for landmarks in hands]
      zs = [landmarks[i]['z'] for landmarks in hands]
      result.append({
        'x': sum(xs)/len(xs),
        'y': sum(ys)/len(ys),
        'z': sum(zs)/len(zs)
      })
  return result
  
  

def compare_landmarks(a, b):
  xs, ys, zs = [], [], []
  # pdb.set_trace()
  for i in range(21):
    xs.append((a[i]['x'] - b[i]['x'])**2)
    ys.append((a[i]['y'] - b[i]['y'])**2)
    zs.append((a[i]['z'] - b[i]['z'])**2)
  return sum(xs)/21, sum(ys)/21, sum(zs)/21

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
      # print(results.multi_hand_landmarks)
      # pdb.set_trace( )
      hand = results.multi_hand_landmarks[0]
      mp_drawing.draw_landmarks(
          image, hand, mp_hands.HAND_CONNECTIONS)
      landmarks = []
      for land_mark in hand.landmark:
        xPos, yPos, z = int(land_mark.x * imgW), int(land_mark.y * imgH), land_mark.z
        landmarks.append({'x': xPos, 'y': yPos, 'z': z})
      if len(last5)>1:
        cx, cy, cz = compare_landmarks(a=average_landmarks(last5), b=landmarks)
        print(cx, cy, cz)
        if cx<1 and cy<1 and cz<0.5:
          gesture_landmarks = landmarks
          print(imgH, imgW, imgC)
          break
      last5.append(landmarks)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

print("This are the landmarks of the scanned gesture")
print(gesture_landmarks)

# I will flatten it on the x,y and z axis
xs, ys, zs = [], [], []
for mark in gesture_landmarks:
  xs.append(mark['x'])
  ys.append(mark['y'])
  zs.append(mark['z'])

# And take them to the origin, except z
minx = min(xs)
xs = [x - minx for x in xs]
miny = min(ys)
ys = [y - miny for y in ys]

# Now the biggest value of each list is the hand scale
maxx = max(xs)
xs = [x/maxx for x in xs]
maxy = max(ys)
ys = [y/maxy for y in ys]

print("This is our compressed gesture")
print(xs, ys, zs)

_, name, *command = sys.argv

print("writing file...")
file = open(f"gestures/{name}.py", 'w')
file.write(
  f'''
from gestures.Gesture import Gesture


class {name}(Gesture):
  command = {command}

  xs = {xs}
  ys = {ys}
  zs = {zs}
  '''
)
file.close()

initfile = open(f"gestures/__init__.py", 'a')
initfile.write(f"\nfrom .{name} import {name} ")
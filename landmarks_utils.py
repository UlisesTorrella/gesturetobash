
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


def scale_landmarks(landmarks):
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
  return {
    'x': xs,
    'y': ys,
    'z': zs
  }
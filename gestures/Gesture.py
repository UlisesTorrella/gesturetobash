import pdb

class Gesture():
  xs, ys, zs = [], [], []
  
  def match(self, sample, imgH, imgW, end=False):
    landmarks = []
    for land_mark in sample.landmark:
        xPos, yPos, z = int(land_mark.x * imgW), int(land_mark.y * imgH), land_mark.z
        landmarks.append({'x': xPos, 'y': yPos, 'z': z})
    # I will flatten it on the x,y and z axis
    xs, ys, zs = [], [], []
    for mark in landmarks:
      xs.append(mark['x'])
      ys.append(mark['y'])
      zs.append(mark['z'])
    minx = min(xs)
    xs = [x - minx for x in xs]
    miny = min(ys)
    ys = [y - miny for y in ys]

    # Now the biggest value of each list is the hand scale
    maxx = max(xs)
    xs = [x/maxx for x in xs]
    maxy = max(ys)
    ys = [y/maxy for y in ys]
    # pdb.set_trace()

    diffxs, diffys, diffzs = [], [], []

    if end:
      for i in range(21):
        diffxs.append((self.end_xs[i] - xs[i])**2)
        diffys.append((self.end_ys[i] - ys[i])**2)
        diffzs.append((self.end_zs[i] - zs[i])**2)
    else: 
      for i in range(21):
        diffxs.append((self.xs[i] - xs[i])**2)
        diffys.append((self.ys[i] - ys[i])**2)
        diffzs.append((self.zs[i] - zs[i])**2)
      
    
    tol = 0.01
    if sum(diffxs)/21 < tol and sum(diffys)/21<tol:
      return True
    return False
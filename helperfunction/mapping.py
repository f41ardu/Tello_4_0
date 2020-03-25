def map(x, in_min, in_max, out_min,  out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

x = 67.08
y = int(map(x, 0, 1024, 0, 255));
print(y)
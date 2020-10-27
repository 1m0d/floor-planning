import heapq

class Rectangle:
  rect_count = 0

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.rotated = False
    self.domain = []
    self.domain_index = 0
    self.position = {}
    self.occupied_space = []
    self.domain_master = None

    Rectangle.rect_count += 1
    self.id = Rectangle.rect_count

  # reversed for heapq
  def __lt__(self, other):
    return self.height * self.width > other.height * other.width

  def calculate_occupied_space(self):
    if(not self.position): return

    self.occupied_space = []
    for h in range(self.height):
      for w in range(self.width):
        x = self.position['x'] + w
        y = self.position['y'] + h
        self.occupied_space.append({ 'x': x, 'y': y })

  def rotate(self):
    self.width, self.height = self.height, self.width
    self.rotated = not self.rotated

  @staticmethod
  def overlap(x1_start, x1_end, y1_start, y1_end, x2_start, x2_end, y2_start, y2_end):
    if(x1_start >= x2_end or x2_start >= x1_end):
      return False

    if(y1_start >= y2_end or y2_start >= y1_end):
      return False

    return True

  def select_satisfactory_domain(self, positioned_que):
    for index in range(self.domain_index, len(self.domain)):
      domain_value = self.domain[index]
      if(domain_value['rotated'] != self.rotated): self.rotate()

      unsatisfactory = False

      x1_start = domain_value['x']
      y1_start = domain_value['y']
      x1_end = domain_value['x'] + self.width
      y1_end = domain_value['y'] + self.height

      for rectangle2 in positioned_que:
        x2_start = rectangle2.position['x']
        y2_start = rectangle2.position['y']
        x2_end = rectangle2.position['x'] + rectangle2.width
        y2_end = rectangle2.position['y'] + rectangle2.height

        if(Rectangle.overlap(x1_start, x1_end, y1_start, y1_end, x2_start, x2_end, y2_start, y2_end)):
          unsatisfactory = True
          break

      self.domain_index += 1
      if(unsatisfactory): continue

      self.domain_index += 1
      return domain_value

    self.domain_index = 0
    return False

class Room:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.pillars = []
    self.rectangles = []

  def add_pillar(self, x, y):
    self.pillars.append({'x': x, 'y': y})

  def add_rectangle(self, rectangle):
    self.rectangles.append(rectangle)

  def calculate_base_domain(self, rectangle):
    if(rectangle.domain_master is not None):
      rectangle.domain = rectangle.domain_master.domain
      return

    for _ in range(2):
      delta_h = self.height - rectangle.height
      delta_w = self.width - rectangle.width
      if(delta_h < 0 or delta_w < 0):
        rectangle.rotate()
        continue

      for h in range(delta_h + 1):
        for w in range (delta_w + 1):
          if(self.__pillar_overlap(w, h, rectangle)):
              continue
          rectangle.domain.append({'x': w, 'y': h, 'rotated': rectangle.rotated})

      if(rectangle.width != rectangle.height):
        rectangle.rotate()
      else:
        break

  def __pillar_overlap(self, w, h, rectangle):
    for pillar in self.pillars:
      x_range = range(w + 1, w + rectangle.width)
      if(pillar['x'] not in x_range):
        return False

      y_range = range(h + 1, h + rectangle.height)
      if(pillar['y'] not in y_range):
        return False

    return True

  def find_rectangle_id(self, x, y):
    for rectangle in self.rectangles:
      if(not bool(rectangle.position)): continue

      if(not rectangle.occupied_space):
        rectangle.calculate_occupied_space()

      if({'x': x, 'y': y} in rectangle.occupied_space):
        return rectangle.id

    return '.'

  def __str__(self):
    result = ""
    for h in range(self.height):
      for w in range(self.width):
        result += str(self.find_rectangle_id(w, h))
        if(w == self.width - 1 and h != self.height - 1):
          result += "\n"
        else:
          result += "\t"

    return result

# -----READ INPUT------

def parse_int_from_input():
    return list(map(int, input().split('\t')))

data = parse_int_from_input()
room = Room(data[0], data[1])

pillar_count = int(input())
rectangle_count = int(input())

for _ in range(pillar_count):
  data = parse_int_from_input()
  room.add_pillar(data[1], data[0])

for _ in range(rectangle_count):
  data = parse_int_from_input()
  rectangle = Rectangle(data[0], data[1])
  room.add_rectangle(rectangle)

# ------MAIN------

# minimum remaining variable que for unassigned variable selecting
mrv_que = []

# has the same order as mrv_que
positioned_que = []

for rect in room.rectangles:
  heapq.heappush(mrv_que, rect)

last_rect = None
for rect in mrv_que:
  if(last_rect is not None and last_rect.width == rect.width and last_rect.height == rect.height):
    rect.domain_master = last_rect

  room.calculate_base_domain(rect)
  last_rect = rect

def backtrack():
  if(len(mrv_que) == 0): return True

  rectangle = heapq.heappop(mrv_que)

  while True:
    domain_value = rectangle.select_satisfactory_domain(positioned_que)
    if not(bool(domain_value)): break

    rectangle.position = {'x': domain_value['x'], 'y': domain_value['y']}
    positioned_que.append(rectangle)
    if(backtrack()): return True
    positioned_que.pop()

  rectangle.position = {}

  heapq.heappush(mrv_que, rectangle)

  return False

if(not backtrack()): raise(Exception("Solution not found"))
print(room)

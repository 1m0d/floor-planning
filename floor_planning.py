import heapq

class Rectangle:
  rect_count = 0

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.rotated = False
    self.domain = []
    self.position = {}
    self.occupied_space = []

    Rectangle.rect_count += 1
    self.id = Rectangle.rect_count

  def size(self):
      return self.height * self.width

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

      rectangle.rotate()

    rectangle.base_domain = rectangle.domain[:]

  def __pillar_overlap(self, w, h, rectangle):
    for pillar in self.pillars:
      x_range = range(w + 1, w + rectangle.width)
      y_range = range(h + 1, h + rectangle.height)
      if(pillar['x'] in x_range and pillar['y'] in y_range):
        return True

    return False


  def reduce_domain(self, rectangle):
    domain = rectangle.domain
    if(not domain):
      return

    for rectangle2 in self.rectangles:
      if(not bool(rectangle2.position)): continue

      sum_h = rectangle.height + rectangle2.height
      sum_w = rectangle.width + rectangle2.width
      reduced_domain = []

      y_range = range(rectangle2.position['y'], rectangle2.position['y'] + rectangle2.height)
      x_range = range(rectangle2.position['x'], rectangle2.position['x'] + rectangle2.width)

      for domain_value in domain:
        if(domain_value['rotated'] != rectangle.rotated):
          reduced_domain.append(domain_value)
          continue

        if(sum_w > self.width):
          if(domain_value['y'] in y_range):
            continue

        if(sum_h > self.height):
          if(domain_value['x'] in x_range):
            continue

        domain_x_range = range(domain_value['x'], domain_value['x'] + rectangle.width)
        domain_y_range = range(domain_value['y'], domain_value['y'] + rectangle.height)
        overlap_x = max(x_range.start, domain_x_range.start) < min(x_range.stop, domain_x_range.stop)
        overlap_y = max(y_range.start, domain_y_range.start) < min(y_range.stop, domain_y_range.stop)
        if(overlap_x and overlap_y):
          continue

        reduced_domain.append(domain_value)

      domain = reduced_domain

    rectangle.domain = domain

  def find_rectangle_id(self, x, y):
    for rectangle in self.rectangles:
      if(not bool(rectangle.position)): continue
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


def parse_int_from_input():
    return list(map(int, input().split('\t')))

# read input
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
  room.calculate_base_domain(rectangle)
  room.add_rectangle(rectangle)

# minimum remaining variable que for unassigned variable selecting
mrv_que = []

for rect in room.rectangles:
  heapq.heappush(mrv_que, rect)

def backtrack():
  if(len(mrv_que) == 0): return True
  rectangle = heapq.heappop(mrv_que)
  room.reduce_domain(rectangle)
  rectangle.rotate()
  room.reduce_domain(rectangle)
  for domain_value in rectangle.domain:
    rectangle.position = {'x': domain_value['x'], 'y': domain_value['y']}
    if(rectangle.rotated != domain_value['rotated']):
      rectangle.rotate()
    if(backtrack()): return True

  rectangle.position = {}
  rectangle.domain = rectangle.base_domain[:]
  heapq.heappush(mrv_que, rectangle)

  return False

backtrack()
print(room)

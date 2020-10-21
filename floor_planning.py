import heapq

class Rectangle:
  rect_count = 0

  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.rotated = False
    self.domain = []

    Rectangle.rect_count += 1
    self.id = Rectangle.rect_count

  def size(self):
      return self.height * self.width

  def __lt__(self, other):
    return self.height * self.width < other.height * other.width

  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, position):
    self._position = position
    self.__calcualte_occupied_space()

  # TODO: remove
  def __calcualte_occupied_space(self):
    self.occupied_space = []
    for h in range(self.height):
      for w in range(self.width):
        x = self.position['x'] + w
        y = self.position['y'] + h
        self.occupied_space.append({ 'x': x, 'y': y })

  def rotate(self):
    if(self.position):
      raise('cannot rotate rectangle after position is set')

    self.width, self.height = self.height, self.width
    self.rotated = True


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
      if(delta_h <= 0 or delta_w <= 0): return

      for h in range(delta_h):
        for w in range (delta_w):
          rectangle.domain.append({'x': h, 'y': w, 'rotated': rectangle.rotated})

      rectangle.rotate()

  def calculate_domain(self, rectangle):
    domain = rectangle.domain
    if(not domain):
      return

    for rectangle2 in self.rectangles:
      sum_h = rectangle.height + rectangle2.height
      sum_w = rectangle.width + rectangle2.width
      reduced_domain = []

      if(sum_w > self.width):
        y_range = range(rectangle2.position['y'], rectangle2.position['y'] + rectangle2.height)
        for domain_value in domain:
          if(domain_value['y'] not in range(y_range)):
            reduced_domain.append(domain_value)

      if(not reduced_domain):
        rectangle.domain = reduced_domain
        return

      if(sum_h > self.height):
        x_range = range(rectangle2.position['x'], rectangle2.position['x'] + rectangle2.width)
        for domain_value in domain:
          if(domain_value['x'] not in range(x_range)):
            reduced_domain.append(domain_value)

      if(not reduced_domain):
        rectangle.domain = reduced_domain
        return

def parse_int_from_input():
    return list(map(int, input().split('\t')))

# read input
data = parse_int_from_input()
room = Room(data[0], data[1])

pillar_count = int(input())
rectangle_count = int(input())

for _ in range(pillar_count):
  data = parse_int_from_input()
  room.add_pillar(data[0], data[1])

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
  if(len(mrv_que) == 0): return
  rectangle = heapq.heappop(mrv_que)

backtrack()

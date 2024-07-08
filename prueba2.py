import pygame
# Your game setup would go here
Rect = pygame.Rect

r = Rect(1, 1, 10, 5)

rects = [
    Rect(1, 1, 5, 10),
    Rect(1, 2, 10, 10),
    Rect(15, 15, 1, 1),
    Rect(2, 2, 1, 1),
]

result = r.collidelistall(rects)  # -> <rect(1, 1, 10, 10)>

print(result)

class ObjectWithSomRectAttribute:
    def __init__(self, name, collision_box, draw_rect):
        self.name = name
        self.draw_rect = draw_rect
        self.collision_box = collision_box

    """def __repr__(self):
        return f'<{self.__class__.__name__}("{self.name}", {list(self.collision_box)}, {list(self.draw_rect)})>'"""

objects = [
    ObjectWithSomRectAttribute("A", Rect(15, 15, 1, 1), Rect(1, 1, 50, 50)),
    ObjectWithSomRectAttribute("B", Rect(2, 2, 10, 10), Rect(300, 300, 50, 50)),
    ObjectWithSomRectAttribute("C", Rect(2, 2, 10, 10), Rect(200, 500, 50, 50)),
]

# collision = r.collideobjects(objects) # this does not work because the items in the list are no Rect like object
collision = r.collideobjectsall(
    objects, key=lambda o: o.collision_box
)  # -> <ObjectWithSomRectAttribute("B", [1, 1, 10, 10], [300, 300, 50, 50])>
print(collision)

screen_rect = r.collideobjectsall(objects, key=lambda o: o.draw_rect)  # -> None
print(screen_rect)
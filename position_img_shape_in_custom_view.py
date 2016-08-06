import ui, textlayout

class Element(object):
    def draw(self):
        pass

class Img(Element):
    def __init__(self, image_name, frame):
        self.image_name = image_name
        self.frame = frame
        self.image = ui.Image.named(self.image_name)
        
    def draw(self):
        self.image.draw()

class Shape(Element):
    shape_objects = {
        'rect': ui.Path.rect,
        'oval': ui.Path.oval
        }
    def __init__(self, shape_type, color, frame, corner_radius=10):
        self.shape_type = shape_type
        self.color = color
        self.frame = frame
        self.corner_radius = corner_radius
        
    def draw(self):
        ui.set_color(self.color)
        self.path = Shape.shape_objects[self.shape_type](*self.frame)
        self.path.fill()
        
layout_text = '''
********
i--*****
|--*****
**s--***
********
****s--*
********
********
'''

ui_element_map = {
        'i': ('image', Img),
        's': ('shape', Shape)
}
layout_processor = textlayout.LayoutProcessor(layout_text,
    width=600, height=600,
    marginx=1, marginy=1,
    ui_element_map=ui_element_map)
frame_map = layout_processor.frame_map
#print(frame_map)
        
class MyView (ui.View):
    def __init__(self, elements):
        self.elements = elements
        self.index = 0

    def draw(self):
        self.elements[self.index].draw()

    def touch_began(self, touch):
        self.index = (self.index+1)%len(self.elements)
        self.set_needs_display()
        
frame = (0, 0, 600, 600)        
v = ui.View(frame=frame) 

elements = [Shape('rect', 'red', frame_map['s'][0]),
            Shape('oval', 'green', frame_map['s'][1]),
            Img('Dog_Face', frame_map['i'][0])] 
                                    
cv = MyView(elements)
cv.width = frame[2]
cv.height = frame[3]
cv.flex='WH'
v.add_subview(cv)
v.present('popover')

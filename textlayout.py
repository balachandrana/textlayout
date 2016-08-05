# coding: utf-8
"""
A compact text based alternative to pyui

layout_text
  - specifies position and size of each ui elemement
  - lines represent rows in grid and each character represents a grid cell
  - '*' represenrs blank cell
  -  ui elements represented by a single character
                'b': ('button', ui.Button),
                'c': ('switch', ui.Switch),
                'd': ('datepicker', ui.DatePicker),
                'f': ('textfield', ui.TextField),
                'g': ('segmentedcontrol', ui.SegmentedControl),
                'i': ('imageview', ui.ImageView),
                'l': ('label', ui.Label),
                's': ('slider', ui.Slider),
                't': ('textview', ui.TextView),
                'w': ('webview', ui.WebView),
                'V': ('view', ui.View)
    - the characters '-' and '|' are used for horizontal and vertical spanning of grid cells
    
    # sample layout specification 
    # - counter aplication with one label and one button
    # - the label element - single row with four horizontal cells
    # - the button element - a rectangular box of 3*4 cells
    layout_text = '''
    ********
    **l---**
    ********
    ********
    **b---**
    **|--|**
    **|--|**
    ********
    ********
    '''
"""
import ui, textwrap

class LayoutProcessor(object):
    def __init__(self, layout_text,
            width=400, height=600,
            cell_size=None,
            marginx=2, marginy=2,
            ui_element_map=None):
        self.layout_text = layout_text
        self.ui_element_map = ui_element_map
        self.height = height
        self.width = width
        self.marginx = marginx
        self.marginy = marginy
        self.frame_map = None
        self.cell_size = cell_size
        self.size = None
        self.build_frame_map()
               
    def process_layout_text(self):
        self.layout_list = [i for i in textwrap.dedent(self.layout_text).strip().split('\n')]
        self.m = len(self.layout_list)
        self.n = max(len(l) for l in self.layout_list)
        if self.cell_size:
            self.cell_width, self.cell_height = self.cell_size
        else:
            self.cell_width = self.width/self.n
            self.cell_height = self.height/self.m 
            self.cell_size = (self.cell_width, self.cell_height)
        self.size = (self.cell_width*self.n, self.cell_height*self.m)       
        
    def get_frame(self, s, i, j):
        p = j + 1
        while p < len(s[i]) and s[i][p] == '-':
            p += 1
        q = i + 1
        while q < len(s) and s[q][j] == '|':
            q += 1
        x = j * self.cell_width + self.marginx
        y = i * self.cell_height + self.marginy
        h = (q - i) * self.cell_height - 2 * self.marginy
        w = (p - j) * self.cell_width - 2 * self.marginx
        return (x, y, w, h)
    
    def build_frame_map(self):
        self.process_layout_text()
        lines = self.layout_list
        frame_map = {}
        for i, item_i in enumerate(lines):
            for j, item_j in enumerate(item_i):
                if item_j in self.ui_element_map: #'bcdfgilstwV':
                    frame_map.setdefault(item_j, []).append(
                            self.get_frame(lines, i, j))
        self.frame_map = frame_map

class BuildView(object):
    """
            Build view object from layout text and attribute text
    """
    def __init__(self, layout_text,
            position=(0, 0),
            width=400, height=600,
            marginx=2, marginy=2,
            view_name='View',
            attributes=None):
        self.ui_element_map = {
                'b': ('button', ui.Button),
                'c': ('switch', ui.Switch),
                'd': ('datepicker', ui.DatePicker),
                'f': ('textfield', ui.TextField),
                'g': ('segmentedcontrol', ui.SegmentedControl),
                'i': ('imageview', ui.ImageView),
                'l': ('label', ui.Label),
                's': ('slider', ui.Slider),
                't': ('textview', ui.TextView),
                'w': ('webview', ui.WebView),
                'v': ('view', ui.View),  #main view             
                'V': ('view', ui.View) #custom view
                }
        self.view_name = view_name
        self.position = position
        self.width = width
        self.height = height
        self.attributes = {elem: attributes.get(elem, [])
                           for elem in self.ui_element_map}
        self.layout_processor = LayoutProcessor(layout_text,
            width=width, height=height,
            marginx=marginx, marginy=marginy,
            ui_element_map=self.ui_element_map)
        self.frame_map = self.layout_processor.frame_map
                                         
    def build_node(self, class_char, idx, frame, attributes=None):
        name, ui_element = self.ui_element_map[class_char]
        index = idx + 1
        v = ui_element(name=((name)+ str(index)))
        v.frame = frame
        for attr in attributes or []:
            #print(attr, attributes[attr], type(attributes[attr]))
            setattr(v, attr, attributes[attr])
        return v  

    def build_main_view_node(self, frame=(0, 0, 100, 100), attributes=None):
        v = self.build_node('V', -1, frame, attributes)
        v.name = self.view_name         
        return v    
                        
    def build_view(self):
        view_attr = self.attributes.get('v', None)
        view_attr = view_attr[0] if view_attr else None
        main_view_node = self.build_main_view_node((self.position[0],
            self.position[1], self.width, self.height), view_attr)
        for ch in self.frame_map:
            for i, frame in enumerate(self.frame_map[ch]):
                node_attr =  self.attributes[ch][i] if (
                    ch in self.attributes and i in range(
                        len(self.attributes[ch]))) else None
                node = self.build_node(ch, i, frame, node_attr)
                main_view_node.add_subview(node)
        return main_view_node
              
if __name__ == '__main__':
    cnt = 0
    def button_action(sender):
        global cnt
        cnt += 1
        sender.superview['label1'].text = 'Counter:' + str(cnt)

    layout_text = '''
    ********
    **l---**
    ********
    ********
    **b---**
    **|--|**
    **|--|**
    ********
    ********
    '''
    
    attributes = {
        'b':[
           {'action':button_action,
             'font' :('Helvetica', 20),
             'title':'Tap to increment counter'
           }],
         'l':[
              {
                'text': 'Counter:0',
                'alignment':  ui.ALIGN_CENTER,
                'font':('Helvetica', 20)
              }
              ]
             }      
                 
    v = BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes=attributes).build_view()
    v.present('popover')

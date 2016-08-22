import circulartextlayout
import ui


layout_text = '''
************
************
bbbbbbbbbbbb
************
i*i*i*i*i*i*
************
************
'''

image_list = [ ui.Image.named(i) for i in 'Rabbit_Face Mouse_Face Cat_Face Dog_Face Octopus Cow_Face'.split()]
_range_12 = (.3, .34, .38, .42, .46, .5, .55, .6, .63, .7, .85, 1.0)

def button_action(sender):
    print('Button {} was pressed.'.format(sender.title))
        
titles = 'jan feb mar apr may jun jul aug sep oct nov dec'.split()

attributes = {'b': [{'action':button_action, 'font' :('Helvetica', 20),
                     'bg_color':'orange', 'alpha':_range_12[i],
                     'border_width':.5, 'text_color':'black', 'tint_color':'black',
                     'title':j } for i, j in enumerate(titles)],
             'i': [{'image':i,  'bg_color':'gray'} for i in image_list ]                  
             }
                       
v = circulartextlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
    attributes=attributes).build_view()
    
for i in range(1, len(titles)+1):
    v['button'+str(i)].corner_radius = v['button'+str(i)].width*.5
for i in range(1, len(image_list)+1):
    v['imageview'+str(i)].corner_radius = v['imageview'+str(i)].width*.5
v.present('popover')

import circulartextlayout
import ui


layout_text = '''
******
iiiiii
******
'''
        
image_list = [ ui.Image.named(i) for i in 'Rabbit_Face Mouse_Face Cat_Face Dog_Face Octopus Cow_Face'.split()]
attributes = {'i': [{'image':i,  'bg_color':'gray'} for i in image_list ]}
                       
v = circulartextlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
    attributes=attributes).build_view()
    
for i in range(1, len(image_list)+1):
    v['imageview'+str(i)].corner_radius = v['imageview'+str(i)].width*.5
v.present('popover')

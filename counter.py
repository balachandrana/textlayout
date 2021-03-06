import ui, textlayout


def button_action(sender):
    label = sender.superview['label1']
    label.text = 'Counter: ' + str(int(label.text.split()[-1]) + 1)

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
            'text': 'Counter: 0',
            'alignment':  ui.ALIGN_CENTER,
            'font':('Helvetica', 20)
          }
          ]
         }      
             
v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
    attributes=attributes).build_view()
v.present('popover')

#coding: utf-8
# ColorMixer
# A simple RGB color mixer with three sliders.

import ui
import clipboard
import textwrap
from random import random
from console import hud_alert
from textlayout import BuildView

def slider_action(sender):
    # Get the root view:
    v = sender.superview
    # Get the sliders:
    r = v['slider1'].value
    g = v['slider2'].value
    b = v['slider3'].value
    # Create the new color from the slider values:
    v['view1'].background_color = (r, g, b)
    v['label1'].text = '#%.02X%.02X%.02X' % (int(r*255), int(g*255), int(b*255))

def copy_action(sender):
    clipboard.set(sender.superview['label1'].text)
    hud_alert('Copied')

def shuffle_action(sender):
    v = sender.superview
    s1 = v['slider1']
    s2 = v['slider2']
    s3 = v['slider3']
    s1.value = random()
    s2.value = random()
    s3.value = random()
    slider_action(s1)

layout_text =       '''\
                    V-l-
                    s---
                    s---
                    s---
                    b-b-
                    '''

attributes = {
    's':[
        {'background_color':'whitesmoke',
         'tint_color':'red',
         'action':slider_action},
        {'background_color':'whitesmoke',
         'tint_color':'blue',
         'action':slider_action},
        {'background_color':'whitesmoke',
         'tint_color':'green',
         'action':slider_action}
        ],
    'l':[{'background_color':'whitesmoke',
            'alignment':ui.ALIGN_CENTER}],
    'b':[
        {'background_color':'whitesmoke',
         'title':'shuffle',
         'action':shuffle_action},
        {'background_color':'whitesmoke',
         'title':'copy',
         'action':copy_action}
        ],
    'v':[{'background_color':'white'}]}
                           
# Building and presenting main view                                                        
v = BuildView(layout_text, width=400, height=350,
    view_name='Color Mixer', attributes=attributes).build_view() 
slider_action(v['slider1'])    
v.present('popover')

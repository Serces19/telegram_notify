import nuke
from telegram_notify.notify import notify

code = '''

import nuke
import re
import os
from telegram_notify.notify import notify
from telegram_notify.render_proxy import render_proxy

write_node = nuke.thisNode()
render_path = nuke.filename(write_node)
nueva_extension = "proxy.mp4"
render_path_proxy = re.sub(r"\.\w+$", "." + nueva_extension, render_path)

render_proxy()
class_notify = notify()
class_notify.send_video(render_path_proxy, "Proxy render .mp4")

'''

def add_old_telegram():

    for nodo in nuke.allNodes():
        if nodo.Class() == 'Write':
            if 'telegram_notify' not in nodo.knobs():

                # Crear un nuevo tab personalizado 'Telegram'
                telegram_tab = nuke.Tab_Knob('Telegram', 'Telegram')

                #Agregar el tab personalizado al nodo Write
                nodo.addKnob(telegram_tab) 

                #Agregar el checkbox knob al nodo 
                telegram_notify_knob = nuke.Boolean_Knob('telegram_notify', 'Telegram Notify')
                telegram_notify_knob.setValue(False)
                nodo.addKnob(telegram_notify_knob)

                # Creamos el botón personalizado (Knob Python Script Button) y lo asignamos al nodo de escritura
                custom_button = nuke.PyScript_Knob("render_proxy", "Render proxy and send", code)
                custom_button.setFlag(nuke.STARTLINE)

                # Agregamos el botón al nodo de escritura
                nodo.addKnob(custom_button)

def add_new_telegram(): 
    nodo = nuke.thisNode()
    if nodo.Class() == 'Write':
        if 'telegram_notify' not in nodo.knobs():
            
            # Crear un nuevo tab personalizado 'Telegram'
            telegram_tab = nuke.Tab_Knob('Telegram', 'Telegram')

            #Agregar el tab personalizado al nodo Write
            nodo.addKnob(telegram_tab) 

            telegram_notify_knob = nuke.Boolean_Knob('telegram_notify', 'Telegram Notify')
            telegram_notify_knob.setValue(False)
            nodo.addKnob(telegram_notify_knob)


            # Creamos el botón personalizado (Knob Python Script Button) y lo asignamos al nodo de escritura
            custom_button = nuke.PyScript_Knob("render_proxy", "Render proxy and send", code)
            custom_button.setFlag(nuke.STARTLINE)

            # Agregamos el botón al nodo de escritura
            nodo.addKnob(custom_button)


add_old_telegram()
nuke.addOnCreate(add_new_telegram)

class_notify = notify()
nuke.addAfterRender(class_notify.send_text)



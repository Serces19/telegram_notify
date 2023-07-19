import nuke
import threading
import time
import re
from telegram_notify.notify import notify
from telegram_notify.render_proxy import render_proxy


#########################################################################################################
#Functions

def add_telegram(nodo):
        if nodo.Class() == 'Write':
            if 'telegram_notify' not in nodo.knobs():

                # Tab 'Telegram'
                telegram_tab = nuke.Tab_Knob('Telegram', 'Telegram')
                nodo.addKnob(telegram_tab) 

                # Checkbox 
                telegram_notify_knob = nuke.Boolean_Knob('telegram_notify', 'Telegram Notify')
                telegram_notify_knob.setValue(False)
                nodo.addKnob(telegram_notify_knob)

                # Slider
                slider_knob = nuke.Double_Knob("proxy_scale_factor", "Proxy scale factor")
                slider_knob.setRange(0.25, 0.75)
                slider_knob.setDefaultValue([0.5])
                nodo.addKnob(slider_knob)

                # Boton
                code = '''

write_node = nuke.thisNode()
render_path = nuke.filename(write_node)
render_path = str(render_path)
render_path = os.path.dirname(render_path)
render_path = os.path.normpath(render_path) 

if os.path.exists(render_path):
    if os.path.isdir(render_path):
        if sys.platform.startswith("darwin"):  # macOS
            os.system("open '{}'".format(render_path))
        elif sys.platform.startswith("win32"):  # Windows
            os.startfile(render_path)
        elif sys.platform.startswith("linux"):  # Linux
            os.system("xdg-open '{}'".format(render_path))
    else:
        nuke.message("The path is not a folder.")
else:
    nuke.message("The folder does not exist.")

'''

                button_knob = nuke.PyScript_Knob("open_folder", "Open in folder", code)
                button_knob.setFlag(nuke.STARTLINE)
                nodo.addKnob(button_knob)


def add_old_telegram():
    for nodo in nuke.allNodes():
        add_telegram(nodo)


def add_new_telegram(): 
    nodo = nuke.thisNode()
    add_telegram(nodo)


def iniciar():
    write_node = nuke.thisNode()

    if write_node['telegram_notify'].value() is False:
        return

    colorspace = write_node["colorspace"].value()
    render_path = nuke.filename(write_node)
    nueva_extension = "proxy.mp4"

    ####
    render_path_proxy = re.sub(r"\.\w+$", "." + nueva_extension, render_path)
    render_path_proxy = render_path_proxy.replace('#', '')

    #%03d, %05d, etc.
    pattern = r'%\d+d'
    render_path_proxy = re.sub(pattern, '', render_path_proxy)
    print(render_path, render_path_proxy)

    resize = write_node["proxy_scale_factor"].value()

    class_thread_notify = thread_notify(render_path, render_path_proxy, colorspace, resize)
    class_thread_notify.starting()

class thread_notify():

    def __init__(self, render_path, render_path_proxy, colorspace, resize):
        self.render_path = render_path
        self.render_path_proxy = render_path_proxy
        self.colorspace = colorspace
        self.resize = resize
        

    def after_render(self):
        class_render_proxy = render_proxy(self.render_path, self.render_path_proxy, self.colorspace, self.resize)
        class_render_proxy.render_mp4()
        class_notify = notify()
        class_notify.send_text()
        class_notify.send_video(self.render_path_proxy, "Proxy render mp4")

    def wait_and_execute(self):

        time.sleep(1)
        nuke.executeInMainThread(self.after_render)

    def starting(self):
        threading.Thread(target=self.wait_and_execute).start()
        print('starting')


add_old_telegram()
nuke.addOnCreate(add_new_telegram)

nuke.addAfterRender(iniciar)

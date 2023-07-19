import os
import nuke
import datetime
import requests


bot_token = '6342421425:AAF6Fm5TGrV09FmN0oiKlDfixQgn1AVqLTQ'
chat_id = os.getenv('chat_id')

class notify():

    def __init__(self):
        print('Iniciando notify')
        self.shot = nuke.tcl('file rootname [file tail [value root.name]]')
        self.shot = str(self.shot)

    def send_text(self):
        now = datetime.datetime.now()
        hora_actual = now.strftime("%H:%M:%S")

        textoMensaje = f'The render of *{self.shot}* was completed successfully at *{hora_actual}*'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + textoMensaje

        response = requests.get(send_text)
        return response.json()
        

    def send_video(self, render_path_proxy, caption):
        print('iniciando send video')

        url = f'https://api.telegram.org/bot{bot_token}/sendVideo'

        caption = self.shot + " " + caption
        data = {'chat_id': chat_id, 'caption': caption}
        print(data, render_path_proxy)

        with open(render_path_proxy, 'rb') as video:
            files = {'video': video}
            response = requests.post(url, data=data, files=files)

        return response.json()

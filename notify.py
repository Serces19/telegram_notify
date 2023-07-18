import os
import nuke
import datetime
import requests


bot_token = '6342421425:AAF6Fm5TGrV09FmN0oiKlDfixQgn1AVqLTQ'
chat_id = os.getenv('chat_id')

class notify():

    def send_text(self):
        write_node = nuke.thisNode()

        if write_node['telegram_notify'].value() is False:
            return
        
        shot = nuke.tcl('file rootname [file tail [value root.name]]')
        shot = str(shot)
        now = datetime.datetime.now()
        hora_actual = now.strftime("%H:%M:%S")

        textoMensaje = f'The render of *{shot}* was completed successfully at *{hora_actual}*'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + textoMensaje

        response = requests.get(send_text)
        return response.json()
        

    def send_video(self, video_path, caption=''):
        url = f'https://api.telegram.org/bot{bot_token}/sendVideo'

        data = {'chat_id': chat_id, 'caption': caption}

        with open(video_path, 'rb') as video:
            files = {'video': video}
            response = requests.post(url, data=data, files=files)

        return response.json()

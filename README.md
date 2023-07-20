## Nuke Telegram Render Plugin

This is a simple plugin for Nuke that allows you to automatically send notifications to a Telegram chat whenever a render finishes, along with a preview proxy of the render.

### Installation:

1. Look for Nuke_render_bot on Telegram and start a conversation with it. It will send you a message with your chat_id. Notifications will arrive through this chat, multiple users can point their notifications to the same chat. If you try to initiate a conversation with the bot, it will only provide a generic message and the chat ID, haha!

![Texto alternativo](https://i.imgur.com/Sr1OfNf.png)

2. Download the 'telegram_notify' folder from this repository.

3. Copy it to your Nuke plugins directory, usually located in ~/.nuke or C:/Users/your_user/.nuke.

4. Add the following line to the .init.py file of Nuke to import the plugin:
```python
# Telegram notify
import os
os.environ['chat_id'] = 'your chat id'
import telegram_notify
```
Make sure to replace 'your chat id' with the key provided by the Nuke_render_bot.

### Usage:

Once the plugin is installed, follow these steps to use it:

1. Open Nuke and load your composition.

2. Go to any Write node and look for the Telegram tab.

3. You will see three knobs:
   - Telegram notify: A checkbox to enable or disable the function. If it is disabled, everything will run normally. If it is enabled, a proxy render will be performed, and the notification will be sent to Telegram.
   - Scaling Factor: A control to define the scale factor of the proxy render. Use values 0.25, 0.5, and 0.75 for better results. Outside these values, scaling artifacts may appear.
   - Open in folder: A button to open the current directory where the renders are saved or will be saved (this can be very useful beyond notifications).

4. Configure the knobs according to your needs and perform the rendering.

### Notes on Possible Errors:

If you encounter possible errors during rendering, they may be related to a very high or low resolution of the render. In this case, try adjusting the scaling factor.

Issues may also arise when using a custom color space; in that case, I am thinking of implementing a new knob to define the color space.

There might also be conflicts with other operating systems, such as Linux or macOS.

I hope you find this plugin useful or enjoyable! If you have any questions or comments, feel free to open an issue in this repository.

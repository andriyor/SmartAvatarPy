import os
from datetime import datetime
import time
import requests
import vk_api
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

msg = "message"


def main():
    login, password = os.environ.get('LOGIN'), os.environ.get('PASSWORD')
    vk_session = vk_api.VkApi(login, password, api_version=5.4)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    msg_count = vk.messages.get(filters=1)['count']
    online_count = len(vk.friends.getOnline())
    request_count = vk.friends.getRequests()['count']

    font = ImageFont.truetype("OpenSans-Italic.ttf", 15)
    color = (255, 255, 255)
    text_pos1 = (200, 115)
    text_pos2 = (200, 137)
    text_pos3 = (200, 160)
    mes_pos = (120, 230)
    time_pos = (60, 300)

    times = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    img = Image.open("templates.jpg")
    draw = ImageDraw.Draw(img)
    draw.text(text_pos1, str(msg_count), fill=color, font=font)
    draw.text(text_pos2, str(online_count), fill=color, font=font)
    draw.text(text_pos3, str(request_count), fill=color, font=font)
    draw.text(mes_pos, msg, fill=color, font=font)
    draw.text(time_pos, times, fill=color, font=font)

    del draw
    img.save("result.png")

    get_upload_server = vk.photos.getProfileUploadServer()
    files = {'photo': open('result.png', 'rb')}
    r = requests.post(get_upload_server['upload_url'], files=files).json()
    vk.photos.saveProfilePhoto(hash=r['hash'], photo=r['photo'], server=r['server'])
    vk.wall.delete(post_id=vk.wall.get()['items'][0]['id'])


if __name__ == '__main__':
    while True:
        main()
        print('OK')
        time.sleep(300)

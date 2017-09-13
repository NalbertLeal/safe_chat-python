from PIL import Image
from sys import exit

from exceptions import *

if __name__ == '__main__':
    image_in_path = input('>> write the name of the BMP image to load:\n')

class Bmp_image_proccess():
    def __init__(self):
        pass

    def write_img(self, image_out_path='', img_bytes=''):
        if image_out_path != '' and img_bytes != '':
            file = open(image_out_path, 'wb')
            file.write(img_bytes)
            file.close()
        else:
            raise Out_path_not_defined()

    def read_img(self, image_out_path=''):
        if image_out_path != '':
            file = open(image_out_path, 'rb')
            msg = file.read()
            file.close()

            return msg
        else:
            raise Out_path_not_defined()

    def write_img_message(self, image_in_path, image_out_path, message):
        if image_in_path == '':
            raise Out_path_not_defined()
        if image_out_path == '':
            raise In_path_not_defined()
        if message == '':
            raise Mesage_not_defined()
        else:
            img = Image.open(image_in_path)
            img = img.convert('RGB')
            img.getpixel((20, 300))
            imgarray = img.load()

            if len(message) > (img.size[0] * img.size[1])-3:
                raise Mesage_too_long()

            message_size = len(message)
            for w in range(0, 3):
                lt = []
                for i in range(0, 3):
                    if (message_size - 255) > 0:
                        lt.append(255)
                        message_size -= 255
                    else:
                        lt.append(message_size)
                        message_size = 0
                        if i == 0:
                            lt.append(0)
                            lt.append(0)
                        elif i == 1:
                            lt.append(0)
                        else:
                            break
                tp = (lt[0], lt[1], lt[2])
                imgarray[0, w] = tp

            red_sum = 0
            counter = 0
            message_counter = 0
            for h in range(0, img.size[0]):
                for w in range(0, img.size[1]):
                    if h == 0 and w < 3:
                        w = 3
                    if counter == 8 and message_counter < len(message):
                        counter = -1

                        blue = imgarray[h, w][0]
                        green = imgarray[h, w][1]
                        red = (red_sum % 255) + ord(message[message_counter])
                        message_counter += 1

                        imgarray[h, w] = (blue, green, red)

                        red_sum = 0
                    else:
                        red_sum += imgarray[h, w][2]
                    counter += 1

            img.save(image_out_path)

    def read_img_message(self, image_in_path=''):
        if image_in_path != '':
            img = Image.open(image_in_path)
            img = img.convert('RGB')
            img.getpixel((20, 300))
            imgarray = img.load()

            message_size = 0
            for w in range(0, 3):
                message_size += imgarray[0, w][0]
                message_size += imgarray[0, w][1]
                message_size += imgarray[0, w][2]

            print(message_size, '\n')

            red_sum = 0
            counter = 0
            message_counter = 0
            message = ''
            for h in range(0, img.size[0]):
                for w in range(0, img.size[1]):
                    if message_counter == message_size:
                        break
                    elif counter == 8:
                        counter = -1

                        message += chr( imgarray[h, w][2] - (red_sum % 255) )
                        message_counter += 1

                        red_sum = 0
                    else:
                        red_sum += imgarray[h, w][2]
                    counter += 1
            return message
        else:
            return ''

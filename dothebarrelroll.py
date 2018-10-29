'''
1. Читаем
2. Генерируем массив 1/0 размером с кол-во пикселей
3. Читаем текст и заменяем пиксели согласно маске из 2 пункта


'''
import math
import random
from random import randrange
import binascii
from PIL import Image, ImageDraw
import numpy as np
import cv2


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    res = ''
    #print(n)

    RES = int2bytes(n).decode(encoding, errors)
    res = RES
    return res


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))






def psnr(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))




def cipher(picname, texttocipher):
    random.seed(5435)
    image = Image.open(picname) #Открываем изображение. 
    draw = ImageDraw.Draw(image) #Создаем инструмент для рисования. 
    width = image.size[0] #Определяем ширину. 
    height = image.size[1] #Определяем высоту.  
    pix = image.load() #Выгружаем значения пикселей.
    #print (pix)

    image.save('sd.bmp',format='BMP')

    lenofcontainer = width*height
    mask = [randrange(0,2) for i in range(lenofcontainer)]

    messageinbits = text_to_bits(texttocipher)
    #print(messageinbits)
    print("Длинна контейнера: "+str(len(mask))+"\n Длинна сообщения: "+ str(len(messageinbits)))
    if (len(mask)<len(messageinbits)):
        print('The message is too long. Try decreasing the message length or increasing the container capacity.')
    print("CheckPoint",".BMP")
    counter = 0
    mescounter = 0
    tostop = False
    for i in range(width):
        for j in range(height):

            if mask[counter] == 1:
                if mescounter == len(messageinbits):
                    image.save('sd.bmp',format='BMP')  
                    f = open("len.txt",'w')
                    f.write(str(mescounter))
                    f.close()
                    exit()
                if messageinbits[mescounter] == "0":
                    one = pix[i, j][0]
                    two = pix[i, j][1]
                    three = pix[i, j][2]
                    c = pix[i, j][2]
                    b = c//10
                    c = b*10
                   # print (pix[i,j])
                    pix[i, j] = (one,two,c)
                    #print (pix[i,j])
                    mescounter +=1
                    if tostop:
                        image.save('sd.bmp',format='BMP')  
                        exit()
                elif messageinbits[mescounter] == "1":
                    one = pix[i, j][0]
                    two = pix[i, j][1]
                    three = pix[i, j][2]
                    c = pix[i, j][2]
                    b = c//10
                    c = (b*10)+1
                   # print (pix[i,j])
                    pix[i, j] = (one,two,c)
                    #print (pix[i,j])
                    mescounter+=1
                    if tostop:
                        image.save('sd.bmp',format='BMP')  
                        exit()
            counter += 1

    image.save('sd.bmp',format='BMP')          
  

def decipher(picname):
    random.seed(5435)
    image = Image.open(picname) #Открываем изображение. 
    draw = ImageDraw.Draw(image) #Создаем инструмент для рисования. 
    width = image.size[0] #Определяем ширину. 
    height = image.size[1] #Определяем высоту.  
    pix = image.load() #Выгружаем значения пикселей.
    print (pix)

    image.save('sd.bmp',format='BMP')

    lenofcontainer = width*height
    mask = [randrange(0,2) for i in range(lenofcontainer)]
    
    print("CheckPoint",".BMP")
    counter = 0
    ret = []
    for i in range(width):
        for j in range(height):

            if mask[counter] == 1 :
                if pix[i,j][2] % 2 == 0:
                    ret.append("0")
                else:
                    ret.append("1")
            counter +=1
    f = open("len.txt",'r')
    l = f.read()
    f.close
    lenn = int(l)
    rett = ret[:lenn]
    res = "".join(rett)
    print(res)
    print(text_from_bits(res))
    image.save('sd.bmp',format='BMP')          

def main():
    #cipher("x.bmp","someygufdsomeygufdhsjfdshjfksdfhkjsdfhdssomeygufdhsjfdshjfksdfhkjsdfhdssomeygufdhsjfdshjfksdfhkjsdfhdssomeygufdhsjfdshjfksdfhkjsdfhdssomeygufdhsjfdshjfksdfhkjsdfhdssomeygufdhsjfdshjfksdfhkjsdfhdssomeygufdhsjfdshjfksdfhkjsdfhdssomeygufdhsjfdshjfksdfhkjsdfhdshsjfdshjfksdfhkjsdfhds")
    decipher("sd.bmp")
    #calculatepsnr('x.bmp','sd.bmp')


    original = cv2.imread("x.bmp")
    contrast = cv2.imread("sd.bmp",1)

    d=psnr(original,contrast)
    print(d)

if __name__ == '__main__':
    main()
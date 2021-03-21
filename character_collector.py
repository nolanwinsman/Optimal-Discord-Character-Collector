import pyautogui
import sys
import glob
import os
import pytesseract as tess
#tess.pytesseract.tesseract_cmd = r'C:\Users\Nolan\AppData\Local\Tesseract-OCR\tesseract.exe' #Windows machines need the path to tesseract.exe
from PIL import Image, ImageEnhance
import math
import time
import cv2
import re
import webbrowser




#makes adjustments to the image to increase the accuracy of pytesseract, adjustments like resizing and increasing contrast
def adjustImage(path, photo):
    img = cv2.imread(path + photo)
    image = Image.open(path + photo)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(4.0)
    image.save(path+photo)
    scale_percent = 4  # three times original size
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(photo, resized)

#takes an image file and outputs a string of any text that pytesseract reads
def readImage(photo):
    img = Image.open(photo)
    text = tess.image_to_string(img)
    return (text)

#takes a screenshot in the region given by the parameter list
def takeScreenshot(n,list,char):
    fileName = str('C' + str(n) + char + '.tiff')
    im = pyautogui.screenshot(fileName, region=(list[0:4]))  # Windows Machine

#clicks where the chat bar is on the discord webpage
def clickChatBar():
    pyautogui.click(600, 1010)
    #y = 978 for windows


# deletes all files with the extension .tiff in the given path
def deleteImg(p):
    files = os.listdir(p)
    for f in files:
        if ".tiff" in f:
            os.remove(f)

#Once the character name has been found this function uses the discord bot to search the character and retrieve an int of the character's monetary value in the game
def findValue(n, name):
    clickChatBar()
    file = str('C'+str(n)+'R.tiff')
    typeOnScreen('$IM ' + name)
    takeScreenshot(n,[450,283,300,300],'R')
    #takeScreenshot(n, [490, 200, 300, 300], 'R')
    adjustImage(path, file)
    value = readImage(path + file)
    value = findInString(value, 'roulette','Animanga')
    return value

#checks to see if the character rolled is worth collecting based on if the character name shows up in wishlist.txt or their value is above 100
def checkCollect(cName, cValue):
    if (cName) in w:
        print('Character Name in wishlist.txt')
        return True
    elif cValue >=150:
        return True
    else:
        return False

#collects the character
def collect():
    print('collected')
    pyautogui.moveTo(1500, 900)
    pyautogui.scroll(-1000)
    pyautogui.scroll(7)
    y = 950
    while y >800:
        pyautogui.click(474, y)
        y-=10
        time.sleep(0.5)
    claimedToTrue(0)
    finished()

#Takes two strings, if the string 'target' is found in the string 's' then it returns target as an int, otherwise it returns -1 as it failed to find 'target'
def findInString(s,target,target2):
    index = s.find(target)
    index2 = s.find(target2)
    if index == -1 and index2 == -1:
        print(target,' Not found in string')
        return -1
    elif index >0:
        s = extractIntFromString(s[index+8:index+17])
        return int(s)
    elif index2 > 0:
        s = extractIntFromString(s[index2+8:index2+17])
        return int(s)
    else:
        print('error')

#clicks where the discord chat bar is, types the string 's' presses ENTER, then it waits 2 seconds
def typeOnScreen(s):
    clickChatBar()
    pyautogui.typewrite(s, interval=0.05)
    pyautogui.press('Enter')
    time.sleep(2)

#finds a list of all ints in a string then returns the first index of that list
def extractIntFromString(s):
    i = re.findall('\d+',s)
    try:
        return i[0]
    except:
        return -1

#if string 's' can be cast to an INT it returns true, otherwise it returns false
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        print(s,' is not an int')
        return False

#simple method that closes the tab and exits the program
def finished():
    pyautogui.hotkey('ctrl', 'w')
    exit()

#path = r'C:\Users\Nolan\PycharmProjects\waifu\\'  # Windows Machine
path = r'/home/nolanwinsman/PycharmProjects/waifu/' #Linux Machine


def main():
    checkClaimAvalibility()
    os.chdir(path)
    deleteImg(path)
    webbrowser.open('https://discord.com/channels/614566919265058819/614861613903904768')  #opens main server
    #webbrowser.open('https://discord.com/channels/763507853851623464/766047479334174745') #opens test server
    time.sleep(15)
    clickChatBar()
    typeOnScreen('$DK')

    #For loop that will roll a character and evaluate if they are worth claiming each iteration
    for n in range(1, 22):
        print('_________ ', n, ' _________')
        typeOnScreen('$WA')
        file = ('C' + str(n) + '.tiff') #the name of the screenshot that will store the character name
        takeScreenshot(n, [467, 530, 228, 55],'') #Linux Dimensions
        #takeScreenshot(n, [500,370,400,30],'') #Windows Dimensions For discord webpage zoom %125
        adjustImage(path, file)
        cName = readImage(file)
        print('Character Name : '+cName)
        value = findValue(n, cName)
        if RepresentsInt(value) == True:
            print('Value: ',int(value))
            if checkCollect(cName, int(value)) == True:
                collect()
            else:
                print('Character not Collected')
    finished()



if __name__ == "__main__":
        main()

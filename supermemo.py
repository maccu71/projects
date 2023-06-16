#!/bin/python3
import pygame
from time import sleep
from selenium import webdriver as driver

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print ("No joystick attached!")
    sleep(2)
    exit()
joystick = pygame.joystick.Joystick(0)
joystick.init()

driver = webdriver.Firefox()

# logowanie na supermemo
driver.get('https://www.supermemo.com/en/authorization/login?returnUrl=%2Fen')
driver.find_element("xpath", '/html/body/supermemo-root/app-cookie/div/div/button').click()  ### cockie
element = driver.find_element("xpath", '/html/body/supermemo-root/sm-localization/sm-authorization/div/div[2]/div/div/app-login/form/span/app-authorization-input/div/div/input')
element.send_keys("maccu@poczta.onet.pl")
sleep(1)
element = driver.find_element_by_xpath('/html/body/supermemo-root/sm-localization/sm-authorization/div/div[2]/div/div/app-login/form/app-authorization-input/div/div/input')
element.send_keys("PASSWORD")
driver.find_element_by_xpath('/html/body/supermemo-root/sm-localization/sm-authorization/div/div[2]/div/div/app-login/form/button').click()
sleep(2)
driver.find_element_by_xpath('/html/body/supermemo-root/sm-localization/sm-landing/sm-default-header/sm-header/header/div/sm-header-logged/div/ul/li[1]/span').click()
sleep(2)
driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div/div[2]/div[1]/sm-hello-course[5]/div/button[1]/div[2]/div[1]/span').click()
sleep(2)
driver.find_element_by_xpath('/html/body/div[7]/sm-cookie-policy/div/button').click()

while not False:
    pygame.event.get()
    if joystick.get_button(3):   ### sprawdzenie UP
        print ("przycisk 3")
        driver.find_element_by_xpath('/html/body/div[6]/div/menu-bottom/div/div/div[2]/button[3]').click()
    elif joystick.get_button(0):      ##  LEFT
        print ("przycisk 0 = ŹLE")
        driver.find_element_by_xpath('/html/body/div[6]/div/menu-bottom/div/div/div[2]/button[6]/span').click()
    elif joystick.get_button(2):      ##   RIGHT
        print ("przycisk 2 = DOBRZE")
        driver.find_element_by_xpath('/html/body/div[6]/div/menu-bottom/div/div/div[2]/button[8]/span').click()
    elif joystick.get_button(1):      ##   DOWN
        print ("przycisk 1 = ŚREDNIO")
        driver.find_element_by_xpath('/html/body/div[6]/div/menu-bottom/div/div/div[2]/button[7]/span').click()
    elif joystick.get_button(5):      ##   SOUND UP
        print ("przycisk 5 = SOUND UP")
        driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div/div/div/div/div[1]/p/fragment[2]/div/sfx/div/button/i').click()
    elif joystick.get_button(7):      ##   DOWN
        print ("przycisk 7 = ŚSOUND DOWN")
        driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div/div/div/div/div[2]/p/fragment[1]/div/sfx/div/button/i').click()
    elif joystick.get_button(4):      ##   DOWN
        print ("przycisk 4 = LEARN")
        driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/div/button[1]').click()
    elif joystick.get_button(6):      ##   DOWN
        print ("przycisk 6 = LEARN")
        driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/div/button[2]/span').click()
    sleep(.2)

## CHECK UP     /html/body/div[6]/div/menu-bottom/div/div/div[2]/button[3]
## BAD          /html/body/div[6]/div/menu-bottom/div/div/div[2]/button[6]/span
## AVERAGE      /html/body/div[6]/div/menu-bottom/div/div/div[2]/button[7]/span
## WELL         /html/body/div[6]/div/menu-bottom/div/div/div[2]/button[8]/span
## UP SOUND     /html/body/div[6]/div/div[1]/div/div/div/div/div[1]/p/fragment[2]/div/sfx/div/button/i
## DOWN SOUND   /html/body/div[6]/div/div[1]/div/div/div/div/div[2]/p/fragment[1]/div/sfx/div/button/i##
#### LEARN      /html/body/div[5]/div/div[1]/div/button[1]
#### REPEAT     /html/body/div[5]/div/div[1]/div/button[2]/span
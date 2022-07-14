from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import string
import keyboard

code = input("Code $ ")

options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)
driver.get("https://pseudo.inanimated.xyz/play/{}".format(code))

path = "./data.txt"
wordlistone = open(path)
stringone = wordlistone.read().splitlines()
random.shuffle(stringone)

used = []
prev = ''
curr = ''

def find_word(syll):
    for i in stringone:
        if i != None and syll in i:
            if not used.__contains__(i):
                used.append(i)
                return i

answered = []

while not keyboard.is_pressed("ctrl+z"):
    try:
        if driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='JoinGameContainer']/button[@id='JoinGameButton']").text == 'Join game':
            driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='JoinGameContainer']/button[@id='JoinGameButton']").click()
    except:
        pass
    time.sleep(.05)
    try:
        executioner : str = driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='StatusContainer']").text
        executioner = executioner.split(' ')[0][:-1]
    except:
        pass
    try:
        data = driver.find_element("xpath", "//div[@id='GameContainer']//div[@id='StatusContainer']//span[@class='Prompt']").text
    except:
        pass
    try:
        curr = data
        if prev != curr:
            print(executioner, curr, find_word(curr))
            prev = curr
    except:
        pass
    try:
        if driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='WordInputContainer']").get_attribute('class') != 'Hidden':
            dat = find_word(curr)
            driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='WordInputContainer']//input[@id='WordInput']").send_keys(dat)
            driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='WordInputContainer']//input[@id='WordInput']").send_keys(Keys.ENTER)
    except:
        pass
    try:
        sidebar = driver.find_element('xpath', "//div[@id='Sidebar']")
        chatTab = sidebar.find_element('xpath', "//div[@id='ChatTab']")
        if chatTab.get_attribute('class') == 'SidebarTab Active':
            chatInput = chatTab.find_element('xpath', "//textarea[@id='ChatInput']")

            chatLog = chatTab.find_element('xpath', "//ol[@id='ChatLog']")
            last_msg = chatLog.find_element('xpath', "(.//li[@class='ChatMessage'])[last()]")
            lm_time = last_msg.find_element('xpath', ".//span[@class='Time']").text
            lm_cntt : str = last_msg.find_element('xpath', ".//span[@class='ChatMessageContent']").text
            
            lm_author = last_msg.find_element('xpath', ".//span[@class='DisplayName']").text
            fusion = '[{}]<{}>{} [id: "{}"]'.format(lm_time, lm_author, lm_cntt, last_msg.id)
            if not fusion in answered:
                answered.append(fusion)
                if lm_cntt.startswith('.'):
                    spl = lm_cntt[1:].split(' ')
                    cmd = spl[0]
                    args = spl[1:]
                    print(cmd, args)
                    if cmd == 'discord':
                        chatInput.click()
                        chatInput.send_keys('[Runned by: {}] https://discord.gg/6gJ8A4zqfw'.format(lm_author))
                        chatInput.send_keys(Keys.ENTER)
                    if cmd == 'echo':
                        chatInput.click()
                        chatInput.send_keys('[Runned by: {}] {}'.format(lm_author, lm_cntt[len(cmd)+2:]))
                        chatInput.send_keys(Keys.ENTER)
                    
            
            
    except:
        pass


driver.close()
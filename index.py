from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import keyboard
import sys
import subprocess
import string
import secrets

code = sys.argv[1]

options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)
driver.get('https://pseudo.inanimated.xyz')
driver.add_cookie({"name": "darkMode", "value": "true"})
driver.add_cookie({"name": "PseudoBP.sid", "value": "s%3AuvC5b9dwEKtQFnYb_gn4Ag3qTqkfZ5P0.N2nHuxDFlZTPxSPrOVJfUkv8X%2BUQl4%2BZl25%2BPYvmphc"})
driver.get("https://pseudo.inanimated.xyz/play/{}".format(code))


path = "./data.txt"
wordlistone = open(path)
stringone = wordlistone.read().splitlines()
random.shuffle(stringone)

used = []
prev = ''
curr = ''
is_dormant = True

def find_word(syll):
    for i in stringone:
        if i != None and syll in i:
            if not used.__contains__(i):
                used.append(i)
                return i

answered = []
while not keyboard.is_pressed("ctrl+z"):
    try:
        if driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='JoinGameContainer']/button[@id='JoinGameButton']").text == 'Join game' and not is_dormant:
            driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='JoinGameContainer']/button[@id='JoinGameButton']").click()
    except:
        pass
    try:
        executioner : str = driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='StatusContainer']").text
        executioner = executioner.split(' ')[0][:-1]
    except:
        pass
    try:
        data = driver.find_element("xpath", "//div[@id='GameContainer']//div[@id='StatusContainer']//span[@class='Prompt']").text
    except:
        pass
    time.sleep(0.05)
    try:
        curr = data
        if prev != curr:
            print(executioner, curr, find_word(curr))
            prev = curr
    except:
        pass
    try:
        if not is_dormant:
            if driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='WordInputContainer']").get_attribute('class') != 'Hidden':
                dat = find_word(curr)
                driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='WordInputContainer']//input[@id='WordInput']").send_keys(dat)
                driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='WordInputContainer']//input[@id='WordInput']").send_keys(Keys.ENTER)
        else:
            if driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='WordInputContainer']").get_attribute('class') != 'Hidden':
                driver.find_element('xpath', "//div[@id='GameContainer']//button[@id='GlennButton']").click()
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
                    if cmd == 'dormant':
                        mods = [i.get_attribute('data-display-name') for i in driver.find_elements('xpath', "//ul[@id='UserList']//li[@class='UsersTabUser Mod']")]
                        owner = driver.find_element('xpath', "//ul[@id='UserList']//li[@class='UsersTabUser Host']").get_attribute('data-display-name')
                        if lm_author == owner or lm_author in mods:
                            is_dormant = not is_dormant
                            chatInput.click()
                            chatInput.send_keys('[MOD-Runned by: {}] Dormant mode is {}'.format(owner, 'on' if is_dormant else 'off'))
                            chatInput.send_keys(Keys.ENTER)
                        else:
                            chatInput.click()
                            chatInput.send_keys('[Runned by: {}] You don\'t have access to this command'.format(lm_author))
                            chatInput.send_keys(Keys.ENTER)
                    if cmd == 'leave':
                        owner = driver.find_element('xpath', "//ul[@id='UserList']//li[@class='UsersTabUser Host']").get_attribute('data-display-name')
                        if lm_author == owner:
                            chatInput.click()
                            chatInput.send_keys('cya guys!')
                            chatInput.send_keys(Keys.ENTER)
                            driver.close()
                            sys.exit()
                        else:
                            chatInput.send_keys('[Runned by: {}] You don\'t have access to this command'.format(lm_author))
                            chatInput.send_keys(Keys.ENTER)
                    if cmd == 'b':
                        data = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(6))
                        chatInput.click()
                        chatInput.send_keys('[Runned by: {}] https://pseudo.inanimated.xyz/{}'.format(lm_author, data))
                        chatInput.send_keys(Keys.ENTER)
                        subprocess.call(['python', 'index.py', data])
                    if cmd == 'start':
                        #print(driver.find_elements('xpath', "//ul[@id='UserList']//li[@class='UsersTabUser Mod']"))
                        mods = [i.get_attribute('data-display-name') for i in driver.find_elements('xpath', "//ul[@id='UserList']//li[@class='UsersTabUser Mod']")]
                        owner = driver.find_element('xpath', "//ul[@id='UserList']//li[@class='UsersTabUser Host']").get_attribute('data-display-name')
                        print(mods, owner)
                        if lm_author in mods or lm_author == owner:
                            startbtncnt = driver.find_element('xpath', "//div[@id='GameContainer']//div[@id='StartGameContainer']")
                            print(startbtncnt.get_attribute('style'))
                            if startbtncnt.get_attribute('style') == 'display: none;':
                                chatInput.click()
                                chatInput.send_keys('[Runned by: {}] Unable to start the game'.format(lm_author))
                                chatInput.send_keys(Keys.ENTER)
                            else:
                                startbtncnt.find_element('xpath', "//button[@id='StartGameButton']").click()
                        else:
                            chatInput.click()
                            chatInput.send_keys('[Runned by: {}] You don\'t have access to this command'.format(lm_author))
                            chatInput.send_keys(Keys.ENTER)
                            
    except:
        pass

driver.close()
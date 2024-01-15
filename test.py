from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()

browser.get("https://www.taptap.com/app/204923")
# time.sleep(10)

gundongz = browser.find_element(By.ID, "nc_1_n1z")

print(gundongz)

# # 解决特征识别
script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
browser.execute_script(script)


ActionChains(browser).click_and_hold(gundongz).perform()
ActionChains(browser).move_by_offset(xoffset=258, yoffset=0).perform()
ActionChains(browser).release().perform()
#

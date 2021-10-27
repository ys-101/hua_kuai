from urllib import request
from selenium import webdriver
import cv2
import random
import time
import pyautogui
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.douban.com/")

print(0)
#  进入iframe
driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="anony-reg-new"]/div/div[1]/iframe'))


time.sleep(2) #延时等待iframe加载完毕
print(0.1)

driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="username"]').send_keys('15065304811')

time.sleep(2)
driver.find_element_by_xpath('//*[@id="password"]').send_keys('sdda44665645')
time.sleep(2)
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/a').click()

# 必须阻塞几秒 要不然页面加载不出来报错
time.sleep(5)
print('休眠一会')


#  进入嵌套的iframe
driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tcaptcha_iframe"]'))



while True:
    # 从网页上获取组件
    target = driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[1]/div[2]/img')
    template = driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[1]/div[3]/img')

    # 获取模块的url路径
    src1 = target.get_attribute("src")
    src2 = template.get_attribute("src")
    # 下载图片
    request.urlretrieve(src1, "findPicimg1.jpg")
    request.urlretrieve(src2, "img2.png")

    pic1 = "findPicimg1.jpg"
    pic2 = "img2.png"

    # 读取图片
    target_rgb = cv2.imread(pic1)
    # 图片灰度化
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
    # 读取模块图片
    template_rgb = cv2.imread(pic2, 0)
    # 匹配模块位置
    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
    # 获取最佳匹配位置
    value = cv2.minMaxLoc(res)
    # 返回最佳X坐标
    x = value[2][0] - 80

    print(x)
    w1 = cv2.imread('findPicimg1.jpg').shape[1]
    w2 = target.size['width']
    print(w1, w2)
    x = x / w1 * w2
    print('x',x)

    track = []  # 移动轨迹
    current = 0  # 当前位移
    # 减速阈值
    mid = x * 4 / 5  # 前4/5段加速 后1/5段减速
    print(mid,1)
    t = 0.5  # 计算间隔
    v = 0  # 初速度
    while current < x:
        if current < mid:
            a = random.uniform(3, 5)  # 加速度随机
        else:
            a = -(random.uniform(12.5, 13.5))  # 加速度随机,负数
        v0 = v  # 初速度v0
        v = v0 + a * t  # 当前速度
        move = v0 * t + 1 / 2 * a * t * t  # 移动距离
        current += move  # 当前位移
        track.append(round(move))  # 加入轨迹


    time.sleep(1)
    slider = driver.find_elements_by_xpath(r'//*[@id="tcaptcha_drag_thumb"]')[0]
    ActionChains(driver).click_and_hold(slider).perform()
    print(track)
    for x in track:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()

    # time.sleep(1)
    ActionChains(driver).release().perform()  # 松开鼠标
    time.sleep(3)


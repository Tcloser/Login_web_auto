# -*- coding: utf-8 -*-
# [url=home.php?mod=space&uid=686208]@AuThor[/url]  : frank_lee

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import random
from selenium.webdriver import ActionChains
import time
from aip import AipOcr
import base64


class Pojie:
    def __init__(self):
        self.url = 'https://www.52pojie.cn/member.php?mod=logging&action=login'
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)  # 设置超时时间
        self.zoom = 1
    #窗口最大化
    def open(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
    #验证码识别
    def recognize_image(self):
        captcha_image = self.driver.find_element_by_xpath('//div[@class="imgCaptcha_img"]/img')#Xpath定位图片为class=imgCaptcha_img列下的img项
        captcha = captcha_image.get_attribute('src')  # 由上面指到的img项中的sre，下载图片 img src=data:image/jpg……
        fh = open("captcha.jpg", "wb")
        fh.write(base64.b64decode(captcha.split(',')[1]))
        fh.close()
        APP_ID = '16001633'
        API_KEY = 'uGXtTEz7zQLgYPidwUrHyoA9'
        SECRET_KEY = 'lhxbM94fHxcqkcxR65Lf4CZWxRRsfcaR'
        with open('./captcha.jpg', 'rb') as bin_data:
            image_data = bin_data.read()
        options = {}
        options["detect_direction"] = "false"
        options["detect_language"] = "false"
        options["probability"] = "true"
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        result = client.basicAccurate(image_data, options)
        print(result['words_result'][0]['words'])
        return result['words_result'][0]['words'].strip()

    def input_captcha(self, captcha):
        self.driver.find_element_by_xpath('//input[@id="nc_1_captcha_input"]').send_keys(captcha)#将识别到的文字传入验证码框
        time.sleep(2)
        self.driver.find_element_by_id("nc_1_scale_submit").click()  # 提交
        time.sleep(2)

        if '验证通过' in self.driver.page_source:
            self.driver.find_element_by_xpath('//*[@name="loginsubmit"]').click()
            time.sleep(3)
            print("你已成功登录，可以开始你的骚操作了")
            time.sleep(2)
            print("等一哈，我要打个卡")
            self.driver.find_element_by_css_selector("#um > p:nth-child(3) > a:nth-child(1)").click()
            print("卡都打了，你还想干什么？")
        if '_errorTEXT' in self.driver.page_source:
            # self.driver.find_element_by_xpath('//*[@id="nc_1__btn_1"]').click()
            self.driver.find_element_by_id("nc_1__btn_1").click()  # 提交
            time.sleep(3)#等一下再下载验证码
            secondcap = self.recognize_image()
            self.input_captcha(secondcap)
            time.sleep(1)
        elif '_errorTooMuch' in self.driver.page_source:
            self.driver.find_element_by_id("nc_1__btn_1").click()  # 提交
            time.sleep(3)
            secondcap = self.recognize_image()
            self.input_captcha(secondcap)
            time.sleep(1)

    def get_tracks(self, distance):
        # 初始速度
        v = 0
        # 0.2秒到0.3s之间随机生成的浮点数来统计轨迹，轨迹即0.2-0.3s内某个时间的位移
        t = random.uniform(0.2, 0.3)
        forward_tracks = []
        # 当前位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小，模拟的轨迹就越多越详细
                a = 2
            else:
                # 先加速后减速，减速时的加速度
                a = -3
            # 初速度
            v0 = v
            # 0.2-0.3秒时间内某个时间的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表,round()为保留一位小数且该小数要进行四舍五入
            forward_tracks.append(round(s))
            # 速度已经达到v，该速度作为下次的初速度
            v = v0 + a * t
        return {'forward_tracks': forward_tracks}

    def pojie_slider(self):
        try:
            distance = 300
            tracks = self.get_tracks(distance)  # 对位移的缩放计算
            self.open()
            self.driver.find_element_by_xpath('//input[@name="username"]').send_keys('输入你的账户名')
            time.sleep(1)
            self.driver.find_element_by_xpath('//input[@name="password"]').send_keys('密码')
            #time.sleep(2)
            slider = self.driver.find_element_by_xpath("//*[@id='nc_1_n1z']")
            time.sleep(1)
            ActionChains(self.driver).click_and_hold(slider).perform()
            for track in tracks['forward_tracks']:
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
            time.sleep(1)
        except Exception as e:
            print(e)
            exit(0)


if __name__ == '__main__':
    p = Pojie()
    p.pojie_slider()#先输入账号密码与验证
    captcha = p.recognize_image()#下载验证码图片
    p.input_captcha(captcha)#输入验证码图片
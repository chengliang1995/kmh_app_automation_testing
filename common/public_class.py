from appium import webdriver
import unittest
from functools import wraps
import configparser
import os
from common.logger import Logger


# 开始结束SetupTeardown
class SetupTeardown(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("class module 开始测试>>>>>>>>>>>")

    @classmethod
    def tearDownClass(cls):
        print("class module 测试结束>>>>>>>>>>>>\n")

    def setUp(self):
        print("setup begin test")

    def tearDown(self):
        print("teardown test end!")


# 跳过测试用例的装饰器
def skip_dependon(depend=""):
    """
    :param depend: 依赖的用例函数名，默认为空
    :return: wraper_func
    """

    def wraper_func(test_func):
        @wraps(test_func)  # @wraps：避免被装饰函数自身的信息丢失
        def inner_func(self):
            if depend == test_func.__name__:
                raise ValueError("{} cannot depend on itself".format(depend))
            # print("self._outcome", self._outcome.__dict__)
            # 此方法适用于python3.4 +
            # 如果是低版本的python3，请将self._outcome.result修改为self._outcomeForDoCleanups
            # 如果你是python2版本，请将self._outcome.result修改为self._resultForDoCleanups
            failures = str([fail[0] for fail in self._outcome.result.failures])
            errors = str([error[0] for error in self._outcome.result.errors])
            skipped = str([error[0] for error in self._outcome.result.skipped])
            flag = (depend in failures) or (depend in errors) or (depend in skipped)
            if failures.find(depend) != -1:
                # 输出结果 [<__main__.TestDemo testMethod=test_login>]
                # 如果依赖的用例名在failures中，则判定为失败，以下两种情况同理
                # find()方法：查找子字符串，若找到返回从0开始的下标值，若找不到返回 - 1
                test = unittest.skipIf(flag, "{} failed".format(depend))(test_func)
            elif errors.find(depend) != -1:
                test = unittest.skipIf(flag, "{} error".format(depend))(test_func)
            elif skipped.find(depend) != -1:
                test = unittest.skipIf(flag, "{} skipped".format(depend))(test_func)
            else:
                test = test_func
            return test(self)
        return inner_func
    return wraper_func


# 获取config.ini文件中的配置数据
class Config:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0]) + '/config/config.ini'

    def get_config(self, section, key=None):
        """
        :param section: section
        :param key: key传了就以字符串格式返回指定key的数据，未传就列表形式返回当前section下的所有数据
        格式如下：[('test_url', 'https://www.kanman.com'), ('account', '15928152911'), ('password', '1234abcd')]
        :return:
        """
        self.config.read(self.path, encoding="utf-8-sig")
        if key:
            config = self.config.get(section, key)
            if config == "True" or config == "true":
                config = True
            if config == "False" or config == "false":
                config = False
        else:
            config = self.config.items(section)
            length = len(config)
            for i in range(length):
                config[i] = list(config[i])  # tuple转为list
            for i in range(length):
                if config[i][1] == "True" or config[i][1] == "true":
                    config[i][1] = True
                if config[i][1] == "False" or config[i][1] == "false":
                    config[i][1] = False
        return config


# 打开app
class OpenApp:
    """获取配置信息打开app"""

    @staticmethod
    def open():
        desired_caps = dict()
        # 配置android系统信息 测试机HUAWEI Mate 20
        section = "app_config_HUAWEI Mate 20"
        desired_caps["platformName"] = con.get_config(section=section, key="platformName")
        desired_caps["deviceName"] = con.get_config(section=section, key="deviceName")
        desired_caps["platformVersion"] = con.get_config(section=section, key="platformVersion")
        desired_caps["udid"] = con.get_config(section=section, key="udid")

        # 配置app包信息
        section = "app_config_package"

        # 取第一个文件
        apk_path = os.getcwd() + "/apk/"
        file_list = list(os.listdir(apk_path))  # ['com.wbxm.icartoon_2.4.5_1904172233.apk']
        for i in range(0, len(file_list)):
            file_list[i] = apk_path + file_list[i]
        if len(file_list) > 0:
            desired_caps["app"] = file_list[0]  # 取第一个apk

        desired_caps["appPackage"] = con.get_config(section=section, key="appPackage")
        desired_caps["appActivity"] = con.get_config(section=section, key="appActivity")  # 首次安装启动的activity

        # 配置其他信息
        section = "app_config_other"
        desired_caps["noSign"] = con.get_config(section=section, key="noSign")  # 不需要再次签名
        desired_caps["noReset"] = con.get_config(section=section, key="noReset")  # 启动app时是否清除app里的原有的数据
        # desired_caps["unicodeKeyboard"] = con.get_config(section=section, key="unicodeKeyboard")  # 键盘输入中文
        # 设置之后会有Appium的输入法守护来执行输入操作
        # desired_caps["unicodeKeyboard"] = con.get_config(section=section, key="unicodeKeyboard")
        # 使用哪个自动化引擎默认为appium，这里修改后用于识别toast内容
        desired_caps["automationName"] = con.get_config(section=section, key="automationName")

        # 启动app
        app_driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
        # app_driver.implicitly_wait(10)  # implicitly_wait(5)隐式等待，5秒钟内只要找到了元素就开始执行，5秒钟后未找到，就超时
        return app_driver

# create a logger instance
logger = Logger(logger="BasePage")
con = Config()
driver = OpenApp.open()


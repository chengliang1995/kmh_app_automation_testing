import time
import os.path
from common.public_class import *
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from appium.webdriver.common.touch_action import TouchAction


class BasePage(object):
    """
    定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法到这个类
    """
    def __init__(self, driver):
        self.driver = driver

    # 保存图片
    def get_screenshot(self, error_info="error_info"):
        """
        :param error_info: 错误信息或者是操作信息
        :return:
        """
        file_path = os.getcwd() + "/screenshots/"
        rq = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))  # 2019-01-09_15-12-47
        # 文件名中不能有\/:*?"<>|符号，所以替换为"_"
        error_info = error_info.replace("=>", "_").replace("\\", "_").replace("/", "_")\
            .replace(":", "_").replace("*", "_").replace("'", "_")
        error_info = error_info.replace("?", "_").replace("\"", "_")\
            .replace("<", "_").replace(">", "_").replace("|", "_")

        screen_name = rq + "_" + error_info + ".png"  # 截图命名 2019-01-09_15-14-12_XXX.png
        full_path = file_path + screen_name  # 截图命名 2019-01-09_15-14-12_XXX.png
        try:
            self.driver.get_screenshot_as_file(full_path)
            logger.info("截图--%s报错,图片名--%s" % (error_info, screen_name))
        except NameError as e:
            logger.error("%s截图失败，reason: %s" % (error_info, e))

    # 直接定位元素方法
    def find_element(self, selector, parent_element=None, isshow_error="yes"):
        """
         (ps:这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位)
        :param selector: 格式 "id=>kw"
        :param parent_element: 传入父元素，则找此父元素的子元素
        :param isshow_error: 控制未找到元素时是否报错，默认为yes--error级别报错且截图，no--warning级别报错不截图
        :return: element
        """
        element = None
        driver_or_el = parent_element if parent_element else self.driver
        if "=>" not in selector:
            # 如无=>符号，默认使用id方式查找
            return driver_or_el.find_element_by_id(selector)
        selector_by = selector.split("=>")[0]
        selector_value = selector.split("=>")[1]
        try:
            if selector_by == "i" or selector_by == "id":
                element = driver_or_el.find_element_by_id(selector_value)
            elif selector_by == "c" or selector_by == "class":
                element = driver_or_el.find_element_by_class_name(selector_value)
            elif selector_by == "x" or selector_by == "xpath":
                element = driver_or_el.find_element_by_xpath(selector_value)
            else:
                raise NameError("Please enter a valid type of target elements.")
        except Exception as e:
            if isshow_error == "yes":
                logger.error("find element failed, reason: %s" % e)
                self.get_screenshot(error_info="find_element_failed_%s_%s" % (selector_by, selector_value))
            elif isshow_error == "no":
                logger.warning("find element failed, reason: %s" % e)
            else:
                raise Exception("isshow_error parameter must be yes or no!")
        else:
            logger.info("Had find the element successful by %s value: %s "
                        % (selector_by, selector_value))
        return element

    # 定位多个相同元素方法
    def find_elements(self, selector, parent_element=None, isshow_error=0):
        """
         这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         submit_btn = "id=>su"
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
        :param selector: 格式 "id=>kw"
        :param parent_element: 传入父元素，则找此父元素的子元素
        :param isshow_error: 控制未找到元素时是否报错，默认为0---报错，1---不报错
        :return: elements，返回一个element的list列表
        """
        elements = None
        driver_or_el = parent_element if parent_element else self.driver
        if "=>" not in selector:
            # 如无=>符号，默认使用id方式查找
            return driver_or_el.find_elements_by_id(selector)
        selector_by = selector.split("=>")[0]
        selector_value = selector.split("=>")[1]
        try:
            if selector_by == "i" or selector_by == "id":
                elements = driver_or_el.find_elements_by_id(selector_value)
            elif selector_by == "c" or selector_by == "class":
                elements = driver_or_el.find_elements_by_class_name(selector_value)
            elif selector_by == "x" or selector_by == "xpath":
                elements = driver_or_el.find_elements_by_xpath(selector_value)
            else:
                raise NameError("Please enter a valid type of targeting elements.")
        except Exception as e:
            if isshow_error == 0:
                logger.error("find elements failed, reason: %s" % e)
                self.get_screenshot(error_info="find_elements_%s_%s" % (selector_by, selector_value))  # 截图
        else:
            logger.info("Had find the elements successful by %s value: %s "
                        % (selector_by, selector_value))
        return elements

    # 直接定位元素方法
    def find_element_by_uiautomator(self, selector, parent_element=None, isshow_error=0):
        """
         (ps:这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位)
        :param selector: 格式 "id=>kw"
        :param parent_element: 传入父元素，则找此父元素的子元素
        :param isshow_error: 控制未找到元素时是否报错，默认为0---报错，1---不报错
        :return: element
        """
        element = None
        driver_or_el = parent_element if parent_element else self.driver
        if "=>" not in selector:
            # 如无=>符号，默认使用id方式查找
            return driver_or_el.find_element_by_id(selector)
        selector_by = selector.split("=>")[0]
        selector_value = selector.split("=>")[1]
        try:
            if selector_by == "i" or selector_by == "id":
                element = driver_or_el.find_element_by_android_uiautomator(
                    "new UiSelector().resourceId(%s)" % selector_value)
            elif selector_by == "c" or selector_by == "class":
                element = driver_or_el.find_element_by_android_uiautomator(
                    "new UiSelector().className(%s)" % selector_value)
            elif selector_by == "t" or selector_by == "text":
                element = driver_or_el.find_element_by_android_uiautomator("new UiSelector().text(%s)" % selector_value)
            else:
                raise NameError("Please enter a valid type of target elements.")
        except Exception as e:
            if isshow_error == 0:
                logger.error("find element failed, reason: %s" % e)
                self.get_screenshot(
                    error_info="find_element_failed_%s_%s" % (selector_by, selector_value))  # take screenshot
        else:
            logger.info("Had find the element successful by %s value: %s "
                        % (selector_by, selector_value))
        return element

    # 定位多个相同元素方法
    def find_elements_by_uiautomator(self, selector, parent_element=None, isshow_error=0):
        """
         (ps:这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位)
        :param selector: 格式 "id=>kw"
        :param parent_element: 传入父元素，则找此父元素的子元素
        :param isshow_error: 控制未找到元素时是否报错，默认为0---报错，1---不报错
        :return: element
        """
        elements = None
        driver_or_el = parent_element if parent_element else self.driver
        if "=>" not in selector:
            # 如无=>符号，默认使用id方式查找
            return driver_or_el.find_elements_by_id(selector)
        selector_by = selector.split("=>")[0]
        selector_value = selector.split("=>")[1]
        try:
            if selector_by == "i" or selector_by == "id":
                elements = driver_or_el.find_elements_by_android_uiautomator(
                    "new UiSelector().resourceId(%s)" % selector_value)
            elif selector_by == "c" or selector_by == "class":
                elements = driver_or_el.find_elements_by_android_uiautomator(
                    "new UiSelector().className(%s)" % selector_value)
            elif selector_by == "t" or selector_by == "text":
                elements = driver_or_el.find_elements_by_android_uiautomator("new UiSelector().text(%s)" % selector_value)
            else:
                raise NameError("Please enter a valid type of target elements.")
        except Exception as e:
            if isshow_error == 0:
                logger.error("find elements failed, reason: %s" % e)
                self.get_screenshot(
                    error_info="find_elements_failed_%s_%s" % (selector_by, selector_value))  # take screenshot
        else:
            logger.info("Had find the elements successful by %s value: %s "
                        % (selector_by, selector_value))
        return elements

    # 输入文本
    def input_text(self, selector=None, element=None, text=""):

        if selector:
            el = self.find_element(selector)
        elif element:
            el = element
        else:
            raise Exception("Parameter incoming error!")
        el.clear()
        try:
            el.send_keys(text)
            logger.info("Had input text \' %s \' in inputBox" % text)
        except NameError as e:
            logger.error("Failed to input text in input box with %s" % e)
            self.get_screenshot(selector)

    # 清除文本框
    def clear(self, selector, element):
        """
        清除文本框
        :param selector: 传入格式 "id=>kw"
        :param element:  传入element
        :return: 无
        """
        if selector:
            el = self.find_element(selector)
        elif element:
            el = element
        else:
            el = ""
            logger.error("调用clear函数传入参数错误")
        try:
            el.clear()
            logger.info("Clear text in input box before input.")
        except NameError as e:
            logger.error("Failed to clear in input box with %s" % e)
            self.get_screenshot("clear fail")

    # 点击元素
    def element_click(self, selector=None, element=None, log_msg="element"):
        """
        可选择传入selector或者元素element，传入element时需传入log_msg作为打印日志的信息
        :param selector:
        :param element:
        :param log_msg: 传入element时需传入log_msg作为打印日志的信息
        :return:
        """
        if selector:
            el = self.find_element(selector)
        else:
            el = element
        try:
            el.click()
            logger.info("The element \" %s \" was clicked." % (selector if selector else log_msg))
        except Exception as e:
            logger.error("Failed to click the element \" %s \", reason: %s" % ((selector if selector else log_msg), e))
            self.get_screenshot("click_%s" % (selector if selector else log_msg))

    # 一直等待某个元素消失，默认超时10秒
    def is_not_visible(self, locator, timeout=10):
        """
        一直等待某个元素消失，默认超时10秒
        :param locator: 元素定位方式 格式：(By.CLASS_NAME, "layer-custom-text")
        :param timeout: 超时时间
        :return: 成功---True  失败--False
        """
        try:
            ui.WebDriverWait(self.driver, timeout).until_not(EC.visibility_of_element_located(locator))
            logger.info("successfully to wait locator \"%s\" is not visible in %ss" % (locator, timeout))
            return True
        except TimeoutException:
            logger.warning(msg="fail to wait locator \"%s\" is not visible in %ss" % (locator, timeout))
            self.get_screenshot(error_info="wait not visible %s time out" % str(locator))
            return False

    # 一直等待某元素可见
    def is_visible(self, locator, text=None, text_type="text", timeout=10, isshow_error="yes"):
        """
        一直等待某元素可见，默认超时10秒
        此方法会先判定元素是否出现，元素出现后再判定其text/content-desc值是否包含传入的text，包含则成功，不包含则失败
        :param locator: 元素定位方式 格式：(By.CLASS_NAME, "layer-custom-text")
        :param text: 等待的元素的文本，text为空则表示只等待元素是否出现，
        不为空则表示需判断出现的元素的text值包含传入的text值（注意：是包含关系，出现元素的text>=传入text即可）
        主要用于toast弹窗上的文字
        :param text_type: 判断文本的方法，text--元素的text，content-desc--元素的content-desc属性
        :param timeout: 超时时间
        :param isshow_error: 没找到元素时是否报错截图，yes--error级别报错且截图，no--warning级别报错不截图
        :return: 成功---返回找到的el  失败--返回None
        """
        toast_el = None
        try:
            toast_el = ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except:
            # 没找到的情况
            if isshow_error == "yes":
                logger.error(msg="fail to wait locator \"%s\" is visible in %ss" % (str(locator), timeout))
                self.get_screenshot(error_info="fail to wait visible %s" % str(locator))
            elif isshow_error == "no":
                logger.warning(msg="fail to wait locator \"%s\" is visible in %ss" % (str(locator), timeout))
            else:
                raise Exception("isshow_error must be yes or no.")
        else:  # 等到元素显示出来
            if text:
                if text_type == "text":
                    if text in toast_el.text:
                        logger.info(msg="success to wait locator \"%s\" is visible" % str(locator))
                    else:
                        if isshow_error == "yes":
                            logger.error(
                                msg="success to wait locator \"%s\" is visible, but text %s is not in the element"
                                    % (str(locator), text))
                            self.get_screenshot(error_info="text %s is not in the element" % text)
                        elif isshow_error == "no":
                            logger.warning(
                                msg="success to wait locator \"%s\" is visible, but text %s is not in the element"
                                    % (str(locator), text))
                        else:
                            raise Exception("isshow_error must be yes or no.")
                elif text_type == "content-desc":
                    if text in toast_el.get_attribute("contentDescription"):
                        logger.info(msg="success to wait locator \"%s\" is visible" % str(locator))
                    else:
                        if isshow_error == "yes":
                            logger.error(msg="success to wait locator \"%s\" is visible,"
                                             " but content-desc %s is not in the element"
                                             % (str(locator), text))
                            self.get_screenshot(error_info="text %s is not in the element" % text)
                        elif isshow_error == "no":
                            logger.warning(msg="success to wait locator \"%s\" is visible,"
                                               " but content-desc %s is not in the element"
                                             % (str(locator), text))
                        else:
                            raise Exception("isshow_error must be yes or no.")
                else:
                    raise Exception("text_type must be text or content-desc")
            else:
                logger.info("success to wait locator \"%s\" is visible" % str(locator))
        return toast_el

    # 获取屏幕宽度和高度
    def get_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        logger.info("获取屏幕size，(%s,%s)" % (x, y))
        return x, y

    # 滑动屏幕
    def swipe_window(self, direction="left", distance: int=6, begin_location=0.2, swipe_time=1000):
        """
        滑动屏幕
        :param direction: 滑动的方向，left、right、up、down
        :param distance: 滑动的距离，数值1-9，例：1代表滑动屏幕长或宽的0.1倍，默认为6，即从0.2滑动到0.8的位置
        :param begin_location: 从距离上下左右的多少倍开始滑动，默认0.2
        :param swipe_time: 滑动的时间，单位ms
        :return: 无
        """
        if (begin_location + 0.1*distance) > 1:
            raise Exception("移动距离超过屏幕最大长度了！")
        l = self.get_size()
        if direction == "left":
            x1 = int(l[0] * (1-begin_location))
            y1 = int(l[1] * 0.5)
            x2 = int(l[0] * ((1-begin_location) - 0.1*distance))
            self.driver.swipe(x1, y1, x2, y1, duration=swipe_time)  # 向左滑动
            logger.info("向左滑动，(%s,%s)->(%s,%s)" % (x1, y1, x2, y1))
        elif direction == "right":
            x1 = int(l[0] * begin_location)
            y1 = int(l[1] * 0.5)
            x2 = int(l[0] * (begin_location + 0.1*distance))
            self.driver.swipe(x1, y1, x2, y1, duration=swipe_time)  # 向右滑动
            logger.info("向右滑动，(%s,%s)->(%s,%s)" % (x1, y1, x2, y1))
        elif direction == "up":
            x1 = int(l[0] * 0.5)
            y1 = int(l[1] * (1-begin_location))
            y2 = int(l[1] * ((1-begin_location) - 0.1*distance))
            self.driver.swipe(x1, y1, x1, y2, duration=swipe_time)  # 向上滑动
            logger.info("向上滑动，(%s,%s)->(%s,%s)" % (x1, y1, x1, y2))
        elif direction == "down":
            x1 = int(l[0] * 0.5)
            y1 = int(l[1] * begin_location)
            y2 = int(l[1] * (begin_location+0.1*distance))
            self.driver.swipe(x1, y1, x1, y2, duration=swipe_time)  # 向下滑动
            logger.info("向下滑动，(%s,%s)->(%s,%s)" % (x1, y1, x1, y2))
        else:
            raise Exception("direction parameter must be left/right/up/down")

    # 普通滑动
    def swipe(self, x1, y1, x2, y2, swipe_time=1000):
        self.driver.swipe(x1, y1, x2, y2, duration=swipe_time)
        logger.info("滑动，(%s,%s)->(%s,%s)" % (x1, y1, x1, y2))

    # 点击屏幕坐标位置
    def touch_tap(self, percentage_x, percentage_y, duration=100):
        """
        以百分比算出屏幕坐标位置，兼容不同分辨率手机
        :param percentage_x:  x坐标与屏幕宽度的百分比
        :param percentage_y:  y坐标与屏幕长度的百分比
        :param duration: 点击持续时间 默认0.1s
        :return:
        """
        l = self.get_size()
        x = int(round(percentage_x, 2)*l[0])
        y = int(round(percentage_y, 2)*l[1])
        self.driver.tap([(x, y)], duration=duration)
        logger.info("点击坐标(%s,%s)" % (x, y))

    # 点击手机物理按键
    def keyevent(self, keycode):
        self.driver.keyevent(keycode)
        logger.info("点击手机物理按键keycode=%d" % keycode)


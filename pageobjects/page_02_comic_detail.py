from common.base_page import *
from selenium.webdriver.common.by import By
import time


class DetailPage(BasePage):

    # 点击斗罗大陆,从搜索页进入漫画详情页
    def goto_comic_detail_page(self):
        for i in range(6):
            el = self.find_element(selector="id=>com.wbxm.icartoon:id/tv_comic_name%s" % (i+1))
            comic_name = con.get_config(section="comic_detail_config", key="comic_name")
            if el.text == comic_name:
                self.element_click(element=el, log_msg=comic_name)
                break

    # 跳过引导
    def skip_guide(self):
        text_list = ["下一步", "朕知道了"]
        for i in range(len(text_list)):
            guide_text = text_list[i]
            next_el = self.is_visible(locator=(By.ID, "com.wbxm.icartoon:id/tv_next"), text=guide_text, isshow_error="no")
            if not next_el:
                logger.warning("未找到详情页引导--%s" % guide_text)
                return
            self.element_click(element=next_el, log_msg=guide_text)
            time.sleep(1)

    # 找到封面图上的漫画名
    def find_comic_name(self):
        return self.find_element(selector="id=>com.wbxm.icartoon:id/tv_name").text

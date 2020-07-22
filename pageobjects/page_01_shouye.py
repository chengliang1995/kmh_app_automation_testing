from common.base_page import *
from selenium.webdriver.common.by import By
import time


class ShouYe(BasePage):

    # 点 始终允许
    def click_allow_btn(self):
        for i in range(2):
            # 此id适用于HUAWEI Mate 20
            allow_el = self.is_visible(
                locator=(By.ID, "com.android.packageinstaller:id/permission_allow_button"),
                isshow_error="no")  # 等待始终允许显示出来
            if allow_el:
                self.element_click(element=allow_el, log_msg="始终允许btn")
                time.sleep(0.5)
            else:
                logger.warning("未找到系统权限弹窗中的始终允许按钮")

    # 点开启二次元
    def click_open_ecy(self):
        self.element_click(selector="id=>com.wbxm.icartoon:id/btn_go")

    # 点击首页引导
    def click_shouye_guide(self, first_or_not="first"):
        if first_or_not == "first":
            guide_dic = [{"locator": (By.ID, "com.wbxm.icartoon:id/tv_close"), "time": 3, "msg": "首页插屏广告"},
                         {"locator": (By.ID, "com.wbxm.icartoon:id/canGuideView"), "time": 3, "msg": "首页小喇叭引导"},
                         {"locator": (By.ID, "com.wbxm.icartoon:id/tv_cancel"), "time": 3, "msg": "首页漫画更新弹窗"}]
        else:
            guide_dic = [{"locator": (By.XPATH, "//android.widget.TextView[@text='跳过']"), "time": 6, "msg": "首页开屏广告"},
                         {"locator": (By.ID, "com.wbxm.icartoon:id/tv_close"), "time": 3, "msg": "首页插屏广告"},
                         {"locator": (By.ID, "com.wbxm.icartoon:id/tv_cancel"), "time": 3, "msg": "首页漫画更新弹窗"}]
        for i in range(len(guide_dic)):
            msg = guide_dic[i]["msg"]
            logger.info("开始查找%s..." % msg)
            tv_el = self.is_visible(locator=guide_dic[i]["locator"], timeout=guide_dic[i]["time"], isshow_error="no")
            if tv_el:
                logger.info("已查找到%s" % msg)
                self.element_click(element=tv_el, log_msg=msg)
            else:
                logger.warning("未找到%s！！" % msg)

    # 点击 首页
    def click_shouye(self):
        self.element_click(selector="id=>com.wbxm.icartoon:id/iv_tab3")

    # 首页书单数据
    def find_book_list(self):
        book_view_el = self.find_element(selector="id=>com.wbxm.icartoon:id/can_content_view")
        book_list_el = self.find_elements(selector="xpath=>.//android.widget.RelativeLayout",
                                          parent_element=book_view_el)
        return book_list_el

    # 点击 我的
    def click_wode(self):
        self.element_click(selector="id=>com.wbxm.icartoon:id/iv_tab5")

    # 跳过 我的 引导
    def skip_my_guide(self):
        time.sleep(1)
        logger.info("开始查找 我的页面引导...")
        el = self.is_visible(
            locator=(By.XPATH,
                     "//android.widget.LinearLayout/android.widget.TextView[@text='消息大改版，快跟好友互动起来吧～']"),
            timeout=3,
            isshow_error="no")
        if el:
            self.element_click(element=el, log_msg="我的 页面引导")
        else:
            logger.warning("未找到我的页面引导")

    # 点头像跳转登录界面
    def click_touxiang(self):
        self.element_click(selector="id=>com.wbxm.icartoon:id/iv_avatar")

    # 输入账号密码登录
    def login(self):
        self.element_click(selector="id=>com.wbxm.icartoon:id/tv_login_switch")  # 切换登录方式为账号密码登录
        time.sleep(0.5)
        account = con.get_config(section="user_account_config", key="account")
        password = con.get_config(section="user_account_config", key="password")
        self.input_text(selector="id=>com.wbxm.icartoon:id/et_user_account", text=account)  # 输入账号
        time.sleep(0.5)
        self.input_text(selector="id=>com.wbxm.icartoon:id/et_user_pwd", text=password)  # 输入密码
        time.sleep(0.5)
        self.element_click(selector="id=>com.wbxm.icartoon:id/btn_login")  # 点击登录

    # 获取用户签名
    def get_user_signature(self):
        time.sleep(1)

        # 跳过漫画更新弹窗
        logger.info("开始查找漫画更新弹窗...")
        comic_update_el = self.is_visible(
            locator=(By.ID, "com.wbxm.icartoon:id/tv_cancel"), timeout=3, isshow_error="no")  # 等漫画更新弹窗弹出
        if comic_update_el:
            self.element_click(element=comic_update_el, log_msg="漫画更新弹窗的不用了按钮")
        else:
            logger.warning("未找到漫画更新弹窗")

        # 查签名
        sign_el = self.find_element(selector="id=>com.wbxm.icartoon:id/tv_signature")
        sign_text = sign_el.text

        # 查用户名
        # user_name_el = self.find_element(selector="id=>com.wbxm.icartoon:id/tv_user_name")
        # user_name = user_name_el.text
        return sign_text

    # 点击排行，进入排行榜
    def click_rank(self):
        self.element_click(selector="id=>com.wbxm.icartoon:id/iv_action_des_1")

    # 等待排行榜界面顶部10个排行table显示出来
    def wait_rank_is_visible(self):
        el = self.is_visible(locator=(By.ID, "com.wbxm.icartoon:id/sort_type_list"))
        rank_list = self.find_elements(selector="class=>android.widget.TextView", parent_element=el)
        return rank_list

    # 等待下方数据显示出来
    def wait_rank_data_is_visible(self):
        scroll_view_el = self.find_element(selector="id=>com.wbxm.icartoon:id/can_scroll_view")
        data_els = self.find_elements(selector="class=>android.widget.RelativeLayout",
                                      parent_element=scroll_view_el)
        if len(data_els) >= 4:  # 小屏幕下面的数据至少能显示两个漫画，由于每个漫画下有两个RelativeLayout，所以以4为分界
            return True
        else:
            return False


class SearchPage(BasePage):
    # 点击搜索按钮
    def click_search_btn(self):
        self.element_click(selector="id=>com.wbxm.icartoon:id/iv_search")

    # 等待 大家都在搜的结果显示出来
    def wait_top_search_is_visible(self):
        locator = (By.XPATH, "//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.TextView")
        return self.is_visible(locator=locator)

    # 输入搜索内容
    def input_search_key(self):
        self.input_text(selector="id=>com.wbxm.icartoon:id/et", text="斗")

    # 等待联想搜索结果显示出来
    def wait_lianxiang_search_list_is_visible(self):
        locator = (By.XPATH, "//android.support.v7.widget.RecyclerView/android.widget.LinearLayout")
        return self.is_visible(locator=locator)

    # 等待熟悉app操作任务弹窗弹出
    def wait_task_is_visible(self):
        return self.is_visible(locator=(By.ID, "com.wbxm.icartoon:id/tv_task_name"),
                               text="熟悉APP操作",
                               text_type="text",
                               timeout=5,
                               isshow_error="no")

    # 领取奖励
    def receive_awards(self):
        self.element_click(selector="xpath=>//android.widget.TextView[@text='领取奖励']")

    # 等待领取奖励成功的弹窗弹出并关闭弹窗
    def receive_awards_toast(self):
        el = self.is_visible(locator=(By.ID, "com.wbxm.icartoon:id/recycler"))
        if el:
            self.keyevent(4)  # 点返回按键，是奖励弹窗消失
            time.sleep(0.5)
            return True
        else:
            return False

    # 关闭任务弹窗
    def close_task(self):
        self.element_click(selector="id=>com.wbxm.icartoon:id/iv_close")

    # 等待升级弹窗弹出，并关闭弹窗
    def close_update_window(self):
        el = self.is_visible(locator=(By.ID, "com.wbxm.icartoon:id/ll_update"), isshow_error="no", timeout=5)
        if el:
            self.keyevent(4)  # 点返回按键，关闭弹窗
        else:
            logger.warning("没有找到升级弹窗")

    # 4个搜素结果的title，相关漫画、相关用户、相关圈子、相关帖子
    def find_4_search_result_title(self):
        el_id = ["com.wbxm.icartoon:id/tv_comic_title",
                 "com.wbxm.icartoon:id/tv_author_title",
                 "com.wbxm.icartoon:id/tv_star_title",
                 "com.wbxm.icartoon:id/tv_star_child_title"]
        comic_title_el = self.find_element(selector="id=>%s" % el_id[0], isshow_error="no")
        user_title_el = self.find_element(selector="id=>%s" % el_id[1], isshow_error="no")
        quanzi_title_el = self.find_element(selector="id=>%s" % el_id[2], isshow_error="no")
        tiezi_title_el = self.find_element(selector="id=>%s" % el_id[3], isshow_error="no")
        if not comic_title_el:
            msg = "未找到相关漫画"
            logger.warning(msg)
            self.get_screenshot(msg)
            return False
        if not user_title_el:
            msg = "未找到相关用户"
            logger.warning(msg)
            self.get_screenshot(msg)
            return False
        if not quanzi_title_el:
            logger.warning("未找到相关圈子，向上滑动一次，再次查找")
            self.swipe_window(direction="up", distance=4, begin_location=0.1)
            quanzi_title_el = self.find_element(selector="id=>%s" % el_id[2], isshow_error="no")
            tiezi_title_el = self.find_element(selector="id=>%s" % el_id[3], isshow_error="no")
            if not quanzi_title_el:
                msg = "未找到相关圈子"
                logger.info(msg)
                self.get_screenshot(msg)
                return False
        if not tiezi_title_el:
            logger.warning("未找到相关帖子，向上滑动一次，再次查找")
            self.swipe_window(direction="up", distance=4, begin_location=0.1)
            time.sleep(1)
            tiezi_title_el = self.find_element(selector="id=>%s" % el_id[3], isshow_error="no")
            if not tiezi_title_el:
                msg = "未找到相关帖子"
                logger.error(msg)
                self.get_screenshot(msg)
                return False
        return True

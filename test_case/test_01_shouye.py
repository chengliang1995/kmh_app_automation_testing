from pageobjects.page_01_shouye import *
from utx import *

shouye = ShouYe(driver=driver)
search_page = SearchPage(driver=driver)


class Test01ShouYe(SetupTeardown):
    """首页相关操作"""

    @tag(Tag.SMOKE)
    def test_first_start_app_skip_guide(self):
        """测试启动qpp跳过引导"""
        first_or_not = con.get_config(section="app_config_other", key="noReset")  # noRest为false，则为首次启动，true为非首次
        if not first_or_not:
            shouye.click_allow_btn()  # 点击始终允许
            time.sleep(0.5)
            for i in range(2):
                shouye.swipe_window(direction="left")  # 左滑
                time.sleep(0.5)
            shouye.click_open_ecy()  # 点 开启二次元
            time.sleep(0.5)
            shouye.touch_tap(percentage_x=0.5, percentage_y=2108/2163)  # 点就不告诉你
            time.sleep(1)
        shouye.click_shouye_guide(first_or_not="first" if not first_or_not else "second")  # 首页及开屏广告相关引导

    def test_getbookbytype(self):
        """首页书单数据"""
        self.assertTrue(shouye.find_book_list())

    @tag(Tag.SMOKE)
    def test_login(self):
        """账号密码登录"""
        shouye.click_wode()  # 点 我的
        shouye.skip_my_guide()  # 跳过我的引导
        shouye.click_touxiang()  # 点头像跳转登录界面
        shouye.login()  # 输入账号密码登录
        sign_text = shouye.get_user_signature()  # 获取用户签名信息
        self.assertNotIn("游客ID:", sign_text)  # 用户签名中没有 游客ID: 这几个字 则判断登录成功

    @skip_dependon(depend="getbookbytype")
    def test_rank(self):
        """排行榜"""
        shouye.click_shouye()  # 点击 跳转到首页
        shouye.click_rank()  # 点击首页排行
        rank_list = shouye.wait_rank_is_visible()
        self.assertTrue(rank_list)
        self.assertTrue(shouye.wait_rank_data_is_visible())  # 等待下方数据显示出来
        num = len(rank_list)
        for i in range(1, num):
            shouye.element_click(element=rank_list[i], log_msg=rank_list[i].text)
            # shouye.is_visible(locator=(By.XPATH, "//*[@text='正在接入M27星球...请稍后']"))
            # shouye.is_not_visible(locator=(By.XPATH, "//*[@text='正在接入M27星球...请稍后']"))
            # 识别不了toast，这里以2s等待代替
            time.sleep(2)
            if shouye.wait_rank_data_is_visible():  # 等待下方数据显示出来
                self.assertTrue(True)
                rank_list = shouye.wait_rank_is_visible()  # 点击后需重新获取才能点到下一个
                if i == (num-1):
                    search_page.keyevent(keycode=4)  # 从排行榜界面返回首页，以便后续测试
            else:
                search_page.keyevent(keycode=4)  # 从排行榜界面返回首页，以便后续测试
                time.sleep(0.5)
                self.assertTrue(False)


class Test02Search(SetupTeardown):
    """搜索相关"""

    @tag(Tag.SMOKE)
    @skip_dependon(depend="login")
    def test_top_search(self):
        """大家都在搜数据"""
        shouye.click_shouye()
        search_page.click_search_btn()
        self.assertTrue(search_page.wait_top_search_is_visible())

    # @tag(Tag.SMOKE)
    @skip_dependon(depend="top_search")
    def test_lianxiang_search(self):
        """联想搜索"""
        search_page.input_search_key()  # 输入搜索文字
        self.assertTrue(search_page.wait_lianxiang_search_list_is_visible())  # 等待联想搜索显示出来

    @tag(Tag.SMOKE)
    @skip_dependon(depend="top_search")
    def test_search_result(self):
        """搜索结果页数据"""
        search_page.input_search_key()  # 输入搜索文字
        search_page.keyevent(66)  # 点击手机回车物理按键

        # 搜索任务逻辑
        task_is_visible = search_page.wait_task_is_visible()  # 等待熟悉app任务弹窗弹出
        if task_is_visible:
            search_page.receive_awards()  # 领取奖励
            self.assertTrue(search_page.receive_awards_toast())  # 等待领取奖励成功的弹窗弹出并关闭弹窗
            search_page.close_task()  # 关闭任务弹窗
            search_page.close_update_window()  # 关闭升级弹窗
        else:
            logger.warning("未找到熟悉app任务弹窗")

        # 搜索的4个结果
        status = search_page.find_4_search_result_title()
        search_page.swipe_window(direction="down", distance=7)  # 无论有没有找到，都向下滑动到屏幕最顶部
        time.sleep(1)  # 等1s，等滑动停止
        self.assertTrue(status)


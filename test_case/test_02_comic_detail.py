from utx import *
from pageobjects.page_02_comic_detail import *

detail_page = DetailPage(driver)


class Test01Detail(SetupTeardown):
    """漫画详情页"""

    @tag(Tag.SMOKE)
    @skip_dependon(depend="search_result")
    def test_goto_comic_detail(self):
        """进入漫画详情页"""
        detail_page.goto_comic_detail_page()  # 进入漫画详情页
        detail_page.skip_guide()  # 跳过引导
        comic_name = con.get_config(section="comic_detail_config", key="comic_name")
        self.assertEqual(detail_page.find_comic_name(), comic_name)

import utx
import logging
from clear_report_file import *
import sys
# 加入这句话使此程序可在cmd下运行，不需要打开pycharm
path = os.getcwd() + "/run_test.py"
sys.path.append(path)

# 创建一个bat文件，命令如下，第三行为run_test.py文件所在的目录
# @echo off
# d:
# cd D:\git\kmh_app_automation_testing
# python run_test.py
# pause

if __name__ == '__main__':

    # 使用的utx库为0.0.6版本
    create_report_dirs()  # 创建存放测试结果的report、logs、screenshots三个文件夹，如已有则不创建
    clear_report_files()  # 清除所有的测试报告

    # utx.setting.run_case = {utx.Tag.ALL}  # 运行全部测试用例--utx V0.0.6适用
    utx.setting.run_case = {utx.Tag.SMOKE}   # 只运行SMOKE标记的测试用例--utx V0.0.6适用
    # utx.setting.run_case = {utx.Tag.SMOKE, utx.Tag.V1_0_0}   # 只运行SMOKE和V1_0_0标记的测试用例--utx V0.0.6适用

    utx.setting.check_case_doc = False  # 关闭检测是否编写了测试用例描述
    utx.setting.full_case_name = True  # 显示完整用例名字（函数名字+参数信息）
    utx.setting.max_case_name_len = 60  # 测试报告内，显示用例名字的最大程度
    utx.setting.show_error_traceback = True  # 执行用例的时候，显示报错信息
    utx.setting.sort_case = True  # 是否按照编写顺序，对用例进行排序

    utx.setting.create_report_by_style_1 = True  # 测试报告样式1--utx V0.0.6适用
    utx.setting.create_report_by_style_2 = True  # 测试报告样式2--utx V0.0.6适用

    utx.log.set_level(logging.DEBUG)  # 设置utx的log级别

    runner = utx.TestRunner()
    runner.add_case_dir(r"test_case")
    runner.run_test(report_title='看漫app自动化测试报告')

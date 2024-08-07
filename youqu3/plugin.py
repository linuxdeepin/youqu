import enum
import re

import pytest
from youqu3 import exceptions
from youqu3 import logger
from youqu3 import setting

FLAG_FEEL = "=" * 10


@enum.unique
class ConfStr(enum.Enum):
    SKIP = "skip"
    SKIPIF = "skipif"
    FIXED = "fixed"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    REMOVED = "removed"
    RERUN = "rerun"


def pytest_addoption(parser):
    parser.addoption("--slaves", action="store", default="", help="")


def pytest_sessionstart(session):
    logger("DEBUG")


def pytest_collection_finish(session):
    session.item_count = len(session.items)
    _items = session.items[:]
    is_skiped_case = False
    for item in _items[::-1]:
        for mark in item.own_markers:
            if mark.name == ConfStr.SKIP.value:
                is_skiped_case = True
                try:
                    _items.remove(item)
                except ValueError:
                    ...
            elif mark.name == ConfStr.SKIPIF.value and mark.args == (True,):
                is_skiped_case = True
                try:
                    _items.remove(item)
                except ValueError:
                    ...
    print(
        f"用例收集数量:\t{session.item_count} "
        f"{f'(剔除跳过: {len(_items)})' if is_skiped_case else ''}"
    )
    print(
        f"用例文件数量:\t{len(set([item.fspath for item in session.items]))} "
        f"{f'(剔除跳过: {len(set([item.fspath for item in _items]))})' if is_skiped_case else ''}"
    )


def pytest_runtest_setup(item):
    print()
    LN = "\n"
    current_item_count = f"[{item.session.items.index(item) + 1}/{item.session.item_count}] "
    try:
        current_item_percent = "{:.0f}%".format(
            int(item.session.items.index(item) + 1) / int(item.session.item_count) * 100
        )
    except:
        current_item_percent = ""
    try:
        rerun_text = f" | <重跑第{item.execution_count - 1}次>" if item.execution_count > 1 else ""
    except AttributeError:
        rerun_text = ""
    logger.info(
        f"{LN}{FLAG_FEEL} {item.function.__name__} | "
        f"{str(item.function.__doc__).replace(LN, '').replace('    ', '')}{rerun_text} "
        f"{FLAG_FEEL} {current_item_count} {current_item_percent}"
    )


def pytest_runtest_call(item):
    logger.info(f"{FLAG_FEEL} case body {FLAG_FEEL}")


def pytest_runtest_teardown(item):
    logger.info(f"{FLAG_FEEL} teardown {FLAG_FEEL}")


@pytest.fixture(scope='module')
def page():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise exceptions.YouQuPluginDependencyError("playwright")
    driver = sync_playwright().start()
    browser = driver.chromium.launch_persistent_context(
        user_data_dir=setting.USER_DATE_DIR,
        executable_path=setting.EXECUTABLE_PATH,
        ignore_https_errors=True,
        no_viewport=True,
        slow_mo=500,
        headless=setting.HEADLESS,
        bypass_csp=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--start-maximized',
        ],

    )
    _page = browser.pages[0]
    yield _page
    browser.close()
    driver.stop()


@pytest.fixture(scope="session")
def slaves(pytestconfig):
    _slaves = pytestconfig.getoption("slaves") or setting.SLAVES
    s = []
    if _slaves:
        for slave in _slaves.split("/"):
            slave_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", slave)
            if slave_info:
                user, ip, password = slave_info[0]
                s.append(
                    {
                        "user": user,
                        "ip": ip,
                        "password": password or setting.PASSWORD,
                    }
                )
    if not s:
        raise EnvironmentError("No slaves found, check -s/--slaves value")
    return s


@pytest.fixture(scope="session")
def gui():
    from youqu3.gui import pylinuxauto
    return pylinuxauto


@pytest.fixture(scope="session")
def sleep():
    from youqu3.sleepx import sleep as slp
    return slp


@pytest.fixture(scope="session")
def cmd():
    from youqu3.cmd import Cmd
    return Cmd

@pytest.fixture(scope="session")
def check():
    from youqu3.assertx import Assert
    return Assert
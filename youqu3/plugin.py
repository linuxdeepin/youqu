import re

import pytest

from youqu3 import exceptions
from youqu3 import setting


def pytest_addoption(parser):
    parser.addoption("--slaves", action="store", default="", help="")


def pytest_sessionstart(session):
    from youqu3 import logger
    logger("INFO")


def pytest_runtest_setup(item):
    print()


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

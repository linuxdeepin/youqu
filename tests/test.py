import pytest

def test_001():
    from youqu3.gui import pylinuxauto
    pylinuxauto.find_element_by_attr_path("/dde-dock/Btn_文件管理器").click()
    pylinuxauto.find_element_by_ocr()



if __name__ == '__main__':
    pytest.main()

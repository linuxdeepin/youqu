from youqu3.gui import pylinuxauto


class RpcMethods:

    # attr
    def click_element_by_attr_path(self, attr_path):
        pylinuxauto.find_element_by_attr_path(attr_path).click()

    def double_click_element_by_attr_path(self, attr_path):
        pylinuxauto.find_element_by_attr_path(attr_path).double_click()

    def right_click_element_by_attr_path(self, attr_path):
        pylinuxauto.find_element_by_attr_path(attr_path).right_click()

    def element_center_by_attr_path(self, attr_path):
        return pylinuxauto.find_element_by_attr_path(attr_path).center()

    # image
    def click_element_by_image(self, image_path):
        pylinuxauto.find_element_by_image(image_path).click()

    def double_click_element_by_image(self, image_path):
        pylinuxauto.find_element_by_image(image_path).double_click()

    def right_click_element_by_image(self, image_path):
        pylinuxauto.find_element_by_image(image_path).right_click()

    def element_center_by_image(self, image_path):
        return pylinuxauto.find_element_by_image(image_path).center()

    # ocr
    def click_element_by_ocr(self, target):
        pylinuxauto.find_element_by_ocr(target).click()

    def double_click_element_by_ocr(self, target):
        pylinuxauto.find_element_by_ocr(target).double_click()

    def right_click_element_by_ocr(self, target):
        pylinuxauto.find_element_by_ocr(target).right_click()

    def element_center_by_ocr(self, target):
        return pylinuxauto.find_element_by_ocr(target).center()

    # ui
    def click_element_by_ui(self, appname, config_path, btn_name):
        pylinuxauto.find_element_by_ui(appname, config_path, btn_name).click()

    def double_click_element_by_ui(self, appname, config_path, btn_name):
        pylinuxauto.find_element_by_ui(appname, config_path, btn_name).double_click()

    def right_click_element_by_ui(self, appname, config_path, btn_name):
        pylinuxauto.find_element_by_ui(appname, config_path, btn_name).right_click()

    # mousekey
    def click(self, x=None, y=None):
        pylinuxauto.click(_x=x, _y=y)

    def double_click(self, x=None, y=None):
        pylinuxauto.double_click(_x=x, _y=y)

    def right_click(self, x=None, y=None):
        pylinuxauto.right_click(_x=x, _y=y)

    def move_to(self, x=None, y=None):
        pylinuxauto.move_to(_x=x, _y=y)

    def input(self, text: str):
        pylinuxauto.input(text)

    def hotkey(self, *key):
        pylinuxauto.hot_key(*key)

from settings import *
from selenium import webdriver

class SelSetup():
    def __init__(self):
        if desired_browser.lower() == 'chrome':
            self.desired_capabilities = webdriver.DesiredCapabilities.CHROME
        else:
            self.desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
        self.desired_capabilities['version'] = browser_version
        self.desired_capabilities['platform'] = browser_platform
        self.desired_capabilities['screen-resolution'] = desired_resolution
        self.desired_capabilities['build'] = test_timestamp

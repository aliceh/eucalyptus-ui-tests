from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, datetime, base64, json, httplib
from settings import *
from login import *
from navigation import *
from passfail import SauceRest

class TestVerifyCreateVolume(unittest.TestCase):
    def setUp(self):
        if default_capabilities['browser'].lower() == 'chrome':
            desired_capabilities = webdriver.DesiredCapabilities.CHROME
        else:
            desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
        desired_capabilities["name"] = "Create Volume"
        desired_capabilities['version'] = default_capabilities['version']
        desired_capabilities['platform'] = default_capabilities['platform']
        desired_capabilities['screen-resolution'] = default_capabilities['screen-resolution']
        desired_capabilities['build'] = default_capabilities['build']
        self.driver = webdriver.Remote(desired_capabilities=desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_verify_create_volume(self):
        self.passed = False
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        click_volumes(driver)
        driver.find_element_by_css_selector("body").click()
        driver.find_element_by_id("table-volumes-new").click()
        driver.find_element_by_id("volume-size").clear()
        driver.find_element_by_id("volume-size").send_keys("2")
        driver.find_element_by_id("volumes-add-btn").click()
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*vol-[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        if ([] == self.verificationErrors):
            self.passed = True

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True

    def tearDown(self):
        sauce_rest = SauceRest(
                               username=sauce_username,
                               password=sauce_accesskey,
                              )
        sauce_rest.report_pass_fail(self.driver.session_id,{'passed': self.passed})
        print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
        self.driver.quit()
        #self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

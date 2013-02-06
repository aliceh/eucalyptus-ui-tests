from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, datetime, base64, json, httplib
from settings import *
from login import *
from navigation import *
from passfail import SauceRest

class TestKeypairs(unittest.TestCase):
    def setUp(self):
        if default_capabilities['browser'].lower() == 'chrome':
            desired_capabilities = webdriver.DesiredCapabilities.CHROME
        else:
            desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
        desired_capabilities["name"] = "Add and Remove Key Pair"
        desired_capabilities['version'] = default_capabilities['version']
        desired_capabilities['platform'] = default_capabilities['platform']
        desired_capabilities['screen-resolution'] = default_capabilities['screen-resolution']
        desired_capabilities['build'] = default_capabilities['build']
        self.driver = webdriver.Remote(desired_capabilities=desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_keypairs(self):
        self.passed = False
        keyname = "a-selenium-test-key"
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        click_keypair(driver)
        #Add keypair
        driver.find_element_by_id("table-keys-new").click()
        driver.find_element_by_id("key-name").clear()
        driver.find_element_by_id("key-name").send_keys(keyname)
        driver.find_element_by_id("keys-add-btn").click()
        if keyname not in driver.find_element_by_css_selector("BODY").text:
            self.verificationErrors.append("Failed to add key pair")
        #Remove keypair
        driver.find_element_by_xpath("//table[@id='keys']/tbody/tr/td[2]").click()
        driver.find_element_by_id("more-actions-keys").click()
        driver.find_element_by_link_text("Delete").click()
        driver.find_element_by_css_selector("body").click()
        driver.find_element_by_id("btn-keys-delete-delete").click()
        if keyname in driver.find_element_by_css_selector("BODY").text:
            self.verificationErrors.append("Failed to remove key pair")
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

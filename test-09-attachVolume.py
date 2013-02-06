from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, datetime, base64, json, httplib
from settings import *
from login import *
from navigation import *
from passfail import SauceRest

class TestVerifyAttachVolume(unittest.TestCase):
    def setUp(self):
        if default_capabilities['browser'].lower() == 'chrome':
            desired_capabilities = webdriver.DesiredCapabilities.CHROME
        else:
            desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
        desired_capabilities["name"] = "Attach Volume"
        desired_capabilities['version'] = default_capabilities['version']
        desired_capabilities['platform'] = default_capabilities['platform']
        desired_capabilities['screen-resolution'] = default_capabilities['screen-resolution']
        desired_capabilities['build'] = default_capabilities['build']
        self.driver = webdriver.Remote(desired_capabilities=desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_verify_attach_volume(self):
        self.passed = False
        self.retry = 20
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        click_volumes(driver)
        #Store volume id
        volume_id = driver.find_element_by_xpath("//table[@id='volumes']/tbody/tr/td[2]").text; #volume_id = volume_id.strip()
        #Attach volume
        click_instances(driver)
        driver.find_element_by_xpath("//table[@id='instances']/tbody/tr/td/input").click()
        driver.find_element_by_id("more-actions-instances").click()
        for i in range(self.retry):
            if self.is_element_present(By.LINK_TEXT, "Attach volume"):
                break
            time.sleep(1)
            if i == (self.retry - 1):
                self.verificationErrors.append("Could not find 'Attach volumed' link")
                return False
        driver.find_element_by_link_text("Attach volume").click()
        driver.find_element_by_xpath("(//input[@id='volume-attach-volume-id'])[2]").clear()
        driver.find_element_by_xpath("(//input[@id='volume-attach-volume-id'])[2]").send_keys(volume_id)
        driver.find_element_by_xpath("(//input[@id='volume-attach-volume-id'])[2]").send_keys(Keys.TAB)
        driver.find_element_by_id("volume-attach-btn").click()
        #Verify that the volume was attached
        time.sleep(20)
        click_dashboard(driver)
        click_volumes(driver)
        Select(driver.find_element_by_id("vol_state-selector")).select_by_visible_text("Attached volumes")
        driver.find_element_by_css_selector("body").click()
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*1 volumes found[\s\S]*$")
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

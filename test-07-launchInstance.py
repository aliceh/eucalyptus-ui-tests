from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, datetime, base64, json, httplib
from settings import *
from login import *
from navigation import *
from passfail import SauceRest
from capabilities import SelSetup

class TestVerifyLaunchInstance(unittest.TestCase):
    def setUp(self):
        sel_setup = SelSetup()
        sel_setup.desired_capabilities["name"] = "Launch Instance"
        self.driver = webdriver.Remote(desired_capabilities=sel_setup.desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_verify_launch_instance(self):
        self.passed = False
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        #Launch the instance
        driver.find_element_by_link_text("Launch new instance").click()
        driver.find_element_by_xpath("//table[@id='launch-images']/tbody/tr").click()
        driver.find_element_by_id("launch-wizard-buttons-image-next").click()
        driver.find_element_by_id("launch-wizard-buttons-type-next").click()
        driver.find_element_by_id("launch-wizard-buttons-security-launch").click()
        #Verify instance is pending
        time.sleep(3)
        Select(driver.find_element_by_id("inst_state-selector")).select_by_visible_text("Pending instances")
        driver.find_element_by_css_selector("body").click()
        if "0 instances found" in driver.find_element_by_css_selector("BODY").text:
            self.verificationErrors.append("Instance did not enter pending state")
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

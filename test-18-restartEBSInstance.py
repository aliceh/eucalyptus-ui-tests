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

class TestVerifyStartInstance(unittest.TestCase):
    def setUp(self):
        sel_setup = SelSetup()
        sel_setup.desired_capabilities["name"] = "Restart EBS Instance"
        self.driver = webdriver.Remote(desired_capabilities=sel_setup.desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_verify_start(self):
        self.retry = 20
        self.passed = False
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        #Restart
        click_instances(driver)
        Select(driver.find_element_by_id("inst_type-selector")).select_by_visible_text("EBS root device")
        driver.find_element_by_css_selector("td.checkbox-cell > input[type=\"checkbox\"]").click()
        driver.find_element_by_id("more-actions-instances").click()
        for i in range(self.retry):
            if self.is_element_present(By.LINK_TEXT, "Start"):
                break
            time.sleep(1)
            if i == (self.retry - 1):
                self.verificationErrors.append("Could not find 'Start' link")
                return False
        driver.find_element_by_link_text("Start").click()
        click_dashboard(driver)
        click_instances(driver)
        #Wait for instance to start
        Select(driver.find_element_by_id("inst_type-selector")).select_by_visible_text("EBS root device")
        Select(driver.find_element_by_id("inst_state-selector")).select_by_visible_text("Running instances")
        for i in range(40):
            driver.find_element_by_css_selector("body").click()
            time.sleep(1)
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*1 instances found[\s\S]*$")
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

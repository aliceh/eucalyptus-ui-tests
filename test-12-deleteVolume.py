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
from capabilities import SelSetup

class TestVerifyDeleteVolume(unittest.TestCase):
    def setUp(self):
        sel_setup = SelSetup()
        sel_setup.desired_capabilities["name"] = "Delete Volume"
        self.driver = webdriver.Remote(desired_capabilities=sel_setup.desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_verify_delete_volume(self):
        self.passed = False
        self.retry = 20
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        click_volumes(driver)
        driver.find_element_by_css_selector("td.checkbox-cell > input[type=\"checkbox\"]").click()
        driver.find_element_by_id("more-actions-volumes").click()
        for i in range(self.retry):
            if self.is_element_present(By.LINK_TEXT, "Delete"):
                break
            time.sleep(1)
            if i == (self.retry - 1):
                self.verificationErrors.append("Could not find 'Delete' link")
                return False
        driver.find_element_by_link_text("Delete").click()
        for i in range(self.retry):
            if self.is_element_present(By.ID, "btn-volumes-delete-delete"):
                break
            time.sleep(1)
            if i == (self.retry - 1):
                self.verificationErrors.append("Could not find delete button")
                return False
        driver.find_element_by_id("btn-volumes-delete-delete").click()
        #Volume detachment can take more than 30 seconds which will cause selenium to die if we don't send a command in that time period
        for i in range(60):
            driver.find_element_by_css_selector("body").click()
            time.sleep(1)
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*You currently have no volumes[\s\S]*$")
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

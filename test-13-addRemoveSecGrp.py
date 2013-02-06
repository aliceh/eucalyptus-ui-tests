from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, datetime, base64, json, httplib
from settings import *
from login import *
from navigation import *
from passfail import SauceRest

class TestVerifyAddRemSecGrp(unittest.TestCase):
    def setUp(self):
        if default_capabilities['browser'].lower() == 'chrome':
            desired_capabilities = webdriver.DesiredCapabilities.CHROME
        else:
            desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
        desired_capabilities["name"] = "Add/Remove Security Group"
        desired_capabilities['version'] = default_capabilities['version']
        desired_capabilities['platform'] = default_capabilities['platform']
        desired_capabilities['screen-resolution'] = default_capabilities['screen-resolution']
        desired_capabilities['build'] = default_capabilities['build']
        self.driver = webdriver.Remote(desired_capabilities=desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_verify_add_rem_sec_grp(self):
        self.passed = False
        self.retry = 20
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        click_secgroup(driver)
        driver.find_element_by_id("table-sgroups-new").click()
        driver.find_element_by_id("sgroup-name").clear()
        driver.find_element_by_id("sgroup-name").send_keys("a-selenium-test-group")
        driver.find_element_by_id("sgroup-description").clear()
        driver.find_element_by_id("sgroup-description").send_keys("a simple test to create, modify, and delete a security group")
        driver.find_element_by_id("sgroup-add-btn").click()
        time.sleep(10)
        if "a-selenium-test-group" not in driver.find_element_by_css_selector("BODY").text:
            self.verificationErrors.append("Unable to create security group")
        driver.find_element_by_xpath("//table[@id='keys']/tbody/tr[2]/td/input").click()
        driver.find_element_by_id("more-actions-sgroups").click()
        for i in range(self.retry):
            if self.is_element_present(By.LINK_TEXT, "Delete"):
                break
            time.sleep(1)
            if i == (self.retry - 1):
                self.verificationErrors.append("Could not find 'Delete' link")
                return False
        driver.find_element_by_link_text("Delete").click()
        driver.find_element_by_id("btn-sgroups-delete-delete").click()
        time.sleep(10)
        if "selenium-test-group" in driver.find_element_by_css_selector("BODY").text:
            self.verificationErrors.append("Unable to delete security group")
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

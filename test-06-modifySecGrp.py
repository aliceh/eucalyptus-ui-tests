from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, datetime, base64, json, httplib
from settings import *
from login import *
from navigation import *
from passfail import SauceRest

class TestVerifyModSecGrp(unittest.TestCase):
    def setUp(self):
        desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
        desired_capabilities["name"] = "Modify Security Group"
        desired_capabilities['version'] = default_capabilities['version']
        desired_capabilities['platform'] = default_capabilities['platform']
        desired_capabilities['screen-resolution'] = default_capabilities['screen-resolution']
        desired_capabilities['build'] = default_capabilities['build']
        self.driver = webdriver.Remote(desired_capabilities=desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_verify_modify_sec_grp(self):
        self.passed = False
        self.retry = 20
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        click_secgroup(driver)
        driver.find_element_by_css_selector("td.checkbox-cell.sorting_1 > input[type=\"checkbox\"]").click()
        driver.find_element_by_id("more-actions-sgroups").click()
        for i in range(self.retry):
            if self.is_element_present(By.LINK_TEXT, "Manage rules"):
                break
            time.sleep(1)
            if i == (self.retry - 1):
                self.verificationErrors.append("Could not find 'Manage rules' link")
                return False
        driver.find_element_by_link_text("Manage rules").click()
        driver.find_element_by_css_selector("body").click()
        Select(driver.find_element_by_xpath("(//select[@id='sgroup-template'])[2]")).select_by_visible_text("SSH (TCP port 22, for terminal access)")
        driver.find_element_by_xpath("(//input[@id='allow-ip'])[2]").clear()
        driver.find_element_by_xpath("(//input[@id='allow-ip'])[2]").send_keys("0.0.0.0/0")
        driver.find_element_by_xpath("(//a[contains(text(),'Add another rule')])[2]").click()
        Select(driver.find_element_by_xpath("(//select[@id='sgroup-template'])[2]")).select_by_visible_text("Custom ICMP")
        driver.find_element_by_xpath("(//input[@id='allow-ip'])[2]").clear()
        driver.find_element_by_xpath("(//input[@id='allow-ip'])[2]").send_keys("0.0.0.0/0")
        driver.find_element_by_xpath("(//a[contains(text(),'Add another rule')])[2]").click()
        for i in range(self.retry):
            if self.is_element_present(By.ID, "sgroup-add-btn"):
                break
            time.sleep(1)
            if i == (self.retry - 1):
                self.verificationErrors.append("Could not find 'Save changes' button")
                return False
        driver.find_element_by_id("sgroup-add-btn").click()
        time.sleep(15)
        driver.find_element_by_link_text("default").click()
        driver.find_element_by_css_selector("body").click()
        # Warning: verifyTextPresent may require manual changes
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*icmp[\s\S]*$")
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

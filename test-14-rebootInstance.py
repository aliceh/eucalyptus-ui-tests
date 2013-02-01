from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, datetime, base64, json, httplib, commands, sys
from settings import *
from login import *
from navigation import *
from passfail import SauceRest

class TestVerifyRebootInstance(unittest.TestCase):
    def setUp(self):
        desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
        desired_capabilities["name"] = "Reboot Instance"
        desired_capabilities['version'] = default_capabilities['version']
        desired_capabilities['platform'] = default_capabilities['platform']
        desired_capabilities['screen-resolution'] = default_capabilities['screen-resolution']
        desired_capabilities['build'] = default_capabilities['build']
        self.driver = webdriver.Remote(desired_capabilities=desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_verify_reboot_instance(self):
        self.retry = 20
        self.passed = False
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        click_running(driver)
        #Get public IP of instance
        driver.find_element_by_xpath("//td[6]").click()
        public_ip = driver.find_element_by_xpath("//td[6]").text
        driver.find_element_by_css_selector("td.checkbox-cell > input[type=\"checkbox\"]").click()
        driver.find_element_by_css_selector("td.checkbox-cell > input[type=\"checkbox\"]").click()
        #Reboot instance
        driver.find_element_by_id("more-actions-instances").click()
        for i in range(self.retry):
            if self.is_element_present(By.LINK_TEXT, "Reboot"):
                break
            time.sleep(1)
            if i == (self.retry - 1):
                self.verificationErrors.append("Could not find 'Reboot' link")
                return False
        driver.find_element_by_link_text("Reboot").click()
        driver.find_element_by_id("btn-instances-reboot-reboot").click()
        time.sleep(20)
        #Ping instance to ensure it came back up
        status,output = commands.getstatusoutput("ping " + public_ip + " -c 5")
        if status != 0:
            print "Unable to ping instance - it may not have rebooted properly"
            self.verificationErrors.append("Unable to ping instance - it may not have rebooted properly")
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

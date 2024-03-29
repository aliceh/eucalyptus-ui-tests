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

class TestNavBar(unittest.TestCase):
    def setUp(self):
        sel_setup = SelSetup()
        sel_setup.desired_capabilities["name"] = "Test NavBar"
        self.driver = webdriver.Remote(desired_capabilities=sel_setup.desired_capabilities,command_executor=command_executor)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_navbar(self):
        self.passed = False
        driver = self.driver
        console_login(driver)
        click_dashboard(driver)
        click_images(driver)
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*images found[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        click_instances(driver)
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*instances found[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        click_storage(driver)
        click_volumes_link(driver)
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*volumes found[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        click_storage(driver)
        click_snapshots_link(driver)
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*snapshots found[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        click_network(driver)
        click_secgroup_link(driver)
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*security groups found[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        click_network(driver)
        click_keypair_link(driver)
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*keys found[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        click_network(driver)
        click_ips_link(driver)
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*IP addresses found[\s\S]*$")
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

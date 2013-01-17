from settings import *

def console_login(driver):
  driver.get("http://" + console_ip + ":" + console_port + "/")
  driver.find_element_by_id("account").clear()
  driver.find_element_by_id("account").send_keys(console_account)
  driver.find_element_by_id("username").clear()
  driver.find_element_by_id("username").send_keys(console_user)
  driver.find_element_by_id("password").clear()
  driver.find_element_by_id("password").send_keys(console_password)
  driver.find_element_by_name("login").click()

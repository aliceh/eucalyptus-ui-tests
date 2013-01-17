def click_dashboard(driver):
  driver.find_element_by_link_text("Dashboard").click()

def click_running(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-instance-running']/div").click()

def click_keypair(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-netsec-keypair']").click()

def click_secgroup(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-netsec-sgroup']").click()

def click_volumes(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-storage-volume']").click()

def click_snapshots(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-storage-snapshot']").click()

def click_ips(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-netsec-eip']/span").click()

def click_stopped(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-instance-stopped']/div").click()

def click_launch(driver):
  driver.find_element_by_link_text("Launch new instance").click()

def click_images(driver):
  driver.find_element_by_link_text("Images").click()

def click_instances(driver):
  driver.find_element_by_link_text("Instances").click()

def click_dashboard(driver):
  driver.find_element_by_link_text("Dashboard").click()

def click_running(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-instance-running']/div").click()

def click_keypair(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-netsec-keypair']").click()

def click_keypair_link(driver):
  driver.find_element_by_link_text("Key Pairs").click()

def click_secgroup(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-netsec-sgroup']").click()

def click_secgroup_link(driver):
  driver.find_element_by_link_text("Security Groups").click()

def click_volumes(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-storage-volume']").click()

def click_volumes_link(driver):
  driver.find_element_by_link_text("Volumes").click()

def click_snapshots(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-storage-snapshot']").click()

def click_snapshots_link(driver):
  driver.find_element_by_link_text("Snapshots").click()

def click_ips(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-netsec-eip']/span").click()

def click_ips_link(driver):
  driver.find_element_by_link_text("IP Addresses").click()

def click_stopped(driver):
  driver.find_element_by_xpath("//div[@id='dashboard-instance-stopped']/div").click()

def click_launch(driver):
  driver.find_element_by_link_text("Launch new instance").click()

def click_images(driver):
  driver.find_element_by_link_text("Images").click()

def click_instances(driver):
  driver.find_element_by_link_text("Instances").click()

def click_storage(driver):
  driver.find_element_by_link_text("Storage").click()

def click_network(driver):
  driver.find_element_by_link_text("Network & Security").click()

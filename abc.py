from executors.login_manager import login_all_sites
login_all_sites()
from executors.login_manager import init_driver, load_cookies

driver = init_driver(headless=False)
load_cookies(driver, "naukri")
load_cookies(driver, "unstop")
load_cookies(driver, "linkedin")

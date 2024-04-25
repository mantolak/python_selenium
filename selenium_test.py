from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def test_twitch():
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, "
                     "like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
        "clientHints": {"platform": "Android", "mobile": True}}
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(chrome_options)

    driver.get("https://m.twitch.tv/")

    title = driver.title
    assert title == "Twitch"

    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR, '[aria-hidden="false"] [role="dialog"] button').click()

    driver.find_element(By.CSS_SELECTOR, '[aria-label="Search"]').click()
    driver.find_element(By.CSS_SELECTOR, '[type="search"]').send_keys("StarCraft II")
    assert driver.find_element(By.CSS_SELECTOR, '[alt="StarCraft II"]').is_displayed()
    driver.find_element(By.CSS_SELECTOR, '[alt="StarCraft II"]').click()
    streamer_list = driver.find_elements(By.CSS_SELECTOR, '[role="list"] div')
    assert len(streamer_list) > 0

    delta_y = driver.get_window_rect()
    scroll_script_20_percentage = f'window.scrollTo(0, {round(delta_y["height"]/100 * 20)})'
    scroll_amount = 2
    for scroll in range(scroll_amount):
        driver.execute_script(scroll_script_20_percentage)
    assert streamer_list[round(len(streamer_list)/100 * (20 * scroll_amount))].is_displayed()
    streamer_list[round(len(streamer_list) / 100 * (20 * scroll_amount))].find_element(By.TAG_NAME, 'a').click()
    assert driver.find_element(By.CSS_SELECTOR, 'main video').is_displayed()
    time.sleep(5)
    driver.save_screenshot('screen.png')
    driver.quit()

import time 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)

URL = "https://kingex.io/?locale=en&cur_from=USDTTRC20&cur_to=ALPCNY"
def get_source_code(URL: str) -> None:

    driver.get(url = URL)
    

    elem = float(str(driver.find_element(By.CLASS_NAME, "iex__new-main-course__value").text).split(" ")[3])
    
    return elem


def main():
    return get_source_code(URL)

if __name__ == '__main__':
    main()
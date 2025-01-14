from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def setup_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def dismiss_overlays(driver, wait):
    try:
        dismiss_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Dismiss']"))
        )
        dismiss_button.click()
    except Exception as ex:
        print("Dismiss pop up not found", ex)

    try:
        cookie_consent = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.cc-btn.cc-dismiss"))
        )
        cookie_consent.click()
        time.sleep(2)
    except Exception as ex:
        print("Cookie pop up not found ", ex)


def test_juice_shop_display_maximum_items():
    """
    Open Juice Shop, dismiss overlays, scroll down, select '48' from the dropdown,
    then verify that 37 images (with specific CSS classes) are displayed.
    """
    driver = setup_driver()
    wait = WebDriverWait(driver, 15)
    
    try:
        driver.get("https://juice-shop.herokuapp.com/#/")        
        dismiss_overlays(driver, wait)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mat-select-value-1")))
        dropdown.click()
        
        option_48 = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='48']"))
        )
        option_48.click()
        time.sleep(5)
        
        image_selector = "img.mat-card-image.img-responsive.img-thumbnail"
        images = driver.find_elements(By.CSS_SELECTOR, image_selector)
        image_count = len(images)
        
        assert image_count == 37, f"Expected 37 images, but found {image_count}"
        
    except Exception as ex:
        print("Test failed:", ex)
    
    finally:
        driver.quit()
        

def test_click_apple_juice_image():
    driver = setup_driver()
    wait = WebDriverWait(driver, 15)
    
    try:
        driver.get("https://juice-shop.herokuapp.com/#/")
        
        dismiss_overlays(driver, wait)
        
        apple_juice_xpath = (
            "//img[contains(@class, 'mat-card-image') and contains(@class, 'img-responsive') "
            "and contains(@class, 'img-thumbnail') and @alt='Apple Juice (1000ml)']"
        )
        apple_juice_image = wait.until(EC.element_to_be_clickable((By.XPATH, apple_juice_xpath)))
        apple_juice_image.click()
        time.sleep(3)
        
        popup = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "mat-dialog-container[role='dialog']"))
        )
        assert popup is not None, "Apple popup not found"
        
        reviews_panel = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//mat-panel-title[.//span[contains(text(),'Reviews')]]")
            )
        )
        reviews_panel.click()
        time.sleep(5)
    
    except Exception as ex:
        print("Test failed:", ex)
    
    finally:
        driver.quit()


if __name__ == "__main__":
    test_juice_shop_display_maximum_items()
    test_click_apple_juice_image()

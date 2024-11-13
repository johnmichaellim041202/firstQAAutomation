import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def setup_dev_browser(request):
    # Path to the chromedriver executable
    # print(os.path.abspath(os.path.join(os.path.dirname(__file__), "../chromedriver/123-0-6312-122.exe")))
    # service_obj = Service(
    #     os.path.abspath(os.path.join(os.path.dirname(__file__), "../chromedriver/128.0.6613.86.exe")))
    # service_obj = Service(ChromeDriverManager().install())
    # service_obj = Service(
    # os.path.abspath(os.path.join(os.path.dirname(__file__), "../chromedriver/124-0-6367-207-linux")))

    # Initialize Chrome WebDriver with options
    chrome_options = webdriver.ChromeOptions()
    # Enables headless mode, which runs Chrome without a graphical user interface
    # chrome_options.add_argument("--headless")
    # Disables GPU hardware acceleration, which can improve performance in headless mode.
    chrome_options.add_argument("--disable-gpu")
    # Disables the sandbox mode, which can sometimes cause issues in headless mode, especially in certain environments.
    chrome_options.add_argument("--no-sandbox")
    # Disable animations
    chrome_options.add_argument("--disable-animations")
    # Set window size to full HD (1920x1080)
    # chrome_options.add_argument('--window-size=1920,1080')
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-device-discovery-notifications")
    chrome_options.add_argument("--disable-extensions")  # Disable extensions that may cause USB interaction
    # Suppress logs (errors only)
    chrome_options.add_argument("--log-level=3")
    # Set the window to be full screen
    chrome_options.add_argument('--start-fullscreen')
    # Disables popup to save address and etc
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,  # Disable saving passwords
        "profile.password_manager_enabled": False,  # Disable password manager
        "autofill.profile_enabled": False,  # Disable autofill for addresses and forms
        "autofill.address_enabled": False,  # Disable address autofill specifically
        "autofill.credit_card_enabled": False  # Disable credit card autofill
    })

    chrome_options.add_argument("--disable-features=AutofillServerCommunication")  # Disable autofill server comms
    chrome_options.add_argument("--disable-save-password-bubble")  # Disable save password bubble

    # driver = webdriver.Chrome(options=chrome_options, service=service_obj)
    # driver = webdriver.Chrome(options=chrome_options)

    # Automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Create the WebDriver instance with the latest ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(5)
    driver.get("https://dev-dashboard.n-compass.online/login")

    yield driver

    # Clean up: close the browser window after the tests
    driver.quit()

@pytest.fixture()
def dev_login_as_admin(request, setup_dev_browser):
    # Initialize admin user
    user = {'username': 'test-bot@admin.com', 'password': 'qwerty123'}
    driver = setup_dev_browser
    wait_driver = WebDriverWait(driver, 30)

    # Find the username input field by its ng-reflect-name attribute
    locator = (By.XPATH, "//input[@ng-reflect-name='username']")
    username_field = wait_driver.until(EC.visibility_of_element_located(locator))

    # Find the password input field by its ng-reflect-name attribute
    locator = (By.XPATH, "//input[@ng-reflect-name='password']")
    password_field = wait_driver.until(EC.visibility_of_element_located(locator))

    # Find the login button by the text content within the <span> tag
    locator = (By.XPATH, "//button[contains(@class, 'mat-raised-button')]/span[contains(text(), 'LOGIN')]")
    login_button = wait_driver.until(EC.element_to_be_clickable(locator))

    # Add the credentials
    username_field.send_keys(user['username'])
    password_field.send_keys(user['password'])

    # Click the Login Button
    login_button.click()

    # On Successful Login
    try:
        # Find the close button within the div with specific styling
        locator = (By.XPATH, "//div[contains(@style, 'justify-content: flex-end')]//button[text()='Close']")
        onLoginClose_button = wait_driver.until(EC.element_to_be_clickable(locator))

        # Click the close button
        onLoginClose_button.click()

    except Exception as e:
        print(e)

    yield driver


@pytest.fixture()
def dev_login_as_dealer_admin(request, setup_dev_browser):
    # Initialize dealer admin user
    user = {'username': 'ricos-dealer-admin@n-compass.biz', 'password': 'qwerty123'}
    driver = setup_dev_browser
    wait_driver = WebDriverWait(driver, 30)

    # Find the username input field by its ng-reflect-name attribute
    locator = (By.XPATH, "//input[@ng-reflect-name='username']")
    username_field = wait_driver.until(EC.visibility_of_element_located(locator))

    # Find the password input field by its ng-reflect-name attribute
    locator = (By.XPATH, "//input[@ng-reflect-name='password']")
    password_field = wait_driver.until(EC.visibility_of_element_located(locator))

    # Find the login button by the text content within the <span> tag
    locator = (By.XPATH, "//button[contains(@class, 'mat-raised-button')]/span[contains(text(), 'LOGIN')]")
    login_button = wait_driver.until(EC.element_to_be_clickable(locator))

    username_field.send_keys(user['username'])
    password_field.send_keys(user['password'])
    login_button.click()

    # On Successful Login
    try:
        # Find the close button within the div with specific styling
        locator = (By.XPATH, "//div[contains(@style, 'justify-content: flex-end')]//button[text()='Close']")
        onLoginClose_button = wait_driver.until(EC.element_to_be_clickable(locator))

        # Click the close button
        onLoginClose_button.click()

    except Exception as e:
        print(e)

    yield driver


@pytest.fixture()
def dev_login_as_dealer(request, setup_dev_browser):
    driver = setup_dev_browser
    wait_driver = WebDriverWait(driver, 30)

    # Initialize dealer admin user
    user = {'username': 'ricos-dealer@n-compass.biz', 'password': 'qwerty123'}

    # Find the username input field by its ng-reflect-name attribute
    locator = (By.XPATH, "//input[@ng-reflect-name='username']")
    username_field = wait_driver.until(EC.visibility_of_element_located(locator))

    # Find the password input field by its ng-reflect-name attribute
    locator = (By.XPATH, "//input[@ng-reflect-name='password']")
    password_field = wait_driver.until(EC.visibility_of_element_located(locator))

    # Find the login button by the text content within the <span> tag
    locator = (By.XPATH, "//button[contains(@class, 'mat-raised-button')]/span[contains(text(), 'LOGIN')]")
    login_button = wait_driver.until(EC.element_to_be_clickable(locator))

    username_field.send_keys(user['username'])
    password_field.send_keys(user['password'])
    login_button.click()

    yield driver


@pytest.fixture()
def dev_admin_navigate_to_locator_screen(dev_login_as_admin):
    locatorTitle = "Locator"
    # Get the driver returned from the fixture
    driver = dev_login_as_admin
    # Set the maximum amount of time to wait for the element (in seconds)
    wait_driver = WebDriverWait(driver, 30)

    # Find the advertisers button
    locator = (By.XPATH, "//span[@class='url-text'][normalize-space()='Locator']")
    locatorButton = wait_driver.until(EC.element_to_be_clickable(locator))

    # Click the locator button
    locatorButton.click()

    title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".page-title"))
    )

    assert title_element.text == locatorTitle, f"Expected Title: {locatorTitle}, Actual Title: {title_element}"

    yield driver
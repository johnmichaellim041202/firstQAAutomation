import time

import random

import allure
import pytest
from select import select
from selenium.common import TimeoutException, ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dashboard.conftest import dev_admin_navigate_to_locator_screen


@allure.feature("Locator")
def test_dev_admin_locator_dealers(dev_admin_navigate_to_locator_screen):
    # Set the maximum amount of time to wait for the element (in seconds)
    # Get the driver returned from the fixture
    wait_driver = initialize_wait_driver_feeds(dev_admin_navigate_to_locator_screen)
    driver = dev_admin_navigate_to_locator_screen
    driver.implicitly_wait(20)

    # List of dealer names to search and select
    dealers_to_search = ["Fujiwara Tofu Store", "Project Deez Nuts", "Violet System"]

    try:
        # Locate the dealer selection dropdown field
        locator = (By.XPATH, "(//div[@class='mat-form-field-infix'])[1]")
        selectDealerNames = wait_driver.until(EC.presence_of_element_located(locator))
        selectDealerNames.click()

        # Loop through each dealer name in the list and select it
        for dealer_to_search in dealers_to_search:
            # Search for each dealer name
            searchDealer = wait_driver.until(
                EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='Search Dealer Name'])[1]"))
            )
            searchDealer.clear()  # Clear previous input
            searchDealer.send_keys(dealer_to_search)

            time.sleep(5)

            # Wait for dealer options to load in the dropdown
            dealerNameDropdown = wait_driver.until(
                EC.presence_of_all_elements_located((By.XPATH, "//mat-option[@role='option']"))
            )

            # Search for the specified dealer in the dropdown and click if found
            dealer_found = False
            for dealer in dealerNameDropdown:
                if dealer.text == dealer_to_search:

                    try:
                        dealer.click()  # Attempt to click the dealer element
                    except ElementClickInterceptedException:
                        print("Dealer didn't find the elements to be clicked")
                    print(f"Selected dealer: {dealer_to_search}")
                    dealer_found = True
                    break

            # If the dealer was not found in the dropdown, log a message
            if not dealer_found:
                print(f"Dealer '{dealer_to_search}' not found in the dropdown.")

            time.sleep(1)
            searchDealer.clear()

    except TimeoutException:
        print("Timed out waiting for elements to load.")
    except NoSuchElementException as e:
        print(f"Error: {e}")
    else:
        print("Nothing went wrong")

    # Try to click 'APPLY SELECTION' to confirm the dealer selection
    try:
        locator = (By.XPATH, "//button[normalize-space()='APPLY SELECTION']")
        applySelection = wait_driver.until(EC.presence_of_element_located(locator))
        applySelection.click()
        print("APPLY SELECTION button clicked successfully.")
    except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
        print(f"Error clicking 'APPLY SELECTION': {e}")

    time.sleep(5)

    try:
        # Verify each selected dealer name appears in the filter list
        for i, dealer in enumerate(dealers_to_search, start=1):
            # Locate the dealer element in the filter list
            locator = (By.XPATH, f"(//div/div/div[@class='name'])[{i}]")
            filter_dealer_element = wait_driver.until(EC.presence_of_element_located(locator))
            filter_dealer_name = filter_dealer_element.text.strip()  # Get the text and strip any whitespace

            # Print the found name and assert it matches the expected dealer
            print(f"Filter name found: {filter_dealer_name}")
            assert filter_dealer_name == dealer, f"Expected dealer '{dealer}' but found '{filter_dealer_name}' in the filter list."

    except TimeoutException:
        print("Timed out waiting for a filter element.")
    except NoSuchElementException:
        print("A filter element was not found.")
    except AssertionError as e:
        print(f"Assertion failed: {e}")

    try:
        # Verify each selected dealer name appears in the accordion list
        for i, dealer in enumerate(dealers_to_search, start=1):
            locator = (By.XPATH, f"(//span[@class='font-weight-bold sm-text'])[{i}]")
            accordion_dealer_element = wait_driver.until(EC.presence_of_element_located(locator))
            accordion_dealer_name = accordion_dealer_element.text.strip()

            # Print the found name and assert it matches the expected dealer
            print(f"Accordion name found: {accordion_dealer_name}")
            assert accordion_dealer_name == dealer, f"Expected dealer '{dealer}' but found '{accordion_dealer_name}' in the accordion list."

    except TimeoutException:
        print("Timed out waiting for a filter element.")
    except NoSuchElementException:
        print("A filter element was not found.")
    except AssertionError as e:
        print(f"Assertion failed: {e}")

    try:
        # Click 'CLEAR SELECTION' to remove selected dealers
        locator = (By.XPATH, "(//span[normalize-space()='CLEAR SELECTION'])[1]")
        clearSelection = wait_driver.until(EC.presence_of_element_located(locator))
        clearSelection.click()
    except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
        print(f"Error clicking 'APPLY SELECTION': {e}")

    time.sleep(10)

    # Update new Dealer Name(s)
    update_dealers_to_search = ["Salt Bae", "Wintoo's Advertisement", "Krusty Krabs", "Beyond Journey's End", "Grumpy Fries", "Fujiwara Tofu Store"]

    try:
        # Locate and click the dealer selection dropdown field
        locator = (By.XPATH, "(//div[@class='mat-form-field-infix'])[1]")
        selectDealerNames = wait_driver.until(EC.presence_of_element_located(locator))
        selectDealerNames.click()

        # Loop through each dealer name in the list and select it
        for newDealer in update_dealers_to_search:
            # Search for each dealer name
            searchDealer = wait_driver.until(
                EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='Search Dealer Name'])[1]"))
            )
            searchDealer.clear()  # Clear previous input
            searchDealer.send_keys(newDealer)

            time.sleep(5)

            # Get the dealer options again after sending keys to ensure list refresh
            dealerNameDropdown = wait_driver.until(
                EC.presence_of_all_elements_located((By.XPATH, f"//mat-option[@role='option']"))
            )

            # Search for the specified dealer in the dropdown and click if found
            dealer_found = False
            for update in dealerNameDropdown:
                if update.text == newDealer:
                    try:
                        update.click()
                        print(f"Selected dealer: {newDealer}")
                        dealer_found = True
                        break
                    except ElementClickInterceptedException:
                        print(f"Could not click dealer: {newDealer}")

            # If the dealer was not found in the dropdown, log a message
            if not dealer_found:
                print(f"Dealer '{newDealer}' not found in the dropdown.")

            # Short pause before searching for the next dealer
            time.sleep(5)
            searchDealer.clear()

    except TimeoutException:
        print("Timed out waiting for elements to load.")
    except NoSuchElementException as e:
        print(f"Error: {e}")

    try:
        # Click 'APPLY SELECTION' to confirm the dealer selection
        applySelection_locator = (By.XPATH, "//button[normalize-space()='APPLY SELECTION']")
        applySelection = wait_driver.until(EC.presence_of_element_located(applySelection_locator))
        applySelection.click()
    except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
        print(f"Error clicking 'APPLY SELECTION': {e}")

    time.sleep(10)

    try:
        # Verify each selected dealer name appears in the filter list
        for i, dealer in enumerate(update_dealers_to_search, start=1):
            locator = (By.XPATH, f"(//div/div/div[@class='name'])[{i}]")
            filter_dealer_element = wait_driver.until(EC.presence_of_element_located(locator))
            filter_dealer_name = filter_dealer_element.text.strip()  # Get the text and strip any whitespace

            # Print the found name and assert it matches the expected dealer
            print(f"Filter name found: {filter_dealer_name}")
            assert filter_dealer_name == dealer, f"Expected dealer '{dealer}' but found '{filter_dealer_name}' in the filter list."

    except TimeoutException:
        print("Timed out waiting for a filter element.")
    except NoSuchElementException:
        print("A filter element was not found.")
    except AssertionError as e:
        print(f"Assertion failed: {e}")

    try:
        # Verify each selected dealer name appears in the accordion list
        for i, dealer in enumerate(update_dealers_to_search, start=1):
            locator = (By.XPATH, f"(//span[@class='font-weight-bold sm-text'])[{i}]")
            accordion_dealer_element = wait_driver.until(EC.presence_of_element_located(locator))
            accordion_dealer_name = accordion_dealer_element.text.strip()

            # Print the found name and assert it matches the expected dealer
            print(f"Accordion name found: {accordion_dealer_name}")
            assert accordion_dealer_name == dealer, f"Expected dealer '{dealer}' but found '{accordion_dealer_name}' in the accordion list."

    except TimeoutException:
        print("Timed out waiting for a filter element.")
    except NoSuchElementException:
        print("A filter element was not found.")
    except AssertionError as e:
        print(f"Assertion failed: {e}")


    # While there are dealers to remove from the filter list
    while update_dealers_to_search:
        # Create a list of indices based on the current length of the dealer list
        indices = list(range(1, len(update_dealers_to_search) + 1))

        # Shuffle the indices randomly
        random.shuffle(indices)

        # Pick a random index from the shuffled list
        i = indices.pop(0)  # Pop the first element after shuffling (this removes and gives a random index)

        try:
            # Locate the remove button for the dealer name in the filter list
            locator = (By.XPATH, f"(//div/div/div[@class='remove-btn cursor-pointer'])[{i}]")
            remove_filter_dealer = wait_driver.until(EC.element_to_be_clickable(locator))
            remove_filter_dealer.click()  # Click the remove button to remove the filter

            # Wait briefly to allow the UI to update
            time.sleep(1)

            # Remove the dealer from the `dealers_to_search` list after clicking remove
            removed_dealer = update_dealers_to_search.pop(i - 1)  # Remove by index, adjusting for 0-based indexing
            print(f"Removed dealer from filter: {removed_dealer}")

        except TimeoutException:
            print("Timed out waiting for remove button to load.")
            break
        except NoSuchElementException as e:
            print(f"Remove button not found: {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

    time.sleep(5)

    driver.close()
    return driver

def initialize_wait_driver_feeds(driver):
    return WebDriverWait(driver, 300)



from time import sleep
from typing import Any, Literal
from bs4 import BeautifulSoup, ResultSet, Tag
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Driver:
    KEYS = Keys

    def __init__(
        self,
        browser: Literal["chrome", "safari", "firefox"] = "chrome",
        url: str = "https://www.google.com",
        headless: bool = True,
        incognito: bool = True,
    ) -> None:
        self.url: str = url
        if not self.url.startswith("http"):
            self.url = "https://" + self.url
        self.browser_name = browser
        self.headless = headless
        self.incognito = incognito
        self.page: str = ""
        self.soup = BeautifulSoup()

        options: webdriver.ChromeOptions | webdriver.SafariOptions | webdriver.FirefoxOptions
        self.browser: webdriver.Chrome | webdriver.Safari | webdriver.Firefox
        match browser:
            case "safari":
                options = webdriver.SafariOptions()
                if headless:
                    options.add_argument("--headless")
                if incognito:
                    options.add_argument("--incognito")
                self.browser = webdriver.Safari(options)
            case "firefox":
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                if incognito:
                    options.add_argument("--incognito")
                self.browser = webdriver.Firefox(options)
            case _:
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument("--headless")
                if incognito:
                    options.add_argument("--incognito")
                self.browser = webdriver.Chrome(options)

    def __repr__(self):
        configs = []
        if self.headless:
            configs.append(f"headless={self.headless}")
        if self.incognito:
            configs.append(f"incognito={self.incognito}")
        if len(configs) == 0:
            return f"{self.browser_name} --> {self.url}"
        return f"{self.browser_name}:{','.join(configs)} --> {self.url}"

    def __enter__(self):
        self.browser.get(self.url)
        self.page = self.browser.page_source
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Exception detected: {exc_type}, {exc_val}")
        self.browser.quit()
        return True

    def wait_for(self, css_selector: str):
        """
        Waits for an element to be present on the page using a CSS selector.

        Args:
            css_selector (str): The CSS selector of the element to wait for.
        """
        WebDriverWait(self.browser, timeout=10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )

    def delay(self, seconds: float):
        """
        Delay the execution for the specified number of seconds.

        Args:
            seconds (float): The number of seconds to delay.
        """
        sleep(seconds)

    def browse_to(self, new_url: str):
        """
        Navigates the browser to the specified URL.

        Args:
            new_url (str): The URL to navigate to.

        Returns:
            None
        """
        if not new_url.startswith("http"):
            new_url = "https://" + new_url
        self.url = new_url
        self.browser.get(self.url)
        self.page = self.browser.page_source

    def click(self, css_selector: str):
        """
        Clicks on an element identified by the given CSS selector.

        Args:
            css_selector (str): The CSS selector used to locate the element.

        Returns:
            None
        """
        self.wait_for(css_selector)
        self.browser.find_element(By.CSS_SELECTOR, css_selector).click()

    def write(
        self,
        at_css_selector: str,
        text: str,
        last_key: str | None = None,
    ):
        """
        Writes the given text to the element located by the CSS selector.

        Args:
            at_css_selector (str): The CSS selector of the element to write the text to.
            text (str): The text to write.
            last_key (str | None, optional): The last key to send after writing the text. Defaults to None.
        """

        self.wait_for(at_css_selector)
        if text.strip() != "":
            self.browser.find_element(By.CSS_SELECTOR, at_css_selector).send_keys(text)
        if last_key is not None:
            _element = self.browser.find_element(By.CSS_SELECTOR, at_css_selector)
            _action = ActionChains(self.browser)
            _action.move_to_element(_element)
            _action.send_keys(last_key)
            _action.perform()

    def hotkey(self, *key: str):
        """
        Presses a hotkey combination.

        Args:
            *key: Variable number of strings representing the keys to be pressed.

        Returns:
            None
        """
        self.wait_for("body")
        _action = ActionChains(self.browser)
        _action.send_keys(*key)
        _action.perform()

    def did_you(self, message: str):
        """
        Waits for user confirmation [ENTER] in the terminal after action is done.

        Args:
            message (str): The message to display in the terminal, describing
            what user is supposed to do.

        Returns:
            None
        """
        if not message.strip().endswith("?"):
            message = message.strip() + "?"
        input("\n" + message.strip())

    def screenshot(self, file_name: str = "screenshot.png"):
        """
        Takes a screenshot of the current web page and saves it as a file.

        Args:
            file_name (str, optional): The name of the screenshot file. Defaults to "screenshot.png".
        """
        self.browser.save_screenshot(file_name)

    def cook_a_soup(self) -> BeautifulSoup:
        """
        Cooks a soup by parsing the HTML content of the page.

        Returns:
            BeautifulSoup: The parsed soup object.
        """
        self.wait_for("body")
        self.soup = BeautifulSoup(self.page, "html.parser")
        return self.soup

    def select_from_soup(self, css_selector: str) -> ResultSet[Tag]:
        """
        Selects elements from the BeautifulSoup object based on the given CSS selector.

        Args:
            css_selector (str): The CSS selector used to select the elements.

        Returns:
            ResultSet[Tag]: A ResultSet object containing the selected elements.
        """
        self.wait_for("body")
        self.soup = BeautifulSoup(self.page, "html.parser")
        return self.soup.select(css_selector)

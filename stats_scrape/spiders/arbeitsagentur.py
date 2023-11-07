import os

import scrapy
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from stats_scrape.items import ArbeitsAgenturScrapeItem

load_dotenv()


class ArbeitsAgenturSpider(scrapy.Spider):
    name = "arbeitsagentur"
    allowed_domains = ["arbeitsagentur.de"]
    ADVERTISES_COUNT_ON_PAGE = 25

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = self.create_driver_with_headless()
        self.driver_2 = self.create_driver_with_headless()
        self.search_word = kwargs.get("word")

    def start_requests(self):
        url = f"https://www.arbeitsagentur.de/jobsuche/suche?angebotsart=1&was={self.search_word}"
        yield scrapy.Request(url, self.parse)

    def parse(self, response, **kwargs):
        self.driver.get(response.url)

        self.accept_cookies(self.driver)
        advertisement_quantity = self.get_advertisement_quantity()
        self.click_weitere_button(advertisement_quantity)

        span_elements = self.driver.find_elements(By.TAG_NAME, "jb-job-listen-eintrag")

        for span_element in span_elements:
            yield self.scrape_single_element(span_element)

        self.driver.quit()
        self.driver_2.quit()

    def scrape_single_element(self, span_element):
        """Scraping info about every single advertisement"""
        advertisement = ArbeitsAgenturScrapeItem()

        position = span_element.find_element(By.CLASS_NAME, "mitte-links-titel.color-red")
        advertisement["position"] = self.driver.execute_script(
            "return arguments[0].textContent;",
            position
        )

        profession = span_element.find_element(By.CLASS_NAME, "oben")
        advertisement["profession"] = self.driver.execute_script(
            "return arguments[0].textContent;",
            profession
        )
        city = span_element.find_element(By.CLASS_NAME, "mitte-links-ort.ba-icon.ba-icon-location")
        advertisement["city"] = self.driver.execute_script(
            "return arguments[0].textContent;",
            city
        )
        company_name = span_element.find_element(By.CLASS_NAME, "mitte-links-arbeitgeber")
        advertisement["company_name"] = self.driver.execute_script(
            "return arguments[0].textContent;",
            company_name
        )

        href = span_element.find_element(By.CLASS_NAME, "ergebnisliste-item").get_property("href")
        advertisement["description"] = self.scrape_description_from_single_page(href)
        return advertisement

    def scrape_description_from_single_page(self, href):
        """Open single advertisement page and scraping the description"""
        self.driver_2.get(href)

        description = ""
        try:
            description_section = self.driver_2.find_element(By.ID, "jobdetails-beschreibung")
            description = self.driver_2.execute_script(
                "return arguments[0].textContent;",
                description_section
            )
        except NoSuchElementException:
            pass
        return description

    def click_weitere_button(self, advertisement_quantity) -> None:
        """Clicking Weitere(next page) button until the last page"""
        pages_quantity = round(
            advertisement_quantity / self.ADVERTISES_COUNT_ON_PAGE
        )
        weitere_button = self.driver.find_element(
            By.CLASS_NAME,
            "ba-btn.ba-btn-tertiary"
        )
        for page in range(pages_quantity):
            self.driver.execute_script("arguments[0].click();", weitere_button)
            id_page = f"ergebnisliste-liste-{page + 1}"
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.ID, id_page))
            )
            print("*" * 100)
            print("Clicked")

    def get_advertisement_quantity(self):
        """Getting advertisements quantity"""
        return int(
            self.driver.find_element(By.CLASS_NAME, "h6")
            .text.split()[0]
            .replace(".", "")
        )

    @staticmethod
    def create_driver_with_headless() -> WebDriver:
        """Creating WebDriver instance with headless option
         to run Selenium without opening a browser"""

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        return webdriver.Chrome(options=chrome_options)

    @staticmethod
    def accept_cookies(driver: WebDriver) -> None:
        """Clicking 'Accept cookies' button if exist"""
        try:
            element = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "hydrated"))
            )
            element.click()
            print("Cookies were accepted!!!")
        except Exception as e:
            print("Cookie consent button not found or failed to click:", e)

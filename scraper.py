from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import asyncio
from prisma import Prisma
from prisma.models import MobileNetworks

class Scraper:
    def __init__(self) -> None:
        self.prisma = None
        self.url = "https://mcc-mnc.com/"
        self.scroll_pause_time = 10
        self.item_count = 0
        self.current_page = 1
        self.last_page = 32 # by select "show 100 entries"
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)

    async def page(self) -> None:
        select = self.browser.find_element(By.NAME, "mncmccTable_length")
        select = Select(select)
        select.select_by_visible_text('100')

        rows = self.browser.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            mcc = None
            mnc = None
            iso = None
            country = None
            countryCode = None
            network = None
            for idx, col in enumerate(columns):
                if idx == 0:
                    mcc = col.text
                if idx == 1:
                    mnc = col.text
                if idx == 2:
                    iso = col.text
                if idx == 3:
                    country = col.text
                if idx == 4:
                    countryCode = col.text
                if idx == 5:
                    network = col.text
            exists = await self.exists(mcc, mnc, network, iso, country, countryCode)
            if exists == False:
                await self.store(mcc, mnc, network, iso, country, countryCode)
            else:
                continue

        WebDriverWait(self.browser, self.scroll_pause_time)

        nextButton = self.browser.find_element(By.ID, "mncmccTable_next")
        nextButton.click()
        await self.page()

    async def store(self, mcc, mnc, network, iso, country, countryCode) -> None:
        if mcc == None:
            return
        await self.prisma.mobilenetworks.create(
            data={
                "mcc": mcc,
                "mnc": mnc,
                "network": network,
                "iso": iso,
                "country": country,
                "countryCode": countryCode
            },
        )
        print("[Network: {}, Tag: {}{}]".format(network, mcc, mnc))

    async def exists(self, mcc, mnc, network, iso, country, countryCode) -> None:
        if mcc != "" and mcc != None and mnc != "" and mnc != None and network != "" and network != None and iso != "" and iso != None and country != "" and country != None and countryCode != "" and countryCode != None:
            search = await self.prisma.mobilenetworks.find_first(
                where={
                    "mcc": str(mcc),
                    "mnc": str(mnc),
                    "network": str(network),
                    "iso": str(iso),
                    "country": str(country),
                    "countryCode": str(countryCode)
                },
            )
            if search == None:
                return False
            else:
                return True
        else:
            return

    async def connectPrisma(self) -> None:
        self.prisma = Prisma(auto_register=True)
        await self.prisma.connect()

    async def disconnectPrisma(self) -> None:
        await self.prisma.disconnect()

async def main():
    scraper = Scraper()
    await scraper.connectPrisma()
    try:
        await scraper.page()
    finally:
        await scraper.disconnectPrisma()

asyncio.run(main())
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import asyncio
from prisma import Prisma
from prisma.models import MCC_MNC
import scraper

# Haupt-Event-Loop
async def main():
    scrape = scraper.Scraper()
    await scrape.connectPrisma()
    try:
        await scrape.page()
    finally:
        await scrape.disconnectPrisma()

if __name__ == '__main__':
    asyncio.run(main())

"""
model MCC_MNC {
  id            String      @id @default(uuid())
  mcc           String      @default("-")
  mnc           String      @default("-")
  network       String      @default("-")
  iso           String      @default("-")
  country       String      @default("-")
  countryCode   String      @default("-")
}
"""

"""
Test Data
"mcc": "202",
"mnc": "299",
"network": "AMD Telecom",
"iso": "gr",
"country": "Greece",
"countryCode": "30"
"""
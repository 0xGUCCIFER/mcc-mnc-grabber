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

async def main():
    scrape = scraper.Scraper()
    await scrape.connectPrisma()
    try:
        await scrape.page()
    finally:
        await scrape.disconnectPrisma()

if __name__ == '__main__':
    asyncio.run(main())
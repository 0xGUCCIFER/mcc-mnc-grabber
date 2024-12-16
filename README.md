# MCC-MNC Grabber
Python web scraper using Selenium to extract Mobile Network Codes (MNCs) and Mobile Country Codes (MCCs) from https://mcc-mnc.com/. The scraper navigates the site, interacts with its elements as needed, and systematically collects the data. 
<br/>
The scraper is designed to extract Mobile Country Code (MCC) and Mobile Network Code (MNC) data, which is used to identify mobile network operators worldwide. This includes names of providers like Telekom, Vodafone, and others, along with their associated MCC/MNC codes. The tool retrieves this information from public sources, such as https://mcc-mnc.com/.
<br/>
The host https://mcc-mnc.com/ provides information about Mobile Network Operators (MNOs). However, there seems to be a discrepancy: while the site claims to list 3,115 operators, only 3,078 are actually extracted. This might be due to how the data is structured in the HTML table.

![Alt text](images/table.png)

## Prisma Model
![Alt text](images/prismaModel.png)

## .env
- DATABASE_URL="dbtype://user:password@host/db?schema=public"

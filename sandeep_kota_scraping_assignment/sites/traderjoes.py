from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time

# Set up the Chrome WebDriver
opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

def scrape_product_data(product_url):
    pass

def scrape_pages(baseurl,href):
    each_page_products_data = []
    main_url = baseurl + href
    driver.maximize_window() 
    driver.get(main_url)
    driver.implicitly_wait(220) 
    time.sleep(5)
    page_response=driver.page_source
    driver.quit()
    page_soup = BeautifulSoup(page_response,'html.parser')
    products = page_soup.find_all('a',class_="Link_link__1AZfr ProductCard_card__img_link__2bBqA")
    print(len(products))
    # for product in products:
    #     product_href = product.get('href')
    #     product_url = baseurl + product_href
    #     print(product_url)
    #     product_data = scrape_product_data(product_url=product_url)
    #     if product_data:
    #         each_page_products_data.append(product_data)
    return each_page_products_data

def scrape_traderjoes(baseurl,href):
    products_data = []
    url = baseurl + href
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(220) 

    time.sleep(3)  # Wait for the page to load
    response = driver.page_source
    driver.quit()
    soup = BeautifulSoup(response, 'html.parser')
    total_pages = int("".join(filter(str.isdigit, soup.find('li',class_="PaginationItem_paginationItem__2f87h Pagination_pagination__lastItem__3eYWw Pagination_pagination__lastItem_shown__mExTm Pagination_pagination__lastItem_shownMobile__3xfjl Pagination_pagination__lastItem_pagesSkipped__1wdCc Pagination_pagination__lastItem_pagesSkippedMobile__2K1Fx").text.strip())))
    print(total_pages)
    products_data += scrape_pages(baseurl=baseurl,href=href)
    for page in range(2,total_pages+1):
        page_href = f'/home/products/category/products-2?filters=%7B"page"%3A{page}%7D'
        products_data+=scrape_pages(baseurl=baseurl,href=page_href)
    return products_data
    # return scrape_types(baseurl=baseurl,types_data=types_data)

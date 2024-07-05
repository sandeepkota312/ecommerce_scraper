from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time

opts = Options()
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

def scrape_product_data(product_url):
    driver.maximize_window() 
    driver.get(product_url)
    driver.implicitly_wait(220)
    time.sleep(4)
    product_response = driver.page_source
    product_soup = BeautifulSoup(product_response,'html.parser')
    try:
        title = product_soup.find('h1', class_="ProductDetails_main__title__14Cnm").text.strip()
    except Exception as e:
        print(f"Error extracting title: {e}")
        title = None

    try:
        description = "\n".join([para.text.strip() for para in product_soup.find('div', class_="ProductDetails_main__description__2R7nN").find_all('p') if para.text.strip()])
    except Exception as e:
        print(f"Error extracting description: {e}")
        description = None

    try:
        image = "https://www.traderjoes.com" + product_soup.find('div', class_="thumbnails").find('div',class_="slick-slide slick-active slick-current").find('img').get('src')
    except:
        try:
            image = "https://www.traderjoes.com" + product_soup.find('div',class_="Carousel_carousel__T71uo slider-wrapper").find('div',class_="slick-slide slick-active slick-current").find('img').get('src')
            print("Site has only one image")
        except Exception as e:
            print(f"Error extracting main image: {e}")
            image = None

    try:
        images = product_soup.find('div', class_="thumbnails").find_all('div',class_="slick-slide slick-active")
        product_images = ["https://www.traderjoes.com" + img.find('img').get('src') + ".jpeg" for img in images]
        if image:
            product_images.append(image)
    except Exception as e:
        print(f"Error extracting additional images: {e}")
        if image:
            product_images=[image]
        else:
            product_images=[]

    try:
        current_price = original_price = product_soup.find('span', class_="ProductPrice_productPrice__price__3-50j").text.strip()
    except Exception as e:
        print(f"Error extracting price: {e}")
        current_price = original_price = None

    try:
        quantity = product_soup.find('span', class_="ProductPrice_productPrice__unit__2jvkA").text.strip()[1:]
    except Exception as e:
        print(f"Error extracting quantity: {e}")
        quantity = None

    try:
        calories_per_serving = product_soup.find('div', class_="Item_characteristics__text__dcfEC").text.strip()
    except Exception as e:
        print(f"Error extracting calories per serving: {e}")
        calories_per_serving = None

    try:
        ingredients = product_soup.find_all('li', class_="IngredientsList_ingredientsList__item__1VrRy")
        product_ingredients = [ingredient.text.strip() for ingredient in ingredients]
    except Exception as e:
        print(f"Error extracting ingredients: {e}")
        product_ingredients = []

    try:
        factors = product_soup.find_all('a', class_="Button_unstyledButton__36gLi FunTag_tag__22xMB")
        product_factors = {factor.find('span').text.strip(): "https://www.traderjoes.com" + factor.get('href') for factor in factors}
    except Exception as e:
        print(f"Error extracting factors: {e}")
        product_factors = {}

    product_data = {
        "title":title,
        "url":product_url,
        "description":description,
        "image":image,
        "images":product_images,
        "price":current_price,
        "actual_price":original_price,
        "quantity":quantity,
        "calories_per_serving":calories_per_serving,
        "ingredients":product_ingredients,
        "factors":product_factors
    }
    # print(product_data)
    # print("\n")
    return product_data

# a=scrape_product_data("https://www.traderjoes.com/home/products/pdp/caesar-salad-with-white-chicken-meat-006832")

def scrape_pages(baseurl,href):
    each_page_products_data = []
    main_url = baseurl + href
    driver.maximize_window() 
    driver.get(main_url)
    driver.implicitly_wait(220) 
    time.sleep(3)
    page_response=driver.page_source
    page_soup = BeautifulSoup(page_response,'html.parser')
    products = page_soup.find_all('a',class_="Link_link__1AZfr ProductCard_card__img_link__2bBqA")
    for product in products:
        product_href = product.get('href')
        product_url = baseurl + product_href
        print(product_url)
        product_data = scrape_product_data(product_url=product_url)
        if product_data:
            each_page_products_data.append(product_data)
    return each_page_products_data

def scrape_traderjoes(baseurl,href):
    products_data = []
    url = baseurl + href
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(220) 

    time.sleep(3)
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')
    total_pages = int("".join(filter(str.isdigit, soup.find('li',class_="PaginationItem_paginationItem__2f87h Pagination_pagination__lastItem__3eYWw Pagination_pagination__lastItem_shown__mExTm Pagination_pagination__lastItem_shownMobile__3xfjl Pagination_pagination__lastItem_pagesSkipped__1wdCc Pagination_pagination__lastItem_pagesSkippedMobile__2K1Fx").text.strip())))
    print("total_pages",total_pages)
    print("page: 1")
    products_data += scrape_pages(baseurl=baseurl,href=href)
    for page in range(2,total_pages+1):
        print(f"page:{page}")
        page_href = f'/home/products/category/products-2?filters=%7B"page"%3A{page}%7D'
        products_data+=scrape_pages(baseurl=baseurl,href=page_href)
    driver.quit()
    return products_data

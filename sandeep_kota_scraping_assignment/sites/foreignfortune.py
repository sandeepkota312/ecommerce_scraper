import requests
import math
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

def scrape_product_data(product_url):
    try:
        product_response = requests.get(product_url)
        time.sleep(1)
        product_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching product URL: {product_url}, error: {e}")
        return None
    
    product_soup = BeautifulSoup(product_response.text,'html.parser')

    try:
        title = product_soup.find('h1',class_="product-single__title").text.strip()
        current_price = original_price = product_soup.find('span',id="ProductPrice-product-template").text.strip()
        description = product_soup.find('div',class_="product-single__description rte").text.strip()
        product_id = urlparse(product_url).path.split('/')[-1]

        main_image = "https:" + product_soup.find('div', class_="product-single__photo js-zoom-enabled product-single__photo--has-thumbnails").get('data-zoom')
        images = product_soup.find('ul', class_="grid grid--uniform product-single__thumbnails product-single__thumbnails-product-template").find_all('img')

        product_images = ["https:" + image.get('src') for image in images]
        if product_images == []:
            product_images.append(main_image)
    except:
        try:
            main_image = "https:"+product_soup.find('div', class_="product-single__photo js-zoom-enabled").get('data-zoom')
            product_images=[main_image]
        except AttributeError as e:
            print(f"Error parsing product details for URL: {product_url}, error: {e}")
            return None

    try:
        variants = product_soup.find('select', id="ProductSelect-product-template").find_all('option')
        product_variants = []
        for variant in variants:
            data = {"id": variant.get('value')}
            components_length = len(product_soup.find_all('div', class_="selector-wrapper js product-form__item"))
            if components_length:
                components = []
                for index in range(components_length):
                    components.append(product_soup.find('label', {'for': f'SingleOptionSelector-{index}'}).text.strip())

                values = variant.text.split(' / ')
                for index, value in enumerate(values):
                    data[components[index]] = value.strip()
            product_variants.append(data)
    except AttributeError as e:
        print(f"Error parsing product variants for URL: {product_url}, error: {e}")
        return None

    product_data = {
        "title": title,
        "url": product_url,
        "price": current_price,
        "actual_price": original_price,
        "image": main_image,
        "description": description,
        "product_id": product_id,
        "images": product_images,
        "models": product_variants
    }
    return product_data

def scrape_sections(baseurl, sections_data):
    products_data = []
    for each_section_data in sections_data:
        main_url = baseurl + each_section_data[-1]
        try:
            section_response = requests.get(main_url)
            time.sleep(1)
            section_response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching section URL: {main_url}, error: {e}")
            continue
        
        section_soup = BeautifulSoup(section_response.text, 'html.parser')
        
        try:
            total_products = int("".join(filter(str.isdigit, section_soup.find('span', class_="filters-toolbar__product-count").text.strip())))
            products_per_page = len(section_soup.find_all('a', class_="grid-view-item__link grid-view-item__image-container product-card__link"))
            total_pages = math.ceil(total_products / products_per_page)
        except (AttributeError, ValueError) as e:
            print(f"Error parsing section details for URL: {main_url}, error: {e}")
            continue

        for page in range(1, total_pages + 1):
            try:
                page_response = requests.get(f"{main_url}?page={page}")
                time.sleep(1)
                page_response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error fetching page URL: {main_url}?page={page}, error: {e}")
                continue
            
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            
            try:
                products = page_soup.find_all('a', class_="grid-view-item__link grid-view-item__image-container product-card__link")
            except AttributeError as e:
                print(f"Error parsing products for URL: {main_url}?page={page}, error: {e}")
                continue
            
            for product in products:
                product_href = product.get('href')
                product_url = baseurl + product_href
                print(product_url)
                product_data = scrape_product_data(product_url)
                if product_data:
                    product_data['category'] = each_section_data[0]
                    products_data.append(product_data)
    return products_data

# Function to scrape Foreign Fortune
def scrape_foreignfortune(baseurl):
    try:
        response = requests.get(baseurl)
        time.sleep(1)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching base URL: {baseurl}, error: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        sections = soup.find('ul', class_='site-nav list--inline site-nav--centered').find_all('a', class_="site-nav__link site-nav__link--main")
    except AttributeError as e:
        print(f"Error parsing sections for base URL: {baseurl}, error: {e}")
        return []
    
    sections_data = []
    for section in sections:
        href = section.get('href')
        text = section.text.strip()
        sections_data.append([text, href])
    
    # HACK: adding shoes section manually as it's not found in the main page
    sections_data.append(["shoes","/collections/shoes"])
    sections_data.append(["Foreign kids","/collections/foreign-kids"]) 
    
    return scrape_sections(baseurl=baseurl, sections_data=sections_data)

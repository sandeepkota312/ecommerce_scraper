import requests
from bs4 import BeautifulSoup
import re
# TODO: need to add sleep for every request

def scrape_product_data(product_url):
    try:
        product_response = requests.get(product_url)
        product_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching product URL: {product_url}, error: {e}")
        return None
    product_soup = BeautifulSoup(product_response.text,'html.parser')

    try:
        title = product_soup.find('h1',class_="productCard__title").text.strip().split('\n')[0]
        match_price = re.search(r'£\d+\.\d{2}',product_soup.find('button',class_="productActions__addToCart button add-to-cart add").text.strip())
        price = match_price.group(0) if match_price else None
        weight = product_soup.find('p',class_="productCard__weight").text.strip()
        description = product_soup.find('div',class_="productDescription__text wysiwyg-content product-description").text.strip()
        images = product_soup.find('ul',class_="productImages__list js-product-images-carousel keen-slider js-product-images-list").find_all('li',class_="productImages__item keen-slider__slide")
        product_images = [image.find('a').get('href') for image in images]
        try:
            variant = product_soup.find('p',class_="linkedProducts__title").text.strip()
        except Exception as e:
            print(f"No variants for this product, error: {e}")
            variant=None
    except Exception as e:
        print(f"Error parsing product details for URL: {product_url}, error: {e}")
        return None
    
    product_data={
        "title":title,
        "url":product_url,
        "price":price,
        "images":product_images,
        "description":description,
        "weight":weight,
        "variant":variant
    }
    # print(product_data)
    return product_data

def scrape_types(baseurl,types_data):
    products_data = []
    for each_type_data in types_data:
        main_url = baseurl + each_type_data[-1]
        type_response = requests.get(main_url)
        type_soup = BeautifulSoup(type_response.text,'html.parser')
        products =type_soup.find_all('div',class_='productMiniature js-product-miniature') + type_soup.find_all('div',class_='productMiniature js-product-miniature --oos')
        # print(len(products))
        for product in products:
            product_url = product.find('a').get('href')
            try:
                product_response = requests.get(product_url)
                product_response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error fetching product URL: {product_url[0]}, error: {e}")
                return 
            print("\n")
            print(product_url)
            product_data = scrape_product_data(product_url)
            if product_data:
                product_data['category'] = each_type_data[0]
                products_data.append(product_data)
    return products_data

# Function to scrape Le Chocolat Alain Ducasse
def scrape_lechocolat_alainducasse(baseurl):
    response = requests.get(baseurl+"/uk/")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        types = soup.find('ul',class_="homeCategoryPads__list").find_all('a',class_="homeCategoryPads__itemLink")
        types_data = []
        for each_type in types:
            href = each_type['href']
            text = each_type.find('p',class_="homeCategoryPads__line --top").text.strip() + each_type.find('p',class_="homeCategoryPads__line --bottom").text.strip()
            types_data.append([text,href])
        # HACK: Not found in the main section
        types_data.append(['gifts','/uk/chocolate-gift'])
        print(types_data)
    return scrape_types(baseurl=baseurl,types_data=types_data)
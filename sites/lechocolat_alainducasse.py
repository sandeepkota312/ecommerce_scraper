import requests
from bs4 import BeautifulSoup

# Function to scrape Le Chocolat Alain Ducasse
def scrape_lechocolat_alainducasse(baseurl):
    response = requests.get(baseurl)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for product in soup.find_all('li', class_='product-item'):
        product_id = product.get('data-id', '')
        name = product.find('a', class_='product-item-link').text.strip()
        description = product.find('div', class_='description').text.strip()
        images = [img['data-src'] for img in product.find_all('img')]
        price = product.find('span', class_='price').text.strip()
        sale_price = product.find('span', class_='sale-price').text.strip() if product.find('span', class_='sale-price') else ''
        sku = product.find('span', class_='sku').text.strip() if product.find('span', class_='sku') else ''
        product_url = product.find('a')['href']

        products.append({
            "id": product_id,
            "name": name,
            "description": description,
            "images": images,
            "price": price,
            "sale_price": sale_price,
            "sku": sku,
            "url": product_url
        })
    
    return products
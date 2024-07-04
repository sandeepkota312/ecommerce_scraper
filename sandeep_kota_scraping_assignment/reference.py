import requests
from bs4 import BeautifulSoup
import json

# Function to scrape Foreign Fortune
def scrape_foreignfortune(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for product in soup.find_all('div', class_='product-grid-item'):
        product_id = product.get('data-id', '')
        name = product.find('h2', class_='product-title').text.strip()
        description = product.find('div', class_='description').text.strip()
        images = [img['src'] for img in product.find_all('img')]
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

# Function to scrape Le Chocolat Alain Ducasse
def scrape_lechocolat_alainducasse(url):
    response = requests.get(url)
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

# Function to scrape Trader Joe's
def scrape_traderjoes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for product in soup.find_all('div', class_='product-item'):
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

# URLs to scrape
urls = {
    "foreignfortune": "https://foreignfortune.com",
    "lechocolat_alainducasse": "https://www.lechocolat-alainducasse.com/uk/",
    "traderjoes": "https://www.traderjoes.com"
}

# Scrape each website
foreignfortune_products = scrape_foreignfortune(urls['foreignfortune'])
lechocolat_alainducasse_products = scrape_lechocolat_alainducasse(urls['lechocolat_alainducasse'])
traderjoes_products = scrape_traderjoes(urls['traderjoes'])

# Combine all products
all_products = {
    "foreignfortune": foreignfortune_products,
    "lechocolat_alainducasse": lechocolat_alainducasse_products,
    "traderjoes": traderjoes_products
}

# Save the scraped data to a JSON file
output_file_path = "scraped_products.json"
with open(output_file_path, "w") as f:
    json.dump(all_products, f, indent=4)

print(f"Scraped product details have been saved to {output_file_path}")

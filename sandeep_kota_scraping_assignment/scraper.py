import json

from sites.foreignfortune import scrape_foreignfortune
from sites.lechocolat_alainducasse import scrape_lechocolat_alainducasse
from sites.traderjoes import scrape_traderjoes

# URLs to scrape
urls = {
    "foreignfortune": "https://foreignfortune.com",
    "lechocolat_alainducasse": "https://www.lechocolat-alainducasse.com",
    "traderjoes": "https://www.traderjoes.com"
}

# # Scrape each website
# foreignfortune_products = scrape_foreignfortune(baseurl=urls['foreignfortune'])
# # Save the scraped data to a JSON file
# output_file_path = f"output/scraped_products_foreignfortune.json"
# with open(output_file_path, "w") as f:
#     json.dump(foreignfortune_products, f, indent=4)

# print(f"Scraped product details have been saved to {output_file_path}")

# lechocolat_alainducasse_products = scrape_lechocolat_alainducasse(baseurl=urls['lechocolat_alainducasse'])
# # Save the scraped data to a JSON file
# output_file_path = f"output/scraped_products_lechocolat_alainducasse.json"
# with open(output_file_path, "w") as f:
#     json.dump(lechocolat_alainducasse_products, f, indent=4)

# print(f"Scraped product details have been saved to {output_file_path}")

traderjoes_products = scrape_traderjoes(baseurl=urls['traderjoes'],href="/home/products/category/products-2")
# # Save the scraped data to a JSON file
# output_file_path = f"output/scraped_products_traderjoes.json"
# with open(output_file_path, "w") as f:
#     json.dump(traderjoes_products, f, indent=4)

# print(f"Scraped product details have been saved to {output_file_path}")

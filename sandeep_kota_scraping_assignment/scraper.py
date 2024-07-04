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

# Scrape each website
# foreignfortune_products = scrape_foreignfortune(baseurl=urls['foreignfortune'])
# lechocolat_alainducasse_products = scrape_lechocolat_alainducasse(baseurl=urls['lechocolat_alainducasse'])
traderjoes_products = scrape_traderjoes(baseurl=urls['traderjoes'],href="/home/products/category/products-2")

# # Combine all products
# all_products = {
#     # "foreignfortune": foreignfortune_products,
#     # "lechocolat_alainducasse": lechocolat_alainducasse_products,
#     "traderjoes": traderjoes_products
# }

# # Save the scraped data to a JSON file
# for site in all_products:
#     output_file_path = f"output/scraped_products_{site}.json"
#     with open(output_file_path, "w") as f:
#         json.dump({site:all_products[site]}, f, indent=4)

#     print(f"Scraped product details have been saved to {output_file_path}")

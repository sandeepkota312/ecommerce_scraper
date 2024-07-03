import json

from sites.foreignfortune import scrape_foreignfortune
from sites.lechocolat_alainducasse import scrape_lechocolat_alainducasse
from sites.traderjoes import scrape_traderjoes

# URLs to scrape
urls = {
    "foreignfortune": "https://foreignfortune.com",
    "lechocolat_alainducasse": "https://www.lechocolat-alainducasse.com/uk/",
    "traderjoes": "https://www.traderjoes.com"
}

# Scrape each website
# foreignfortune_products = scrape_foreignfortune(baseurl=urls['foreignfortune'])
lechocolat_alainducasse_products = scrape_lechocolat_alainducasse(baseurl=urls['lechocolat_alainducasse'])
# traderjoes_products = scrape_traderjoes(baseurl=urls['traderjoes'])

# Combine all products
all_products = {
    # "foreignfortune": foreignfortune_products,
    "lechocolat_alainducasse": lechocolat_alainducasse_products,
    # "traderjoes": traderjoes_products
}

# Save the scraped data to a JSON file
output_file_path = "scraped_products_lechocolat_alainducasse.json"
with open(output_file_path, "w") as f:
    json.dump(all_products, f, indent=4)

print(f"Scraped product details have been saved to {output_file_path}")

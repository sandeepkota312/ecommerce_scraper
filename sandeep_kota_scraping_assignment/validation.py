import json

class Validation:
    def __init__(self, domain, products):
        self.domain = domain
        self.products = products

    def validate(self):
        errors = []
        
        for product in self.products:
            product_errors = self.validate_product(product)
            if product_errors:
                errors.append({
                    "domain": self.domain,
                    "product_url": product.get("url", "N/A"),
                    "errors": product_errors
                })
        
        return errors

    def validate_product(self, product):
        errors = []
        
        mandatory_fields = ["title", "price", "url","image"]
        for field in mandatory_fields:
            if field not in product or not product[field]:
                errors.append(f"Mandatory field '{field}' is missing or empty.")
        
        if "price" in product and "actual_price" in product:
            try:
                price = float("".join(filter(str.isdigit,product["price"])))
                actual_price = float("".join(filter(str.isdigit,product["actual_price"])))
                if price > actual_price:
                    errors.append("price is greater than Actual price.")
            except ValueError:
                errors.append("Price or Actual price is not a valid number.")
        
        if "images" not in product or not product["images"]:
            errors.append("Product does not have any images.")
        
        if "description" not in product or not product["description"]:
            errors.append("Product does not have description")
        
        return errors

data_paths = {
    "foreignfortune": "output/scraped_products_foreignfortune.json",
    "lechocolat_alainducasse": "output/scraped_products_lechocolat_alainducasse.json",
    "traderjoes": "output/scraped_products_traderjoes.json"
}
validation_errors = []
for domain in data_paths:
    with open(data_paths[domain], "r") as f:
        data = json.load(f)

    validator = Validation(domain=domain,products=data)
    validation_errors += validator.validate()

if validation_errors:
    print(f"{len(validation_errors)} Validation errors found:")
    for error in validation_errors:
        print(f"Domain: {error['domain']}, Product Url: {error['product_url']}, Errors: {', '.join(error['errors'])}")
        print("\n")
else:
    print("All products passed validation.")

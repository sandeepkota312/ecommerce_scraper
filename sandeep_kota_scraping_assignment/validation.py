import json

class Validation:
    def __init__(self, data):
        self.data = data

    def validate(self):
        errors = []
        
        for domain, products in self.data.items():
            for product in products:
                product_errors = self.validate_product(product)
                if product_errors:
                    errors.append({
                        "domain": domain,
                        "product_id": product.get("id", "N/A"),
                        "errors": product_errors
                    })
        
        return errors

    def validate_product(self, product):
        errors = []
        
        # Check mandatory fields
        mandatory_fields = ["id", "name", "price", "url"]
        for field in mandatory_fields:
            if field not in product or not product[field]:
                errors.append(f"Mandatory field '{field}' is missing or empty.")
        
        # Check sale price <= original price
        if "price" in product and "sale_price" in product:
            try:
                price = float(product["price"].replace('$', '').replace(',', ''))
                sale_price = float(product["sale_price"].replace('$', '').replace(',', ''))
                if sale_price > price:
                    errors.append("Sale price is greater than original price.")
            except ValueError:
                errors.append("Price or sale price is not a valid number.")
        
        # Each variant (model) has images and their respective prices
        if "images" not in product or not product["images"]:
            errors.append("Product does not have any images.")
        
        return errors

if __name__ == "__main__":
    # Load the scraped products data from JSON file
    input_file_path = "scraped_products.json"
    with open(input_file_path, "r") as f:
        data = json.load(f)
    
    # Validate the data
    validator = Validation(data)
    validation_errors = validator.validate()

    # Print the validation errors
    if validation_errors:
        print("Validation errors found:")
        for error in validation_errors:
            print(f"Domain: {error['domain']}, Product ID: {error['product_id']}, Errors: {', '.join(error['errors'])}")
    else:
        print("All products passed validation.")

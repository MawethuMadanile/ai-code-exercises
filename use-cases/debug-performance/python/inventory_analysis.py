from itertools import combinations
import time
import random

def find_product_combinations(products, target_price, price_margin=10):
    results = []
    lower = target_price - price_margin
    upper = target_price + price_margin

    for product1, product2 in combinations(products, 2):
        combined_price = product1['price'] + product2['price']
        if lower <= combined_price <= upper:
            results.append({
                'product1': product1,
                'product2': product2,
                'combined_price': combined_price,
                'price_difference': abs(target_price - combined_price)
            })

    results.sort(key=lambda x: x['price_difference'])
    return results

if __name__ == "__main__":
    product_list = [{'id': i, 'name': f'Product {i}', 'price': random.randint(5, 500)} for i in range(5000)]

    start_time = time.time()
    combinations_result = find_product_combinations(product_list, 500, 50)
    end_time = time.time()

    print(f"Found {len(combinations_result)} product combinations")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
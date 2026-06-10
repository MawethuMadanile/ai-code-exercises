def validate_order(order, inventory, customer_data):
    if order['item_id'] not in inventory:
        return 'Item not in inventory'
    if inventory[order['item_id']]['quantity'] < order['quantity']:
        return 'Insufficient quantity'
    if order['customer_id'] not in customer_data:
        return 'Customer not found'
    return None

def calculate_price(order, inventory, customer_data):
    price = inventory[order['item_id']]['price'] * order['quantity']
    if customer_data[order['customer_id']]['premium']:
        price *= 0.9
    return price

def calculate_shipping(price, customer_data, customer_id):
    if customer_data[customer_id]['location'] == 'domestic':
        return 5.99 if price < 50 else 0
    return 15.99

def process_orders(orders, inventory, customer_data):
    results, error_orders, total_revenue = [], [], 0

    for order in orders:
        error = validate_order(order, inventory, customer_data)
        if error:
            error_orders.append({'order_id': order['order_id'], 'error': error})
            continue

        price = calculate_price(order, inventory, customer_data)
        shipping = calculate_shipping(price, customer_data, order['customer_id'])
        tax = price * 0.08
        final_price = price + shipping + tax

        inventory[order['item_id']]['quantity'] -= order['quantity']
        total_revenue += final_price
        results.append({**order, 'price': price, 'shipping': shipping, 'tax': tax, 'final_price': final_price})

    return {'processed_orders': results, 'error_orders': error_orders, 'total_revenue': total_revenue}
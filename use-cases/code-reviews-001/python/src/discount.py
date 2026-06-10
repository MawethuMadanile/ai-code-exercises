def calculate_cart_total(cart):
    total = 0
    for item in cart:
        total += item['price'] * item['quantity']
    return total


def apply_promo_discount(promo, cart_total, user):
    if promo['type'] == 'percent':
        if promo['min_purchase'] is None or cart_total >= promo['min_purchase']:
            return cart_total * promo['value'] / 100

    elif promo['type'] == 'fixed':
        if promo['min_purchase'] is None or cart_total >= promo['min_purchase']:
            return min(promo['value'], cart_total)

    elif promo['type'] == 'shipping':
        if cart_total >= promo['min_purchase']:
            user['free_shipping'] = True

    return 0


def apply_user_discount(user, cart_total):
    if user['status'] == 'vip':
        return cart_total * 0.05
    elif user['status'] == 'member' and user['months'] > 6:
        return cart_total * 0.02
    return 0


def discount(cart, promos, user):
    cart_total = calculate_cart_total(cart)

    best_discount = 0

    for promo in promos:
        promo_discount = apply_promo_discount(promo, cart_total, user)
        best_discount = max(best_discount, promo_discount)

    user_discount = apply_user_discount(user, cart_total)
    best_discount = max(best_discount, user_discount)

    return {
        'original': cart_total,
        'discount': best_discount,
        'final': cart_total - best_discount,
        'free_shipping': user.get('free_shipping', False)
    }
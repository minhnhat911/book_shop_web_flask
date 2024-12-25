def stats_cart(cart):
    total_amount,total_quantity=0,0
    if cart:
        for c in cart.values():
            total_quantity+=c['quantity']
            total_amount+=c['quantity']*c['price']


    return {
        "total_amount":total_amount,
        "total_quantity":total_quantity
    }
# def stats_bill(bill):
#     total_amount,total_quantity=0,0
#     if bill:
#         for c in bill.values():
#             total_quantity+=c['quantity']
#             total_amount+=c['quantity']*c['price']
#
#
#     return {
#         "total_amount":total_amount,
#         "total_quantity":total_quantity
#     }
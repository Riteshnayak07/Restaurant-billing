def calculate_totals(items, menu_lookup, discount=0):
    subtotal = 0
    gst_total = 0
    for item_id, qty in items:
        item = menu_lookup.get(item_id)
        if item:
            price, gst = item
            subtotal += price * qty
            gst_total += (price * gst / 100) * qty
    total = subtotal + gst_total - discount
    return round(subtotal, 2), round(gst_total, 2), round(total, 2)
    

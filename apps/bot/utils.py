from services.main.schema import MainItemSchema

# def generate_caption(service_title, item: MainItemSchema):
#     full_price = f"{item.full_price:,} so'm" if item.full_price else ""
#     return (
#         f"<b>{service_title}:</b> {item.title}\n"
#         f"Narxi: <b>{int(item.sell_price):,} so'm</b> <s>{full_price}</s>"
#     ).replace(",", " ")

def generate_caption(service_title, item: MainItemSchema):
    full_price = f"{item.full_price:,} сум" if item.full_price else ""
    return (
        f"<b>{service_title}:</b> {item.title}\n"
        f"Цена: <b>{int(item.sell_price):,} сум</b> <s>{full_price}</s>"
    ).replace(",", " ")

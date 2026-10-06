import ast
import json
import re

# Product information used by the Gemini/Panel service-assistant exercise.
# This file is intentionally independent of the Gemini API.

PRODUCTS = {
    "TechPro Ultrabook": {
        "category": "Computers and Laptops",
        "model": "TP-UB100",
        "warranty": "1 year",
        "rating": 4.5,
        "display": '13.3"',
        "ram": "8GB",
        "storage": "256GB SSD",
        "processor": "Intel Core i5",
        "price": 799.99,
    },
    "BlueWave Gaming Laptop": {
        "category": "Computers and Laptops",
        "model": "BW-GL200",
        "warranty": "2 years",
        "rating": 4.7,
        "display": '15.6"',
        "ram": "16GB",
        "storage": "512GB SSD",
        "graphics": "RTX 3060",
        "price": 1199.99,
    },
    "PowerLite Convertible": {
        "category": "Computers and Laptops",
        "model": "PL-CV300",
        "warranty": "1 year",
        "rating": 4.3,
        "display": '14" touchscreen',
        "ram": "8GB",
        "storage": "256GB SSD",
        "feature": "360-degree hinge",
        "price": 699.99,
    },
    "TechPro Desktop": {
        "category": "Computers and Laptops",
        "model": "TP-DT500",
        "warranty": "1 year",
        "rating": 4.4,
        "processor": "Intel Core i7",
        "ram": "16GB",
        "storage": "1TB HDD",
        "graphics": "GTX 1660",
        "price": 999.99,
    },
    "BlueWave Chromebook": {
        "category": "Computers and Laptops",
        "model": "BW-CB100",
        "warranty": "1 year",
        "rating": 4.1,
        "display": '11.6"',
        "ram": "4GB",
        "storage": "32GB eMMC",
        "os": "Chrome OS",
        "price": 249.99,
    },

    "SmartX ProPhone": {
        "category": "Smartphones and Accessories",
        "model": "SX-PP10",
        "warranty": "1 year",
        "rating": 4.6,
        "display": '6.1"',
        "storage": "128GB",
        "camera": "12MP dual camera",
        "network": "5G",
        "price": 899.99,
    },
    "MobiTech PowerCase": {
        "category": "Smartphones and Accessories",
        "model": "MT-PC20",
        "warranty": "1 year",
        "rating": 4.3,
        "battery": "5000mAh",
        "charging": "Wireless charging",
        "compatibility": "SmartX ProPhone",
        "price": 59.99,
    },
    "SmartX MiniPhone": {
        "category": "Smartphones and Accessories",
        "model": "SX-MP5",
        "warranty": "1 year",
        "rating": 4.2,
        "display": '4.7"',
        "storage": "64GB",
        "camera": "8MP",
        "network": "4G",
        "price": 399.99,
    },
    "MobiTech Wireless Charger": {
        "category": "Smartphones and Accessories",
        "model": "MT-WC10",
        "warranty": "1 year",
        "rating": 4.5,
        "charging": "10W fast charging",
        "standard": "Qi",
        "feature": "LED indicator",
        "price": 29.99,
    },
    "SmartX EarBuds": {
        "category": "Smartphones and Accessories",
        "model": "SX-EB20",
        "warranty": "1 year",
        "rating": 4.4,
        "type": "True wireless",
        "bluetooth": "Bluetooth 5.0",
        "feature": "Touch controls",
        "battery": "24h",
        "price": 99.99,
    },

    "CineView 4K TV": {
        "category": "Televisions and Home Theater Systems",
        "model": "CV-4K55",
        "warranty": "2 years",
        "rating": 4.8,
        "display": '55"',
        "resolution": "4K",
        "feature": "HDR, Smart TV",
        "price": 599.99,
    },
    "SoundMax Home Theater": {
        "category": "Televisions and Home Theater Systems",
        "model": "SM-HT100",
        "warranty": "1 year",
        "rating": 4.4,
        "channels": "5.1",
        "power": "1000W",
        "feature": "Wireless subwoofer, Bluetooth",
        "price": 399.99,
    },
    "CineView 8K TV": {
        "category": "Televisions and Home Theater Systems",
        "model": "CV-8K65",
        "warranty": "2 years",
        "rating": 4.9,
        "display": '65"',
        "resolution": "8K",
        "feature": "HDR, Smart TV",
        "price": 2999.99,
    },
    "SoundMax Soundbar": {
        "category": "Televisions and Home Theater Systems",
        "model": "SM-SB50",
        "warranty": "1 year",
        "rating": 4.3,
        "channels": "2.1",
        "power": "300W",
        "feature": "Wireless subwoofer, Bluetooth",
        "price": 199.99,
    },
    "CineView OLED TV": {
        "category": "Televisions and Home Theater Systems",
        "model": "CV-OLED55",
        "warranty": "2 years",
        "rating": 4.7,
        "display": '55"',
        "resolution": "4K",
        "feature": "HDR, Smart TV, OLED",
        "price": 1499.99,
    },

    "GameSphere X": {
        "category": "Gaming Consoles and Accessories",
        "model": "GS-X",
        "warranty": "1 year",
        "rating": 4.9,
        "resolution": "4K",
        "storage": "1TB",
        "feature": "Backward compatibility, online multiplayer",
        "price": 499.99,
    },
    "ProGamer Controller": {
        "category": "Gaming Consoles and Accessories",
        "model": "PG-C100",
        "warranty": "1 year",
        "rating": 4.2,
        "feature": "Ergonomic, customizable buttons, wireless, rechargeable",
        "price": 59.99,
    },
    "GameSphere Y": {
        "category": "Gaming Consoles and Accessories",
        "model": "GS-Y",
        "warranty": "1 year",
        "rating": 4.8,
        "resolution": "4K",
        "storage": "500GB",
        "feature": "Backward compatibility, online multiplayer",
        "price": 399.99,
    },
    "ProGamer Racing Wheel": {
        "category": "Gaming Consoles and Accessories",
        "model": "PG-RW200",
        "warranty": "1 year",
        "rating": 4.5,
        "feature": "Force feedback, adjustable pedals, paddle shifters",
        "compatibility": "GameSphere X",
        "price": 249.99,
    },
    "GameSphere VR Headset": {
        "category": "Gaming Consoles and Accessories",
        "model": "GS-VR",
        "warranty": "1 year",
        "rating": 4.6,
        "feature": "Immersive VR, built-in headphones, adjustable headband",
        "compatibility": "GameSphere X",
        "price": 299.99,
    },

    "AudioPhonic Noise-Canceling Headphones": {
        "category": "Audio Equipment",
        "model": "AP-NC100",
        "warranty": "1 year",
        "rating": 4.6,
        "feature": "Active noise cancellation, Bluetooth, comfortable",
        "battery": "20h",
        "price": 199.99,
    },
    "WaveSound Bluetooth Speaker": {
        "category": "Audio Equipment",
        "model": "WS-BS50",
        "warranty": "1 year",
        "rating": 4.5,
        "feature": "Portable, water-resistant, built-in microphone",
        "battery": "10h",
        "price": 49.99,
    },
    "AudioPhonic True Wireless Earbuds": {
        "category": "Audio Equipment",
        "model": "AP-TW20",
        "warranty": "1 year",
        "feature": "True wireless, Bluetooth 5.0, touch controls",
        "battery": "18h",
        "price": 79.99,
    },
    "WaveSound Soundbar": {
        "category": "Audio Equipment",
        "model": "WS-SB40",
        "warranty": "1 year",
        "channels": "2.0",
        "power": "80W",
        "feature": "Bluetooth, wall-mountable",
        "price": 99.99,
    },
    "AudioPhonic Turntable": {
        "category": "Audio Equipment",
        "model": "AP-TT10",
        "warranty": "1 year",
        "feature": "3-speed, built-in speakers, Bluetooth, USB recording",
        "price": 149.99,
    },

    "FotoSnap DSLR Camera": {
        "category": "Cameras and Camcorders",
        "model": "FS-DSLR200",
        "warranty": "1 year",
        "rating": 4.7,
        "resolution": "24.2MP",
        "video": "1080p",
        "display": '3" LCD',
        "feature": "Interchangeable lenses",
        "price": 599.99,
    },
    "ActionCam 4K": {
        "category": "Cameras and Camcorders",
        "model": "AC-4K",
        "warranty": "1 year",
        "rating": 4.4,
        "resolution": "4K",
        "feature": "Waterproof, image stabilization, Wi-Fi",
        "price": 299.99,
    },
    "FotoSnap Mirrorless Camera": {
        "category": "Cameras and Camcorders",
        "model": "FS-ML100",
        "warranty": "1 year",
        "rating": 4.6,
        "resolution": "20.1MP",
        "video": "4K",
        "display": "Touchscreen",
        "feature": "Interchangeable lenses",
        "price": 799.99,
    },
    "ZoomMaster Camcorder": {
        "category": "Cameras and Camcorders",
        "model": "ZM-CM50",
        "warranty": "1 year",
        "rating": 4.3,
        "video": "1080p",
        "zoom": "30x optical zoom",
        "display": '3" LCD',
        "feature": "Image stabilization",
        "price": 249.99,
    },
    "FotoSnap Instant Camera": {
        "category": "Cameras and Camcorders",
        "model": "FS-IC10",
        "warranty": "1 year",
        "rating": 4.1,
        "feature": "Instant prints, built-in flash, selfie mirror",
        "power": "Battery-powered",
        "price": 69.99,
    },
}

CATEGORY_ALIASES = {
    "tv": "Televisions and Home Theater Systems",
    "tvs": "Televisions and Home Theater Systems",
    "television": "Televisions and Home Theater Systems",
    "televisions": "Televisions and Home Theater Systems",
    "camera": "Cameras and Camcorders",
    "cameras": "Cameras and Camcorders",
    "dslr": "Cameras and Camcorders",
    "laptop": "Computers and Laptops",
    "laptops": "Computers and Laptops",
    "computer": "Computers and Laptops",
    "computers": "Computers and Laptops",
    "phone": "Smartphones and Accessories",
    "phones": "Smartphones and Accessories",
    "smartphone": "Smartphones and Accessories",
    "smartphones": "Smartphones and Accessories",
    "gaming": "Gaming Consoles and Accessories",
    "console": "Gaming Consoles and Accessories",
    "consoles": "Gaming Consoles and Accessories",
    "audio": "Audio Equipment",
    "headphones": "Audio Equipment",
    "earbuds": "Audio Equipment",
    "speaker": "Audio Equipment",
}

def get_products_and_category():
    """Return all products grouped by category."""
    result = {}
    for product, info in PRODUCTS.items():
        category = info["category"]
        result.setdefault(category, []).append(product)
    return result

def _normalise(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

def find_category_and_product_only(user_input, products_and_category=None):
    """
    Extract likely product names/categories from a customer message.

    Returns a JSON list containing product names and/or category names.
    This is a local replacement for the course's missing utils.py.
    """
    text = _normalise(user_input)
    found = []

    # Exact product-name matching, longest names first.
    for product in sorted(PRODUCTS.keys(), key=len, reverse=True):
        if _normalise(product) in text:
            found.append(product)

    # Handle natural-language references used in the exercise.
    if ("smartx pro phone" in text or "smartx prophone" in text
            or "pro phone" in text):
        if "SmartX ProPhone" not in found:
            found.append("SmartX ProPhone")

    if ("fotosnap camera" in text and "dslr" in text) or "dslr camera" in text:
        if "FotoSnap DSLR Camera" not in found:
            found.append("FotoSnap DSLR Camera")

    # Category matching.
    for alias, category in CATEGORY_ALIASES.items():
        if re.search(r"\b" + re.escape(alias) + r"\b", text):
            if category not in found:
                found.append(category)

    # Return a JSON list so read_string_to_list can parse it.
    return json.dumps(found)

def read_string_to_list(text):
    """Convert a JSON/Python-list string into a Python list."""
    if isinstance(text, list):
        return text

    if not isinstance(text, str):
        return []

    text = text.strip()

    try:
        value = json.loads(text)
        return value if isinstance(value, list) else [value]
    except Exception:
        try:
            value = ast.literal_eval(text)
            return value if isinstance(value, list) else [value]
        except Exception:
            return [item.strip() for item in text.split(",") if item.strip()]

def generate_output_string(category_and_product_list):
    """
    Convert extracted product/category names into readable product information.
    """
    if not category_and_product_list:
        return "No matching products or categories were found."

    selected_products = []

    for item in category_and_product_list:
        if item in PRODUCTS:
            selected_products.append(item)
        elif item in get_products_and_category():
            for product in get_products_and_category()[item]:
                if product not in selected_products:
                    selected_products.append(product)

    if not selected_products:
        return "No matching products were found in the product catalog."

    lines = []
    for product in selected_products:
        info = PRODUCTS[product]
        lines.append(f"Product: {product}")
        for key, value in info.items():
            if key != "category":
                label = key.replace("_", " ").title()
                if key == "price":
                    value = f"${value:.2f}"
                lines.append(f"  {label}: {value}")
        lines.append("")

    return "\n".join(lines).strip()


def get_products_from_query(customer_msg):
    """
    Compatibility function for the course notebook.
    Finds products/categories mentioned in a customer query and
    returns them as a JSON list string.
    """
    return find_category_and_product_only(
        customer_msg,
        get_products_and_category()
    )


def get_mentioned_product_info(category_and_product_list):
    """
    Compatibility function for the course notebook.
    Returns product information for the extracted products/categories.
    """
    return generate_output_string(category_and_product_list)


def answer_user_msg(user_msg, product_info):
    """
    Local customer-service response helper.
    This function does not call Gemini; it formats the retrieved
    product information into a useful response.
    """
    if not product_info or "No matching" in product_info:
        return (
            "I could not find matching products in the available "
            "product catalog. Could you please provide the product name?"
        )

    return (
        "Sure! Here is the information available for the products "
        "you asked about:\n\n" + product_info +
        "\n\nPlease let me know if you have any other questions."
    )
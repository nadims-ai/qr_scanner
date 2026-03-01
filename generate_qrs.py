import os
import sys
import json
import socket
import argparse

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

try:
    import qrcode
except ImportError:
    print("Installing qrcode...")
    os.system('pip3 install qrcode pillow')
    import qrcode

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_qrs(custom_base_url=None):
    # Load products
    try:
        with open('products.json', 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        print("Error: products.json not found in current directory.")
        sys.exit(1)

    # Make output directory
    output_dir = "qr_codes"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ip_address = get_local_ip()
    port = 8000
    
    # If custom domain is provided, use it, else default to local IP
    base_url = custom_base_url if custom_base_url else f"http://{ip_address}:{port}"

    print(f"Generating QR Codes pointing to {base_url} ...\n")

    for product_id, product_data in products.items():
        name = product_data.get('name', 'Product')
        product_url = f"{base_url}/?id={product_id}"
        
        # Generate QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(product_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save file
        filename = f"{product_id}_qr.png"
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        print(f"✅ Generated {filename} for {product_id} ({name}) -> {product_url}")

    print(f"\nDone! QR Codes saved in the '{output_dir}' directory.")
    print(f"To test, run this command in this terminal:")
    print(f"python3 -m http.server {port}")

if __name__ == "__main__":
    generate_qrs()

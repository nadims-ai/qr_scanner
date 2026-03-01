import json
import os
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
import generate_qrs

PORT = 8000
DATA_FILE = 'products.json'

class RetailAPIHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow CORS if needed later
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_POST(self):
        if self.path == '/api/products':
            # Handle saving new product
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse new product data
                new_product = json.loads(post_data.decode('utf-8'))
                product_id = new_product.pop('id') # Extract the ID to use as the key
                
                # Load existing products
                with open(DATA_FILE, 'r') as f:
                    products = json.load(f)
                
                # Add or update the product
                products[product_id] = new_product
                
                # Save back to JSON
                with open(DATA_FILE, 'w') as f:
                    json.dump(products, f, indent=2)
                
                # Regenerate QR Codes locally
                print("New product added, regenerating QR codes...")
                generate_qrs.generate_qrs()
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "Product saved and QR code generated"}).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RetailAPIHandler)
    print(f"Server running on port {PORT}...")
    httpd.serve_forever()

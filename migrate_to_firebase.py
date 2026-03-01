import json
import urllib.request

FIREBASE_URL = 'https://qr-scanner-dd1-default-rtdb.firebaseio.com/products.json'

print("Loading local products.json...")
try:
    with open('products.json', 'r') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading local file: {e}")
    exit(1)

print(f"Uploading {len(data)} products to Firebase...")

req = urllib.request.Request(
    FIREBASE_URL,
    data=json.dumps(data).encode('utf-8'),
    method='PUT',
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        if response.status == 200:
            print("✅ Successfully migrated all data to Firebase!")
        else:
            print(f"❌ Failed with status: {response.status}")
except Exception as e:
    print(f"❌ Error uploading to Firebase: {e}")

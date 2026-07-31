import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# 1. Shared Secret Key (Must be 32 bytes for AES-256)
SECRET_KEY = b'GTRE_SECRET_KEY_32BYTES_LONG_!!!'

# 2. Raw Telemetry Data
telemetry_data = '{"RPM": 14200, "Temp_C": 760, "Pressure_PSI": 58}'.encode('utf-8')

# 3. Encrypt using AES-256-GCM
cipher = AES.new(SECRET_KEY, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(telemetry_data)

# 4. Connect to Ground Control Station
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5000))

print("🔒 Encrypting telemetry data...")
print(f"📦 Encrypted Payload (Hex): {ciphertext.hex()[:20]}...")

# 5. Send Nonce + Tag + Ciphertext together
payload = cipher.nonce + tag + ciphertext
client_socket.send(payload)

client_socket.close()
print("🚀 Encrypted transmission complete.")

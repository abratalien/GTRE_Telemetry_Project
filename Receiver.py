import socket
from Crypto.Cipher import AES

# 1. Must use the exact same 32-byte key
SECRET_KEY = b'GTRE_SECRET_KEY_32BYTES_LONG_!!!'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allowing port reuse in case script restarts quickly
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen(1)

print("📡 Ground Control Station waiting for ENCRYPTED telemetry...")

conn, addr = server_socket.accept()
print(f"✅ Connected to Engine Transmitter at {addr}")

# 2. Receive the encrypted payload
payload = conn.recv(1024)

# 3. Extract components (16 bytes Nonce + 16 bytes Tag + Ciphertext)
nonce = payload[:16]
tag = payload[16:32]
ciphertext = payload[32:]

# 4. Decrypt and Verify
try:
    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    print("🔓 Decryption & Integrity Check Successful!")
    print(f"📩 Decrypted Telemetry: {decrypted_data.decode('utf-8')}")
except Exception as e:
    print("❌ Security Alert! Data tampered or wrong key!")

conn.close()

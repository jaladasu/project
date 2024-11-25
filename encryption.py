from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# AES Encryption Helper Functions
KEY = b'your256bitkeyyour256bitkey!!'  # Ensure this is 32 bytes long
KEY = KEY.ljust(32, b'\0')  # Pad the key to ensure it's 32 bytes

def encrypt(data: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + encrypted_data).decode('utf-8')

def decrypt(data: str) -> str:
    raw_data = base64.b64decode(data)
    iv = raw_data[:16]
    encrypted_data = raw_data[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')

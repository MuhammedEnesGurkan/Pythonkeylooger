#Kötü amaçlar için kullanmayınız sadece kodlama eğitimi amaçlı geliştirilmiştir.

import socket
import datetime
from cryptography.fernet import Fernet

# Sunucu soketini oluştur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 12345
s.bind((host, port))

# Veriyi al
key = b'Lp5m5bDamhp_0rGDFF1LE-UsFwz0tt6CFPKTYuLmfxI='  # Anahtar sabit olmalı ve her iki tarafta aynı olmalı
cipher_suite = Fernet(key)


def decrypt_message(encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message)
    return decrypted_message.decode()


def receive_all(conn, buffer_size=1024): # veri küçükse hata almadan veriyi almak için
    data = b''
    while True:
        part = conn.recv(buffer_size)
        data += part
        if len(part) < buffer_size:  # Daha fazla veri gelmiyorsa döngüyü kır
            break
    return data


# Sunucunun dinlemesi
s.listen(1)
print("Sunucu dinlemeye başladı...")
dosyaa = "serverdosya.txt"

while True:
    conn, addr = s.accept()
    print(f"Bağlantı alındı: {addr}")

    veri = receive_all(conn)  # Tüm veriyi alıyoruz
    dec_message = decrypt_message(veri)  # Şifreyi çöz

    if dec_message:
         #print("Deşifre edilmiş veri:", dec_message)
        try:
            with open(dosyaa, 'w') as dosya:
                writing_Time = datetime.datetime.now()
                dosya.write(f"Yazılış Tarihi: {str(writing_Time)} \n")
                dosya.write(dec_message + '\n')
                print("Veri dosyası yazıldı.")
        except FileNotFoundError:
            print(f"'{dosyaa}' dosyası bulunamadı.")
    else:
        print("Veri alınamadı.")

    conn.close()

s.close()

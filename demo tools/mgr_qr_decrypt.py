# -*- coding:utf-8 -*-
from Crypto.Cipher import AES
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import tkinter as tk
from tkinter import messagebox

private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAohQ7j01IKXoDgRZlTPKw8dRON07CaLP/Wys9b8vAJYT6iUOB
7zIv/Gtm7Wqq6aMXo8+lt0flsbL6wYZUltfcf2HPgcaOWRXZKLhJQeVMmP4F75fs
eYRoUPZGrUIfxoYwLWWroSRjVA7FB93IMmLkGN83O1PsumC1imMEXkNvKjFVatc4
c72vgPl5RD8TX16juRrONFWmqa5iMziVtindBC+nSRTeljIImIrZAE5ZZWIXAGha
h6tV5EET3wgcx4ncBUu5Eh+2I7I4yxqMtMPI8uxUuQS+nB3ZwJiwnqX48P5XUitt
b2ySKV2535K7hL/daYBdg/j6QPkLy0yU0nDEgwIDAQABAoIBAH4HXYjAfyxBRBhM
YdjDnfNtMqSvCVyBGj66ELuto2uJS4cQhyiHzehpW0+hceTafLdT73fk4CadFX8G
BSCGGV6zn7c5vdZntsSDB/PFaRpN7C+x4p9a5gKOfcabdDnaffvO4vYaZWInWe4T
9me3ncX5S+lGCP2j1YYWGH9z0Cztkm4FBuOz4dJMVlZW0VtIHs3QCxR3nWuGpBeD
YiMsL1XvAfM9r5P+e98yL9hrAu/Q0lOitIezd4f+bBys1u69NsSaDjOez2aek4B3
sb4KlFNd+EOVXuSjEn/pZYanmAipqmqFEGiNPuDQmKxSFKGI6H83X1ymqZt/kcUZ
79c6VoECgYEA1VymNFdCKrVwI/Vr5DKgmNfzYVNO9RsMU2SEfnSboQP9V0xod/1E
YSXSNnJcbaiAdqZyFyRnFVd16uPqvFKMa0W5jGr0uLoz3hAbGhmYn71DyQ7LwHCX
B+nhy8wa54Q4KpFD7arTj7ps9Y+DMO2G1bBj/mRwQze9qR+w2UdkHq0CgYEAwngC
nS9ltXjrG76ksBar6DUSuUtuc1Rre+NSoC9mHSAdS2TshvsT/paUOqeH2Mt9tRD0
X6DLh7TKk6pfG1rtVmAo3eU72pToPXpmKHhNtgo+Tza7rEvUBqGbIvQTJwuCe2ve
R/+bJHFGKOEqyMi/ShLP3CtRtLG8Z2OcwK5xxe8CgYB6imPK2/LcpKhrfqEgxxMF
tcHKvBY1H/vMSYbvOfnIWIpAgVne0E9dnGNHchczw/tEKgSM1hN+ZmULKyu+TYro
cXtH8oXrMsZnW8i1DM5jsEgmSaEsPX4AxYsxiWBKZ936VMQ21E391oyN3Ib0qvct
88j6aqUvdewwHktr/1y5YQKBgQDCQhOKZOBayPFCg8wLQnpyuSF9C0bH2hqMZOYS
sYZ1rbDVsXk81O6CMHTdqqBfBdcK2mbiZ8MoSobZvyTGNKxEzkXEcsq5bGoZj30h
DBvErrLTej86u3yPKzvHTL0dEbhEBdrDXSfi3WxSRarxaub63ZPZwUQbFji3pp/d
MeTg7QKBgDWiiuZcBnfFr2D9UgHFlGuHFmeqO+lhIA+yAmu9SjCA2DlgHgRG68UB
s0ypiWWrhiE5VqMWp+pKY8KsZYrMqWco+Zf5jzwcsfGxy29e+6QzF1xvCTUHW1rI
7rk8N6sbX5q8BVsQWRC3PNqca4Y4EAMqTqYBN9TmwQjzUQdg4pkN
-----END RSA PRIVATE KEY-----'''

public_key = '''-----BEGIN PUBLIC KEY-----
hfgghftetet
-----END PUBLIC KEY-----'''

def rsa_encrypt(message):
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(public_key))
    return base64.b64encode(cipher.encrypt(message.encode())).decode()

def rsa_decrypt(text):
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(private_key))
    return cipher.decrypt(base64.b64decode(text), 'ERROR').decode('utf-8')

def decode_passwd(passwd):
    tmp_str = passwd.replace(" ", "").replace("\n", "")
    for _ in range(4):
        offset = tmp_str[-2]
        if not offset.isdigit():
            raise Exception(f"passwd is invalid:{passwd}, offset:{offset}")
        offset = int(offset)
        tmp_str = tmp_str[:-2]
        tmp_str = tmp_str[-offset:] + tmp_str[:-offset]
    return tmp_str[::-1]

def decrypt_text():
    txt = txt_entry.get().replace(" ", "").replace("\n", "")
    try:
        decrypted_txt = decode_passwd(rsa_decrypt(txt)).replace(" ", "").replace("\n", "")
        result_text.set(decrypted_txt)
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")

def on_text_change(event):
    global timer_id
    if timer_id:
        app.after_cancel(timer_id)
    timer_id = app.after(1000, decrypt_text)  # 3-second delay

def copy_to_clipboard():
    app.clipboard_clear()
    app.clipboard_append(result_text.get())
    messagebox.showinfo("Copied", "Decrypted text copied to clipboard!")

# GUI setup
app = tk.Tk()
app.title("RSA Decryption Tool")

timer_id = None

tk.Label(app, text="Enter Encrypted Text:").pack()
txt_entry = tk.Entry(app, width=50)
txt_entry.pack()
txt_entry.bind("<KeyRelease>", on_text_change)

result_text = tk.StringVar()
tk.Label(app, text="Decrypted Text:").pack()
tk.Entry(app, textvariable=result_text, width=50, state="readonly").pack()

tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard).pack()

app.mainloop()
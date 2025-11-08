import qrcode as qr
data="http://192.168.1.168:8000/"
code=qr.make(data)
code.save("code.png")
print("done")
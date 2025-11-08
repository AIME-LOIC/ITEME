import qrcode as qr
data="https://iteme-charity-wk9f.onrender.com"
code=qr.make(data)
code.save("final_image.png")
print("done")

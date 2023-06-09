import qrcode

# Generate QR code for a given string
def generate_qr_code(data, file_name):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)

# Example usage
generate_qr_code("ALI_QR_CODE_STRING", "ALI.png")
generate_qr_code("MELEK_QR_CODE_STRING", "MELEK.png")
generate_qr_code("MORAD_QR_CODE_STRING", "MORAD.png")


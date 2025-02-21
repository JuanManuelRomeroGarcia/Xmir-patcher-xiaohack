import qrcode

def show_donation_link():
    url = "https://www.paypal.com/donate/?hosted_button_id=S29YHTJCRPYH8"
    print("\n\U0001F90D Apoya el proyecto escaneando el código QR o ingresando al enlace:")
    print(url)
    print("\n\U0001F4F7 Escanea el siguiente QR directamente desde la terminal:\n")
    
    qr = qrcode.QRCode(
        version=2,  # Reduce el tamaño del QR
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,  # Tamaño más compacto
        border=0
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_matrix = qr.modules
    for y in range(0, len(qr_matrix), 2):  # Une dos filas en una sola línea
        row_top = qr_matrix[y]
        row_bottom = qr_matrix[y + 1] if y + 1 < len(qr_matrix) else [0] * len(row_top)
        line = "".join(["█" if top and bottom else "▀" if top else "▄" if bottom else " " for top, bottom in zip(row_top, row_bottom)])
        print(line)
    
    input("\nPresiona ENTER para volver al menú...")  # Pausa hasta que el usuario presione ENTER

if __name__ == "__main__":
    show_donation_link()
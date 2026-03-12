import qrcode

def gerar_qrcode(mensagem, nome_arquivo="qrcode.png"):
    # Cria o objeto QR Code
    qr = qrcode.QRCode(
        version=None,  # tamanho automático
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    # Adiciona a mensagem
    qr.add_data(mensagem)
    qr.make(fit=True)

    # Gera a imagem
    img = qr.make_image(fill_color="black", back_color="white")

    # Salva o arquivo
    img.save(nome_arquivo)

    print(f"QR Code gerado e salvo como {nome_arquivo}")

if __name__ == "__main__":
    mensagem = input("Digite a mensagem para o QR Code: ")
    gerar_qrcode(mensagem)
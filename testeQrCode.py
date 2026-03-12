import cv2
from pyzbar.pyzbar import decode

def ler_qrcode():
    # Abre a webcam (0 = câmera padrão)
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return

    print("Aproxime o QR Code da câmera. Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Erro ao capturar imagem.")
            break

        # Detecta QR Codes no frame
        qrcodes = decode(frame)

        for qrcode in qrcodes:
            # Extrai os dados
            dados = qrcode.data.decode("utf-8")
            print("QR Code detectado:", dados)

            # Desenha um retângulo ao redor do QR Code
            x, y, w, h = qrcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Mostra o texto na tela
            cv2.putText(frame, dados, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

        cv2.imshow("Leitor de QR Code", frame)

        # Sai ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    ler_qrcode()
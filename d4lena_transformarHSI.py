import os
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

# PIXEL A PIXEL - RGB/BGR -> HSI
#
# Fórmulas da literatura (com R,G,B em [0,1]):
#   I = (R + G + B) / 3
#   S = 1 - (3 * min(R,G,B)) / (R + G + B)
#   H = arccos( ((R-G)+(R-B)) / (2*sqrt((R-G)^2 + (R-B)(G-B))) )
#   Se B > G então H = 360 - H
#
# Tratamentos "acadêmicos" necessários:
# - Se (R+G+B) == 0  -> S = 0   (pixel preto)
# - Se denominador do H == 0 -> H = 0 (H indefinido quando S=0 / tons de cinza)
# - Clamp do argumento do acos para [-1, 1] (evita erro numérico)
# - Retorna H em graus [0,360], S e I em [0,1]


def bgr_para_hsi(img_bgr):
    # 1) Normaliza BGR (0..255) -> (0..1) em float
    bgr = img_bgr.astype(np.float32) / 255.0

    # 2) Separa canais no padrão OpenCV (B,G,R)
    B = bgr[:, :, 0]
    G = bgr[:, :, 1]
    R = bgr[:, :, 2]

    # 3) Prepara matrizes de saída H, S, I
    altura, largura = B.shape
    H = np.zeros((altura, largura), dtype=np.float32)  # H em graus
    S = np.zeros((altura, largura), dtype=np.float32)  # S em [0,1]
    I = np.zeros((altura, largura), dtype=np.float32)  # I em [0,1]

    # 4) Loop pixel a pixel (didático)
    for i in range(altura):
        for j in range(largura):

            # 4.1) Valores do pixel (já normalizados 0..1)
            r = float(R[i, j])
            g = float(G[i, j])
            b = float(B[i, j])

            # Intensidade: I = (R+G+B)/3
            I[i, j] = (r + g + b) / 3.0

            # Saturação: S = 1 - (3*min)/(R+G+B)
            soma = r + g + b
            if soma == 0.0:
                # pixel preto: saturação definida como 0
                S[i, j] = 0.0
            else:
                minimo = min(r, g, b)
                S[i, j] = 1.0 - (3.0 * minimo / soma)

            # Matiz (Hue):
            #   H = arccos( num / den )
            #   se B > G -> H = 360 - H
            num = (r - g) + (r - b)
            den = 2.0 * math.sqrt((r - g) ** 2 + (r - b) * (g - b))

            if den == 0.0:
                # tons de cinza / saturação ~ 0 => H indefinido
                # convenção: H = 0
                H[i, j] = 0.0
            else:
                valor = num / den

                # clamp do argumento para o domínio do acos: [-1, 1]
                if valor < -1.0:
                    valor = -1.0
                elif valor > 1.0:
                    valor = 1.0

                theta = math.acos(valor)  # em radianos (0..pi)
                h_graus = theta * (180.0 / math.pi)  # converte para graus

                # ajuste de quadrante: se B > G então H = 360 - H
                if b > g:
                    h_graus = 360.0 - h_graus

                H[i, j] = h_graus

    return H, S, I


if __name__ == "__main__":

    # 1) Caminhos
    caminho_imagem = "lena-Color.png"
    pasta_saida = "canaisHSI_lena"
    os.makedirs(pasta_saida, exist_ok=True)

    # 2) Ler imagem
    img_bgr = cv2.imread(caminho_imagem)
    if img_bgr is None:
        raise FileNotFoundError(f"Não foi possível ler a imagem: {caminho_imagem}")

    # 3) Converter BGR -> HSI  (pixel a pixel) e salvar imagem hsi
    H, S, I = bgr_para_hsi(img_bgr)
    
    hsi_img = cv2.merge((H, S, I))

    cv2.imwrite("canaisHSI_lena/imagem_HSI.tiff", hsi_img)

    # 4) Preparar para salvar em PNG (8-bit)
    # H: 0..360 -> 0..255
    # S: 0..1   -> 0..255
    # I: 0..1   -> 0..255
    H_8bit = (H / 360.0 * 255.0).astype(np.uint8)
    S_8bit = (S * 255.0).astype(np.uint8)
    I_8bit = (I * 255.0).astype(np.uint8)

    # 5) Salvar canais
    caminho_H = os.path.join(pasta_saida, "canal_H.png")
    caminho_S = os.path.join(pasta_saida, "canal_S.png")
    caminho_I = os.path.join(pasta_saida, "canal_I.png")

    cv2.imwrite(caminho_H, H_8bit)
    cv2.imwrite(caminho_S, S_8bit)
    cv2.imwrite(caminho_I, I_8bit)

    hsi_img = cv2.merge((H_8bit, S_8bit, I_8bit))

    cv2.imwrite("canaisHSI_lena/imagem_8bit_HSI.png", hsi_img)

    # 6) Relatório rápido
    print("HSI (pixel a pixel) concluído e salvo.")
    print(f"- {caminho_H}")
    print(f"- {caminho_S}")
    print(f"- {caminho_I}")

    # Ler imagens em escala de cinza
    H = cv2.imread(caminho_H, cv2.IMREAD_GRAYSCALE)
    S = cv2.imread(caminho_S, cv2.IMREAD_GRAYSCALE)
    I = cv2.imread(caminho_I, cv2.IMREAD_GRAYSCALE)

    if H is None or S is None or I is None:
        raise FileNotFoundError("Não foi possível carregar um ou mais canais HSI.")

    # Plotar lado a lado
    plt.figure(figsize=(12,5))

    plt.subplot(1,3,1)
    plt.imshow(H, cmap='gray')
    plt.title("Canal H")
    plt.axis("off")

    plt.subplot(1,3,2)
    plt.imshow(S, cmap='gray')
    plt.title("Canal S")
    plt.axis("off")

    plt.subplot(1,3,3)
    plt.imshow(I, cmap='gray')
    plt.title("Canal I")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

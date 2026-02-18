import os  # pastas
import cv2  # leitura e escrita
import numpy as np  # arrays
import math  # acos, sqrt
import matplotlib.pyplot as plt  # plot

def bgr_para_hsi_pixel_a_pixel(img_bgr):
    bgr = img_bgr.astype(np.float32) / 255.0  # normaliza para [0,1]
    B = bgr[:, :, 0]  # canal B
    G = bgr[:, :, 1]  # canal G
    R = bgr[:, :, 2]  # canal R

    altura, largura = B.shape  # dimensões
    H = np.zeros((altura, largura), dtype=np.float32)  # H em graus
    S = np.zeros((altura, largura), dtype=np.float32)  # S em [0,1]
    I = np.zeros((altura, largura), dtype=np.float32)  # I em [0,1]

    for i in range(altura):  # linha
        for j in range(largura):  # coluna
            r = float(R[i, j])  # R do pixel
            g = float(G[i, j])  # G do pixel
            b = float(B[i, j])  # B do pixel

            I[i, j] = (r + g + b) / 3.0  # intensidade

            soma = r + g + b  # soma RGB
            if soma == 0.0:  # pixel preto
                S[i, j] = 0.0  # saturação definida como 0
            else:
                minimo = min(r, g, b)  # min(R,G,B)
                S[i, j] = 1.0 - (3.0 * minimo / soma)  # saturação

            num = (r - g) + (r - b)  # numerador do cos
            den = 2.0 * math.sqrt((r - g) ** 2 + (r - b) * (g - b))  # denominador

            if den == 0.0:  # caso indefinido
                H[i, j] = 0.0  # convenção
            else:
                valor = num / den  # argumento do acos
                if valor < -1.0:  # clamp inferior
                    valor = -1.0
                elif valor > 1.0:  # clamp superior
                    valor = 1.0

                theta = math.acos(valor)  # radianos
                h_graus = theta * (180.0 / math.pi)  # graus

                if b > g:  # ajuste de quadrante
                    h_graus = 360.0 - h_graus

                H[i, j] = h_graus  # matiz em graus

    return H, S, I  # retorna canais

caminho_imagem = "top_mosaic_09cm_area35.tif"  # entrada
pasta_saida = "canaisHSI_area35"  # saída
os.makedirs(pasta_saida, exist_ok=True)  # cria pasta

img_bgr = cv2.imread(caminho_imagem, cv2.IMREAD_COLOR)  # lê imagem
if img_bgr is None:  # checa leitura
    raise FileNotFoundError(f"Não foi possível ler a imagem: {caminho_imagem}")  # erro

H, S, I = bgr_para_hsi_pixel_a_pixel(img_bgr)  # calcula HSI pixel a pixel

# (opcional) tenta salvar HSI float em TIFF (se o OpenCV não suportar, pode dar warning/fallback)
hsi_float = cv2.merge((H.astype(np.float32), S.astype(np.float32), I.astype(np.float32)))  # junta float
cv2.imwrite(os.path.join(pasta_saida, "imagem_HSI_float.tiff"), hsi_float)  # salva (pode cair pra 8U dependendo do build)

H_8bit = (H / 360.0 * 255.0).astype(np.uint8)  # H 0..360 -> 0..255
S_8bit = (S * 255.0).astype(np.uint8)  # S 0..1 -> 0..255
I_8bit = (I * 255.0).astype(np.uint8)  # I 0..1 -> 0..255

caminho_H = os.path.join(pasta_saida, "canal_H.png")  # saída H
caminho_S = os.path.join(pasta_saida, "canal_S.png")  # saída S
caminho_I = os.path.join(pasta_saida, "canal_I.png")  # saída I

cv2.imwrite(caminho_H, H_8bit)  # salva H
cv2.imwrite(caminho_S, S_8bit)  # salva S
cv2.imwrite(caminho_I, I_8bit)  # salva I

# junta em um PNG 3-canais (dados H,S,I em 8-bit, NÃO é “imagem colorida”)
hsi_8bit = cv2.merge((H_8bit, S_8bit, I_8bit))  # merge
cv2.imwrite(os.path.join(pasta_saida, "imagem_HSI_8bit.png"), hsi_8bit)  # salva

print("d.4 concluído (area35): canais HSI salvos.")
print(f"- {caminho_H}\n- {caminho_S}\n- {caminho_I}")

# ler os arquivos salvos e plotar lado a lado (igual você pediu)
H_lido = cv2.imread(caminho_H, cv2.IMREAD_GRAYSCALE)  # lê H salvo
S_lido = cv2.imread(caminho_S, cv2.IMREAD_GRAYSCALE)  # lê S salvo
I_lido = cv2.imread(caminho_I, cv2.IMREAD_GRAYSCALE)  # lê I salvo

plt.figure(figsize=(12, 4))  # figura

plt.subplot(1, 3, 1)  # H
plt.imshow(H_lido, cmap="gray")  # mostra H salvo
plt.title("H")  # título
plt.axis("off")  # sem eixo

plt.subplot(1, 3, 2)  # S
plt.imshow(S_lido, cmap="gray")  # mostra S salvo
plt.title("S")  # título
plt.axis("off")  # sem eixo

plt.subplot(1, 3, 3)  # I
plt.imshow(I_lido, cmap="gray")  # mostra I salvo
plt.title("I")  # título
plt.axis("off")  # sem eixo

plt.tight_layout()  # ajusta
plt.show()  # exibe
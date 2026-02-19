import os  # pastas e caminhos
import cv2  # ler e salvar
import numpy as np  # contas
import matplotlib.pyplot as plt  # plot

pasta_rgb = "canaisRGB_area35"  # origem dos canais RGB
pasta_saida = "canaisYUV_area35"  # saída YUV
os.makedirs(pasta_saida, exist_ok=True)  # cria pasta

R = cv2.imread(os.path.join(pasta_rgb, "canal_R.png"), cv2.IMREAD_GRAYSCALE)  # lê R
G = cv2.imread(os.path.join(pasta_rgb, "canal_G.png"), cv2.IMREAD_GRAYSCALE)  # lê G
B = cv2.imread(os.path.join(pasta_rgb, "canal_B.png"), cv2.IMREAD_GRAYSCALE)  # lê B

if R is None or G is None or B is None:  # checa leitura
    raise FileNotFoundError("Não foi possível carregar canal_R.png, canal_G.png ou canal_B.png em canaisRGB_area35.")  # erro

R = R.astype(np.float32)  # float para não truncar
G = G.astype(np.float32)  # float para não truncar
B = B.astype(np.float32)  # float para não truncar

# BT.601 (YUV)
Y = 0.299 * R + 0.587 * G + 0.114 * B  # luminância
U = -0.14713 * R - 0.28886 * G + 0.436 * B  # crominância azul (pode ser negativa)
V = 0.615 * R - 0.51499 * G - 0.10001 * B  # crominância vermelha (pode ser negativa)

U_digital = U + 128.0  # desloca para caber em 0..255
V_digital = V + 128.0  # desloca para caber em 0..255

Y_8bit = np.clip(Y, 0, 255).astype(np.uint8)  # Y em 8-bit
U_8bit = np.clip(U_digital, 0, 255).astype(np.uint8)  # U em 8-bit
V_8bit = np.clip(V_digital, 0, 255).astype(np.uint8)  # V em 8-bit

# Montar a imagem YUV 3 canais (Y,U,V)
imagem_yuv = cv2.merge((Y_8bit, U_8bit, V_8bit))  # merge YUV

cv2.imwrite(os.path.join(pasta_saida, "canal_Y.png"), Y_8bit)  # salva canal Y
cv2.imwrite(os.path.join(pasta_saida, "canal_U.png"), U_8bit)  # salva canal U
cv2.imwrite(os.path.join(pasta_saida, "canal_V.png"), V_8bit)  # salva canal V
cv2.imwrite(os.path.join(pasta_saida, "imagem_YUV.png"), imagem_yuv)  # salva imagem YUV (dados)

print("d.5 concluído (area35): canais YUV e imagem YUV 3-canais salvos em canaisYUV_area35.")

plt.figure(figsize=(12, 4))  # figura

plt.subplot(1, 3, 1)  # Y
plt.imshow(Y_8bit, cmap="gray")  # mostra Y
plt.title("Y")  # título
plt.axis("off")  # sem eixo

plt.subplot(1, 3, 2)  # U
plt.imshow(U_8bit, cmap="gray")  # mostra U
plt.title("U (+128)")  # título
plt.axis("off")  # sem eixo

plt.subplot(1, 3, 3)  # V
plt.imshow(V_8bit, cmap="gray")  # mostra V
plt.title("V (+128)")  # título
plt.axis("off")  # sem eixo

plt.tight_layout()  # ajusta
plt.show()  # exibe
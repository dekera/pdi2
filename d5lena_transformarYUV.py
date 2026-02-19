import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# d.5) RGB (canais separados) -> YUV (canais + imagem 3-canais)

pasta_rgb = "canaisRGB_lena"
pasta_saida = "canaisYUV_lena"
os.makedirs(pasta_saida, exist_ok=True)

# 1) Ler canais R, G, B salvos (1 canal cada)
R = cv2.imread(os.path.join(pasta_rgb, "canal_R.png"), cv2.IMREAD_GRAYSCALE)
G = cv2.imread(os.path.join(pasta_rgb, "canal_G.png"), cv2.IMREAD_GRAYSCALE)
B = cv2.imread(os.path.join(pasta_rgb, "canal_B.png"), cv2.IMREAD_GRAYSCALE)

if R is None or G is None or B is None:
    raise FileNotFoundError("Não foi possível carregar canal_R.png, canal_G.png ou canal_B.png.")

# 2) Converter para float para não truncar as contas
R = R.astype(np.float32)
G = G.astype(np.float32)
B = B.astype(np.float32)

# 3) Transformação RGB -> YUV (BT.601)
Y = 0.299 * R + 0.587 * G + 0.114 * B
U = -0.14713 * R - 0.28886 * G + 0.436 * B
V = 0.615 * R - 0.51499 * G - 0.10001 * B

# 4) Ajuste "digital" para salvar (U e V centrados em 128)
U_digital = U + 128.0
V_digital = V + 128.0

# 5) Clip + uint8 para salvar como PNG (0..255)
Y_8bit = np.clip(Y, 0, 255).astype(np.uint8)
U_8bit = np.clip(U_digital, 0, 255).astype(np.uint8)
V_8bit = np.clip(V_digital, 0, 255).astype(np.uint8)

# 6) Montar a "imagem YUV" (3 canais)
# Aqui está o que faltava: uma única matriz (H, W, 3) com (Y, U, V)
imagem_yuv = cv2.merge((Y_8bit, U_8bit, V_8bit))

# 7) Salvar canais e a imagem YUV
cv2.imwrite(os.path.join(pasta_saida, "canal_Y.png"), Y_8bit)
cv2.imwrite(os.path.join(pasta_saida, "canal_U.png"), U_8bit)
cv2.imwrite(os.path.join(pasta_saida, "canal_V.png"), V_8bit)

# Salva o “frame YUV” como PNG 3-canais (armazenamento, não visualização RGB)
cv2.imwrite(os.path.join(pasta_saida, "imagem_YUV.png"), imagem_yuv)

print("d.5 concluído: canais Y, U, V e imagem_YUV.png (3 canais) salvos em 'canaisYUV_lena'.")

# 8) Plotar os canais (visualmente úteis)
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(Y_8bit, cmap="gray")
plt.title("Y")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(U_8bit, cmap="gray")
plt.title("U (+ 128)")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(V_8bit, cmap="gray")
plt.title("V (+ 128)")
plt.axis("off")

plt.tight_layout()
plt.show()
import os  # criar pasta e caminhos
import cv2  # ler imagem e salvar
import numpy as np  # operações numéricas
import matplotlib.pyplot as plt  # plotar

caminho_imagem = "top_mosaic_09cm_area35.tif"  # entrada
pasta_saida = "canaisCMY_area35"  # saída
os.makedirs(pasta_saida, exist_ok=True)  # cria pasta

img_bgr = cv2.imread(caminho_imagem, cv2.IMREAD_COLOR)  # lê em BGR
if img_bgr is None:  # checa leitura
    raise FileNotFoundError(f"Não foi possível ler a imagem: {caminho_imagem}")  # erro

img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # converte para RGB
r, g, b = cv2.split(img_rgb)  # separa canais

c = 255 - r  # C = 255 - R
m = 255 - g  # M = 255 - G
y = 255 - b  # Y = 255 - B

plt.figure(figsize=(12, 4))  # figura

plt.subplot(1, 3, 1)  # posição 1
plt.imshow(c, cmap="gray")  # canal C
plt.title("Canal C (Ciano)")  # título
plt.axis("off")  # sem eixo

plt.subplot(1, 3, 2)  # posição 2
plt.imshow(m, cmap="gray")  # canal M
plt.title("Canal M (Magenta)")  # título
plt.axis("off")  # sem eixo

plt.subplot(1, 3, 3)  # posição 3
plt.imshow(y, cmap="gray")  # canal Y
plt.title("Canal Y (Amarelo)")  # título
plt.axis("off")  # sem eixo

plt.tight_layout()  # ajusta
plt.show()  # exibe

caminho_c = os.path.join(pasta_saida, "canal_C.png")  # saída C
caminho_m = os.path.join(pasta_saida, "canal_M.png")  # saída M
caminho_y = os.path.join(pasta_saida, "canal_Y.png")  # saída Y

cv2.imwrite(caminho_c, c.astype(np.uint8))  # salva C
cv2.imwrite(caminho_m, m.astype(np.uint8))  # salva M
cv2.imwrite(caminho_y, y.astype(np.uint8))  # salva Y

print("d.2 concluído (area35): canais CMY separados, plotados e salvos.")
print(f"- {caminho_c}\n- {caminho_m}\n- {caminho_y}")
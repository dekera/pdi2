import os  # criar pasta e montar caminhos
import cv2  # ler imagem, converter, separar canais e salvar
import numpy as np  # garantir tipos numéricos
import matplotlib.pyplot as plt  # plotar imagens

caminho_imagem = "top_mosaic_09cm_area35.tif"  # arquivo TIF de entrada
pasta_saida = "canaisRGB_area35"  # pasta onde os canais RGB serão salvos
os.makedirs(pasta_saida, exist_ok=True)  # cria a pasta se não existir

img_bgr = cv2.imread(caminho_imagem, cv2.IMREAD_COLOR)  # lê a imagem (OpenCV lê em BGR)
if img_bgr is None:  # checa se carregou
    raise FileNotFoundError(f"Não foi possível ler a imagem: {caminho_imagem}")  # erro claro

img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # converte para RGB (padrão Matplotlib)
r, g, b = cv2.split(img_rgb)  # separa canais RGB (cada um vira matriz 2D)

plt.figure(figsize=(12, 4))  # cria figura

plt.subplot(1, 3, 1)  # posição 1
plt.imshow(r, cmap="gray")  # mostra canal R
plt.title("Canal R")  # título
plt.axis("off")  # remove eixos

plt.subplot(1, 3, 2)  # posição 2
plt.imshow(g, cmap="gray")  # mostra canal G
plt.title("Canal G")  # título
plt.axis("off")  # remove eixos

plt.subplot(1, 3, 3)  # posição 3
plt.imshow(b, cmap="gray")  # mostra canal B
plt.title("Canal B")  # título
plt.axis("off")  # remove eixos

plt.tight_layout()  # ajusta layout

# Histograma
plt.figure(figsize=(8, 5))  # cria nova figura para histograma

plt.hist(
    r.flatten(),  # transforma matriz 2D em vetor 1D
    bins=256,  # 256 níveis digitais
    range=(0, 255),  # intervalo completo 8 bits
    color="red",  # cor da curva
    alpha=0.5,  # transparência
    label="Canal R"  # legenda
)

plt.hist(
    g.flatten(),  # vetor 1D
    bins=256,
    range=(0, 255),
    color="green",
    alpha=0.5,
    label="Canal G"
)

plt.hist(
    b.flatten(),
    bins=256,
    range=(0, 255),
    color="blue",
    alpha=0.5,
    label="Canal B"
)

plt.title("Histograma dos Canais RGB - GeoTIFF")  # título
plt.xlabel("Nível Digital (0–255)")  # eixo X
plt.ylabel("Frequência")  # eixo Y
plt.legend()  # mostra legenda
plt.grid(alpha=0.3)  # grade leve

plt.tight_layout()  # ajusta layout
plt.show()  # exibe
caminho_r = os.path.join(pasta_saida, "canal_R.png")  # saída R
caminho_g = os.path.join(pasta_saida, "canal_G.png")  # saída G
caminho_b = os.path.join(pasta_saida, "canal_B.png")  # saída B

cv2.imwrite(caminho_r, r.astype(np.uint8))  # salva R
cv2.imwrite(caminho_g, g.astype(np.uint8))  # salva G
cv2.imwrite(caminho_b, b.astype(np.uint8))  # salva B

print("d.1 concluído (area35): canais RGB separados, plotados e salvos.")
print(f"- {caminho_r}\n- {caminho_g}\n- {caminho_b}")
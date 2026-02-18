import os  # caminhos e pastas
import cv2  # ler e salvar imagens
import numpy as np  # diferença pixel a pixel
import matplotlib.pyplot as plt  # plotar

caminho_original = "top_mosaic_09cm_area35.tif"  # original
pasta_canais = "canaisRGB_area35"  # onde estão canal_R, canal_G, canal_B
pasta_saida = "resultados"  # resultados (como você pediu)
os.makedirs(pasta_saida, exist_ok=True)  # cria pasta

img_bgr_original = cv2.imread(caminho_original, cv2.IMREAD_COLOR)  # lê original
if img_bgr_original is None:  # checa leitura
    raise FileNotFoundError(f"Não foi possível ler a imagem original: {caminho_original}")  # erro

img_rgb_original = cv2.cvtColor(img_bgr_original, cv2.COLOR_BGR2RGB)  # converte para RGB

caminho_r = os.path.join(pasta_canais, "canal_R.png")  # canal R salvo
caminho_g = os.path.join(pasta_canais, "canal_G.png")  # canal G salvo
caminho_b = os.path.join(pasta_canais, "canal_B.png")  # canal B salvo

r = cv2.imread(caminho_r, cv2.IMREAD_GRAYSCALE)  # lê R 2D
g = cv2.imread(caminho_g, cv2.IMREAD_GRAYSCALE)  # lê G 2D
b = cv2.imread(caminho_b, cv2.IMREAD_GRAYSCALE)  # lê B 2D

if r is None or g is None or b is None:  # checa leitura
    raise FileNotFoundError("Não foi possível ler um ou mais canais em 'canaisRGB_area35'.")  # erro

img_rgb_recomposta = cv2.merge((r, g, b))  # recompõe RGB

if img_rgb_recomposta.shape != img_rgb_original.shape:  # checa dimensão
    raise ValueError(f"Dimensões não batem: original={img_rgb_original.shape}, recomposta={img_rgb_recomposta.shape}")  # erro

diff_int = img_rgb_original.astype(np.int16) - img_rgb_recomposta.astype(np.int16)  # diferença assinada
diff_abs = np.abs(diff_int).astype(np.uint8)  # diferença absoluta

iguais = np.array_equal(img_rgb_original, img_rgb_recomposta)  # teste identidade
max_diff = int(np.max(diff_abs))  # maior diferença
sum_diff = int(np.sum(diff_abs))  # soma das diferenças
pixels_diferentes = int(np.sum(np.any(diff_abs > 0, axis=2)))  # pixels com diferença em qualquer canal

print("=== COMPARAÇÃO (area35) ORIGINAL vs RECOMPOSTA ===")
print(f"Idênticas pixel a pixel? -> {iguais}")
print(f"Maior diferença absoluta (max) -> {max_diff}")
print(f"Soma total das diferenças -> {sum_diff}")
print(f"Número de pixels com alguma diferença -> {pixels_diferentes}")

plt.figure(figsize=(15, 5))  # figura

plt.subplot(1, 3, 1)  # original
plt.imshow(img_rgb_original)  # mostra original
plt.title("Original (RGB)")  # título
plt.axis("off")  # sem eixos

plt.subplot(1, 3, 2)  # recomposta
plt.imshow(img_rgb_recomposta)  # mostra recomposta
plt.title("Recomposta (RGB)")  # título
plt.axis("off")  # sem eixos

plt.subplot(1, 3, 3)  # diferença
plt.imshow(diff_abs)  # mostra diferença (RGB)
plt.title("Diferença |Original - Recomposta|")  # título
plt.axis("off")  # sem eixos

plt.tight_layout()  # ajusta
plt.show()  # exibe

caminho_diff = os.path.join(pasta_saida, "area35_diferenca_original_vs_recomposta.png")  # nome da saída
cv2.imwrite(caminho_diff, cv2.cvtColor(diff_abs, cv2.COLOR_RGB2BGR))  # salva diferença

print(f"Imagem de diferença salva em: {caminho_diff}")
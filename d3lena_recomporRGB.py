import os  # criar pastas e montar caminhos
import cv2  # ler imagens e fazer conversões
import numpy as np  # cálculos pixel a pixel
import matplotlib.pyplot as plt  # plotar lado a lado


# d.3) Comparar imagem original vs imagem recomposta
# - Lê a imagem original (lena-Color.png)
# - Lê os canais R, G, B salvos em canaisRGB_lena
# - Recompõe a imagem RGB
# - Mostra original e recomposta lado a lado
# - Calcula diferença pixel a pixel e prova se é idêntica
# - Salva a imagem diferença em resultados

# 1) Caminhos de entrada e saída
caminho_original = "lena-Color.png"             # imagem original
pasta_canais = "canaisRGB_lena"                # onde estão canal_R.png, canal_G.png, canal_B.png
pasta_saida = "resultados"                 # onde vamos salvar resultados
os.makedirs(pasta_saida, exist_ok=True)        # cria a pasta de saída se não existir

# 2) Ler a imagem original
img_bgr_original = cv2.imread(caminho_original)  # OpenCV lê em BGR
if img_bgr_original is None:
    raise FileNotFoundError(f"Não foi possível ler a imagem original: {caminho_original}")

# 3) Converter original para RGB (para comparação e plot no matplotlib)
img_rgb_original = cv2.cvtColor(img_bgr_original, cv2.COLOR_BGR2RGB)  # agora está em RGB

# 4) Ler os canais salvos (em escala de cinza)
caminho_r = os.path.join(pasta_canais, "canal_R.png")  # caminho do canal R
caminho_g = os.path.join(pasta_canais, "canal_G.png")  # caminho do canal G
caminho_b = os.path.join(pasta_canais, "canal_B.png")  # caminho do canal B

r = cv2.imread(caminho_r, cv2.IMREAD_GRAYSCALE)  # lê como 2D (0-255)
g = cv2.imread(caminho_g, cv2.IMREAD_GRAYSCALE)
b = cv2.imread(caminho_b, cv2.IMREAD_GRAYSCALE)

if r is None or g is None or b is None:
    raise FileNotFoundError("Não foi possível ler um ou mais canais em 'canaisRGB_lena'.")

# 5) Recompôr a imagem RGB a partir dos canais
img_rgb_recomposta = cv2.merge((r, g, b))  # junta em (R,G,B) -> imagem 3 canais

# 6) Verificar se as dimensões batem
if img_rgb_recomposta.shape != img_rgb_original.shape:
    raise ValueError(
        f"As dimensões não batem!\n"
        f"Original: {img_rgb_original.shape}\n"
        f"Recomposta: {img_rgb_recomposta.shape}"
    )

# 7) Calcular diferença pixel a pixel
# Convertendo para int16 evita problema de underflow (ex: 0 - 255 em uint8 vira número grande).
diff_int = img_rgb_original.astype(np.int16) - img_rgb_recomposta.astype(np.int16)  # diferença assinada
diff_abs = np.abs(diff_int).astype(np.uint8)  # diferença absoluta em 8-bit

# 8) Métricas para "provar" identidade
max_diff = int(np.max(diff_abs))                # maior diferença encontrada (0 se idêntico)
sum_diff = int(np.sum(diff_abs))                # soma de todas as diferenças (0 se idêntico)
iguais = np.array_equal(img_rgb_original, img_rgb_recomposta)  # True se idêntico pixel a pixel

# 9) Imprimir relatório numérico
print("=== COMPARAÇÃO ORIGINAL vs RECOMPOSTA ===")
print(f"Idênticas pixel a pixel? -> {iguais}")
print(f"Maior diferença absoluta (max) -> {max_diff}")
print(f"Soma total das diferenças -> {sum_diff}")

# Se não forem idênticas, mostrar quantos pixels diferem (em qualquer canal)
# Um pixel é considerado diferente se pelo menos 1 canal (R ou G ou B) tiver diferença > 0
pixels_diferentes = int(np.sum(np.any(diff_abs > 0, axis=2)))
print(f"Número de pixels com alguma diferença -> {pixels_diferentes}")

# 10) Plotar lado a lado (original, recomposta, diferença)
plt.figure(figsize=(15, 6))

plt.subplot(1, 3, 1)
plt.imshow(img_rgb_original)
plt.title("Original (RGB)")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(img_rgb_recomposta)
plt.title("Recomposta (RGB)")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(diff_abs)  # mostra diferença por canal (RGB)
plt.title("Diferença |Original - Recomposta|")
plt.axis("off")

plt.tight_layout()
plt.show()

# 11) Salvar a imagem de diferença
# Para salvar com OpenCV, convertemos RGB -> BGR
caminho_diff = os.path.join(pasta_saida, "diferenca_original_vs_recomposta.png")
cv2.imwrite(caminho_diff, cv2.cvtColor(diff_abs, cv2.COLOR_RGB2BGR))

print(f"Imagem de diferença salva em: {caminho_diff}")

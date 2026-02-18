import os  # manipulação de pastas
import cv2  # leitura e salvamento de imagem
import numpy as np  # operações numéricas
import matplotlib.pyplot as plt  # visualização


# =========================
# d.2) Separar a imagem nos canais CMY
# =========================

# -------- 1) Caminhos --------
caminho_imagem = "lena-Color.png"  # ajuste se necessário
pasta_saida = "canaisCMY_lena"

# -------- 2) Criar pasta se não existir --------
os.makedirs(pasta_saida, exist_ok=True)

# -------- 3) Ler imagem --------
img_bgr = cv2.imread(caminho_imagem)

if img_bgr is None:
    raise FileNotFoundError(f"Não foi possível ler a imagem: {caminho_imagem}")

# -------- 4) Converter para RGB --------
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# -------- 5) Separar canais RGB --------
r, g, b = cv2.split(img_rgb)

# -------- 6) Converter para CMY --------
# Fórmula do modelo CMY:
# C = 255 - R
# M = 255 - G
# Y = 255 - B

c = 255 - r
m = 255 - g
y = 255 - b

# -------- 7) Plotar canais CMY --------
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(c, cmap="gray")
plt.title("Canal C (Ciano)")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(m, cmap="gray")
plt.title("Canal M (Magenta)")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(y, cmap="gray")
plt.title("Canal Y (Amarelo)")
plt.axis("off")

plt.tight_layout()
plt.show()

# -------- 8) Salvar canais --------
c_saida = c.astype(np.uint8)
m_saida = m.astype(np.uint8)
y_saida = y.astype(np.uint8)

caminho_c = os.path.join(pasta_saida, "canal_C.png")
caminho_m = os.path.join(pasta_saida, "canal_M.png")
caminho_y = os.path.join(pasta_saida, "canal_Y.png")

cv2.imwrite(caminho_c, c_saida)
cv2.imwrite(caminho_m, m_saida)
cv2.imwrite(caminho_y, y_saida)

# -------- 9) Confirmação --------
print("d.2 concluído: canais CMY separados, plotados e salvos em 'resultados'.")
print(f"Arquivos gerados:\n- {caminho_c}\n- {caminho_m}\n- {caminho_y}")
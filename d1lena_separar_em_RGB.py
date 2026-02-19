import os  # importa funções do sistema operacional (criar pasta, montar caminhos)
import cv2  # importa OpenCV (ler imagem, separar canais, salvar imagens)
import numpy as np  # importa NumPy (manipulação numérica, não é obrigatório aqui mas é comum em PDI)
import matplotlib.pyplot as plt  # importa Matplotlib (plotar/exibir imagens)

# d.1) Separar a imagem nos canais RGB
# - Ler a imagem
# - Converter BGR -> RGB (porque OpenCV lê em BGR)
# - Separar canais R, G, B
# - Plotar os 3 canais
# - Salvar os 3 canais em uma pasta "resultados"

# 1) Definir caminhos
caminho_imagem = "lena-Color.png"  # caminho do arquivo de entrada (ajuste se estiver em outra pasta)
pasta_saida = "canaisRGB_lena"     # nome da pasta onde os canais serão salvos

# 2) Criar a pasta de saída (se não existir)
os.makedirs(pasta_saida, exist_ok=True)  # cria a pasta; se já existir, não dá erro

# 3) Ler a imagem com OpenCV
img_bgr = cv2.imread(caminho_imagem)  # lê a imagem (OpenCV lê em BGR)

# 4) Verificar se a imagem foi carregada
if img_bgr is None:  # se não encontrou o arquivo ou deu erro de leitura
    raise FileNotFoundError(f"Não foi possível ler a imagem: {caminho_imagem}")  # para o programa com erro claro

# 5) Converter BGR -> RGB para interpretação correta
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # converte para RGB (padrão do Matplotlib)

# 6) Separar canais R, G, B
r, g, b = cv2.split(img_rgb)  # separa em 3 matrizes 2D (cada uma = um canal)

# 7) Plotar os canais separados
plt.figure(figsize=(12, 5))  # cria uma figura com tamanho adequado

plt.subplot(1, 3, 1)         # 1 linha, 3 colunas, posição 1
plt.imshow(r, cmap="gray")   # mostra o canal R como imagem em tons de cinza
plt.title("Canal R")         # título do subplot
plt.axis("off")              # remove eixos

plt.subplot(1, 3, 2)         # posição 2
plt.imshow(g, cmap="gray")   # mostra canal G
plt.title("Canal G")
plt.axis("off")

plt.subplot(1, 3, 3)         # posição 3
plt.imshow(b, cmap="gray")   # mostra canal B
plt.title("Canal B")
plt.axis("off")

plt.tight_layout()           # ajusta espaçamentos automaticamente
plt.show()                   # exibe a figura na tela

# 8) Salvar os canais separados em arquivos
# Obs: para salvar corretamente, usamos PNG (8-bit), então garantimos dtype uint8

r_saida = r.astype(np.uint8)  # garante tipo 8-bit
g_saida = g.astype(np.uint8)  # garante tipo 8-bit
b_saida = b.astype(np.uint8)  # garante tipo 8-bit

# Montar caminhos completos dos arquivos de saída
caminho_r = os.path.join(pasta_saida, "canal_R.png")  # arquivo do canal R
caminho_g = os.path.join(pasta_saida, "canal_G.png")  # arquivo do canal G
caminho_b = os.path.join(pasta_saida, "canal_B.png")  # arquivo do canal B

# Salvar cada canal como uma imagem em escala de cinza
cv2.imwrite(caminho_r, r_saida)  # salva canal R
cv2.imwrite(caminho_g, g_saida)  # salva canal G
cv2.imwrite(caminho_b, b_saida)  # salva canal B

# 9) Mensagem final
print("d.1 concluído: canais RGB separados, plotados e salvos em 'resultados'.")  # confirma execução
print(f"Arquivos gerados:\n- {caminho_r}\n- {caminho_g}\n- {caminho_b}")  # lista os arquivos salvos
# Processamento Digital de Imagens II

## Trabalho 01 – Modelos de Sistemas de Cores

---

## 1. Descrição do Projeto

Este repositório contém a implementação do Trabalho 01 da disciplina de Processamento Digital de Imagens II.

O objetivo do trabalho é realizar a manipulação e conversão de imagens digitais entre diferentes modelos de cores, incluindo:

* RGB
* CMY
* HSI
* YUV

Foram utilizadas duas imagens base:

* lena-Color.png
* top_mosaic_09cm_area35.tif (GeoTIFF com resolução espacial de 9 cm)

Todas as operações foram implementadas em Python.

---

## 2. Estrutura do Repositório

### 2.1 Separação em Canais RGB

* d1lena_separar_em_RGB.py
* d1area35_separar_em_RGB.py
* canaisRGB_lena/
* canaisRGB_area35/

Realiza a decomposição da imagem nos três canais fundamentais:

* R (Red)
* G (Green)
* B (Blue)

---

### 2.2 Conversão para CMY

* d2lena_separar_em_CMY.py
* d2area35_separar_em_CMY.py
* canaisCMY_lena/
* canaisCMY_area35/

A conversão é realizada a partir da relação:

C = 255 − R
M = 255 − G
Y = 255 − B

---

### 2.3 Recomposição da Imagem RGB

* d3lena_recomporRGB.py
* d3area35_recomporRGB.py

Reconstrói a imagem colorida a partir dos canais R, G e B previamente separados.

---

### 2.4 Conversão para HSI

* d4lena_transformarHSI.py
* d4area35_transformarHSI.py
* canaisHSI_lena/
* canaisHSI_area35/

Conversão do modelo RGB para HSI utilizando:

* H (Hue) – Matiz
* S (Saturation) – Saturação
* I (Intensity) – Intensidade

---

### 2.5 Conversão para YUV

* d5lena_transformarYUV.py
* d5area35_transformarYUV.py
* canaisYUV_lena/
* canaisYUV_area35/

Conversão do modelo RGB para YUV, separando:

* Y – Luminância
* U – Crominância azul
* V – Crominância vermelha

A luminância representa a informação de brilho da imagem, enquanto U e V armazenam informação de cor.

---

### 2.6 Pasta de Resultados

* resultados/

Contém as imagens geradas durante o processamento, incluindo comparações e visualizações dos modelos convertidos.

---

## 3. Bibliotecas Utilizadas

O projeto foi desenvolvido em Python utilizando principalmente:

* OpenCV (cv2)
* NumPy
* Matplotlib
* Math

Ambiente virtual gerenciado com Pixi.

---

## 4. Objetivos Técnicos

* Manipular imagens digitais de 8 bits sem sinal (0–255).
* Implementar conversões entre sistemas de cores manualmente.
* Entender a separação entre luminância e crominância.
* Comparar diferenças visuais entre modelos de cor.
* Aplicar os métodos tanto em imagem padrão (Lena) quanto em imagem GeoTIFF real.

---

## 5. Observações

A imagem top_mosaic_09cm_area35.tif é um raster RGB com 8 bits por banda, contendo três bandas espectrais.

O projeto demonstra tanto a manipulação de imagens convencionais quanto de dados raster geoespaciais.

---

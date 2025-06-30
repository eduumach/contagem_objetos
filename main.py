import cv2
import numpy as np

# 1. Carregar a imagem
img = cv2.imread('images/chocolates.jpg')
h, w = img.shape[:2]

# 2. Converter para HSV e criar máscara para remover fundo branco
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask_white = cv2.inRange(hsv, (0, 0, 200), (180, 40, 255))
mask_obj = cv2.bitwise_not(mask_white)

# 3. Suavizar para ajudar na segmentação
mask_obj = cv2.GaussianBlur(mask_obj, (5, 5), 0)

# 4. Morfologia: abrir e depois fechar
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
mask_clean = cv2.morphologyEx(mask_obj, cv2.MORPH_OPEN, kernel)
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)

# 5. Detectar contornos
contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 6. Desenhar contornos e filtrar por área
contagem = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    if 300 < area < 0.2 * h * w:  # Ajuste o valor mínimo conforme necessário
        contagem += 1
        cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)


print(f'Objetos detectados: {contagem}')

# 6. Adicionar texto com a contagem na imagem
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.5
font_thickness = 3
text = f'Objetos detectados: {contagem}'
text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

# Posicionar o texto no canto superior esquerdo
text_x = 10
text_y = text_size[1] + 30

# Desenhar retângulo de fundo para o texto
cv2.rectangle(img, (text_x - 10, text_y - text_size[1] - 10), 
              (text_x + text_size[0] + 10, text_y + 10), (0, 0, 0), -1)

# Desenhar o texto
cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

# 7. Salvar a imagem da máscara
cv2.imwrite('output/mask.png', mask_clean)
cv2.imwrite('output/img.png', img)

# 8. Exibir imagem
cv2.imshow("Morph", mask_clean)
cv2.imshow("IMG", img)
cv2.waitKey(0)  # Espera até apertar alguma tecla
cv2.destroyAllWindows()  # Fecha todas as janelas abertas

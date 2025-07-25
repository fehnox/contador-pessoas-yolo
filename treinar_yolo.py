# ========================================
# SCRIPT DE TREINAMENTO DO MODELO YOLO
# ========================================
# Este script treina um modelo YOLO personalizado para detectar pessoas
# usando o dataset de imagens anotadas que você preparou

# Importa a biblioteca YOLO da Ultralytics
from ultralytics import YOLO

# ========================================
# CONFIGURAÇÃO E CARREGAMENTO DO MODELO
# ========================================

# Cria o modelo baseado em YOLOv8 nano (versão mais leve e rápida)
# Opções de modelo:
# - yolov8n.pt = nano (mais rápido, menos preciso)
# - yolov8s.pt = small (balanceado)  
# - yolov8m.pt = medium (mais preciso, mais lento)
# - yolov8l.pt = large (muito preciso, muito lento)
# - yolov8x.pt = extra large (máxima precisão, muito lento)
model = YOLO("yolov8n.pt")

# ========================================
# TREINAMENTO DO MODELO
# ========================================

# Executa o treinamento com os parâmetros definidos
model.train(
    data="data.yaml",    # Arquivo que define onde estão as imagens e labels
    epochs=50,           # Número de épocas (ciclos completos de treinamento)
                        # Mais épocas = melhor aprendizado, mas demora mais
    imgsz=640,          # Tamanho da imagem para treinamento (640x640 pixels)
                        # Imagens maiores = mais precisão, mas mais lento
    batch=8             # Número de imagens processadas simultaneamente
                        # Batch maior = treinamento mais rápido, mas usa mais memória
)

# ========================================
# O QUE ACONTECE DURANTE O TREINAMENTO:
# ========================================
"""
1. O modelo carrega as imagens de treino da pasta 'train/images'
2. Lê as anotações (bounding boxes) da pasta 'train/labels'  
3. Aprende a detectar pessoas baseado nos exemplos
4. Valida o aprendizado com imagens da pasta 'valid/images'
5. Salva os melhores pesos em 'runs/detect/train/weights/best.pt'
6. Salva os últimos pesos em 'runs/detect/train/weights/last.pt'

ARQUIVOS GERADOS:
- best.pt: Melhor modelo (menor erro de validação)
- last.pt: Último modelo (final do treinamento)
- results.csv: Métricas de treinamento
- confusion_matrix.png: Matriz de confusão
- results.png: Gráficos de progresso
"""

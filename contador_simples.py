# ========================================
# CONTADOR SIMPLES DE PESSOAS - VERSÃO BÁSICA
# ========================================
# Este é um contador mais simples, ideal para:
# - Testes rápidos do modelo
# - Contagem básica sem rastreamento
# - Verificar se o sistema está funcionando
# - Usar com câmera em tempo real

import cv2  # OpenCV para captura de câmera e processamento de imagem
from ultralytics import YOLO  # YOLOv8 para detecção de pessoas
import os   # Para verificar arquivos

def contador_simples():
    """
    Versão simplificada do contador de pessoas para testes rápidos.
    
    Características:
    - Usa apenas câmera (sem suporte a vídeo)
    - Não faz rastreamento individual
    - Conta apenas pessoas visíveis no momento
    - Interface mais simples
    - Ideal para testes e demonstrações
    
    Como funciona:
    1. Tenta usar modelo treinado, senão usa pré-treinado
    2. Abre a câmera do computador
    3. Detecta pessoas em tempo real
    4. Mostra contagem atual na tela
    5. Não rastreia entradas/saídas
    """
    
    # ========================================
    # ETAPA 1: ESCOLHA DO MODELO
    # ========================================
    
    # Tenta usar o modelo treinado primeiro
    modelo_path = "runs/detect/train/weights/best.pt"
    
    if not os.path.exists(modelo_path):
        print("⚠️ Usando modelo pré-treinado (yolov8n.pt)")
        modelo_path = "yolov8n.pt"
    else:
        print("✅ Usando modelo treinado!")
    
    # ========================================
    # ETAPA 2: CARREGA O MODELO YOLO
    # ========================================
    model = YOLO(modelo_path)
    
    # ========================================
    # ETAPA 3: ABRE A CÂMERA
    # ========================================
    # 0 = câmera padrão (geralmente webcam integrada)
    # 1 = segunda câmera, etc.
    cap = cv2.VideoCapture(0)
    
    # Variáveis de controle
    pessoas_detectadas = 0  # Número atual de pessoas na tela
    frame_count = 0         # Contador de frames para otimização
    
    print("📹 Câmera aberta! Pressione 'q' para sair")
    
    # ========================================
    # ETAPA 4: LOOP PRINCIPAL - CAPTURA E PROCESSAMENTO
    # ========================================
    while True:
        # Captura frame atual da câmera
        ret, frame = cap.read()
        if not ret:  # Se não conseguiu capturar
            break
        
        frame_count += 1
        
        # OTIMIZAÇÃO: Faz detecção apenas a cada 5 frames
        # Isso melhora a performance sem perder muito da precisão
        if frame_count % 5 == 0:
            # Executa detecção YOLO no frame atual
            results = model(frame, verbose=False)  # verbose=False evita prints
            
            # Conta pessoas detectadas neste frame
            pessoas_no_frame = 0
            
            # Verifica se há detecções
            if results[0].boxes is not None:
                # Processa cada detecção
                for box in results[0].boxes:
                    # Obtém coordenadas da caixa delimitadora
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                    # Obtém nível de confiança da detecção
                    conf = box.conf[0].float()
                    
                    # SÓ CONTA SE A CONFIANÇA FOR ALTA (maior que 50%)
                    if conf > 0.5:
                        pessoas_no_frame += 1
                        
                        # DESENHA CAIXA VERDE ao redor da pessoa
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        # ADICIONA TEXTO com nível de confiança
                        cv2.putText(frame, f'Pessoa ({conf:.2f})', 
                                   (x1, y1-10),  # Posição acima da caixa
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Atualiza contador global
            pessoas_detectadas = pessoas_no_frame
        
        # ========================================
        # ETAPA 5: INTERFACE VISUAL - PAINEL DE INFORMAÇÕES (MAIOR)
        # ========================================
        
        # PAINEL DE FUNDO (retângulo preto) - AUMENTADO
        cv2.rectangle(frame, (10, 10), (400, 120), (0, 0, 0), -1)  # Era 300x80, agora 400x120
        
        # TEXTO PRINCIPAL - Contador de pessoas (FONTE MAIOR)
        cv2.putText(frame, f"PESSOAS DETECTADAS: {pessoas_detectadas}", 
                   (25, 50),  # Posição do texto (era y=40, agora y=50)
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)  # Tamanho 0.9 (era 0.7), espessura 3
        
        # INSTRUÇÕES para o usuário (FONTE MAIOR)
        cv2.putText(frame, "Pressione 'q' para sair", 
                   (25, 85),  # Era y=65, agora y=85
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)  # Tamanho 0.6 (era 0.5)
        
        # ADICIONA INFORMAÇÕES EXTRAS
        cv2.putText(frame, f"Modelo: {os.path.basename(modelo_path)}", 
                   (25, 110),  # Nova linha com info do modelo
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # ========================================
        # ETAPA 6: MOSTRA O RESULTADO (JANELA MAIOR)
        # ========================================
        # Configura janela redimensionável e maior
        cv2.namedWindow('Contador Simples de Pessoas', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Contador Simples de Pessoas', 900, 650)  # Janela maior
        cv2.imshow('Contador Simples de Pessoas', frame)
        
        # Verifica se usuário pressionou 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # ========================================
    # ETAPA 7: LIMPEZA E FINALIZAÇÃO
    # ========================================
    cap.release()         # Libera a câmera
    cv2.destroyAllWindows()  # Fecha janelas do OpenCV
    print(f"🎯 Sessão finalizada!")

# ========================================
# EXECUÇÃO DO PROGRAMA
# ========================================
if __name__ == "__main__":
    """
    Ponto de entrada do programa simples.
    Executa quando o arquivo é rodado diretamente.
    """
    contador_simples()

# ========================================
# SCRIPT DE TESTE RÁPIDO DO CONTADOR
# ========================================
# Este script faz um teste básico do sistema de detecção
# sem o rastreamento completo, ideal para validar se o modelo está funcionando

import cv2  # OpenCV para processamento de vídeo
import os   # Para operações com arquivos e pastas
from ultralytics import YOLO  # YOLOv8 para detecção

def testar_contador_video():
    """
    Função principal de teste do contador de pessoas.
    
    Esta função:
    1. Procura modelos disponíveis (treinado ou pré-treinado)
    2. Procura vídeos no diretório atual
    3. Permite escolher um vídeo para teste
    4. Executa detecção básica sem rastreamento
    5. Mostra resultados em tempo real
    
    É uma versão simplificada para testes rápidos.
    """
    print("🎯 TESTE DO CONTADOR DE PESSOAS")
    print("=" * 50)
    
    # ========================================
    # ETAPA 1: VERIFICA MODELOS DISPONÍVEIS
    # ========================================
    modelo_treinado = "runs/detect/train/weights/best.pt"  # Seu modelo personalizado
    modelo_pretrained = "yolov8n.pt"  # Modelo genérico pré-treinado
    
    # Escolhe qual modelo usar baseado na disponibilidade
    if os.path.exists(modelo_treinado):
        modelo_path = modelo_treinado
        print(f"✅ Usando modelo treinado: {modelo_path}")
    elif os.path.exists(modelo_pretrained):
        modelo_path = modelo_pretrained
        print(f"⚠️ Usando modelo pré-treinado: {modelo_path}")
    else:
        print("❌ Nenhum modelo encontrado!")
        return
    
    # ========================================
    # ETAPA 2: PROCURA VÍDEOS NO DIRETÓRIO
    # ========================================
    print("\n📁 Procurando vídeos no diretório...")
    
    # Lista de extensões de vídeo suportadas
    extensoes_video = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    videos_encontrados = []
    
    # Varre todos os arquivos do diretório atual
    for arquivo in os.listdir('.'):
        # Verifica se o arquivo tem extensão de vídeo
        if any(arquivo.lower().endswith(ext) for ext in extensoes_video):
            videos_encontrados.append(arquivo)
    
    # ========================================
    # ETAPA 3: INTERFACE DE ESCOLHA DE VÍDEO
    # ========================================
    if videos_encontrados:
        print("🎬 Vídeos encontrados:")
        # Lista os vídeos numerados
        for i, video in enumerate(videos_encontrados, 1):
            print(f"  {i}. {video}")
        
        # Permite escolher por número ou digitar caminho completo
        escolha = input(f"\nEscolha um vídeo (1-{len(videos_encontrados)}) ou digite o caminho completo: ").strip()
        
        try:
            # Se digitou um número válido, usa o vídeo correspondente
            if escolha.isdigit() and 1 <= int(escolha) <= len(videos_encontrados):
                video_path = videos_encontrados[int(escolha) - 1]
            else:
                # Senão, assume que digitou um caminho completo
                video_path = escolha
        except:
            video_path = escolha
    else:
        # Se não encontrou vídeos, pede para digitar o caminho
        video_path = input("📂 Digite o caminho completo do vídeo: ").strip()
    
    # Remove aspas do caminho (caso o usuário tenha copiado com aspas)
    video_path = video_path.strip('"\'')
    
    # Verifica se o arquivo existe
    if not os.path.exists(video_path):
        print(f"❌ Vídeo não encontrado: {video_path}")
        return
    
    print(f"🎬 Testando com: {video_path}")
    
    # ========================================
    # ETAPA 4: CARREGA O MODELO YOLO
    # ========================================
    try:
        model = YOLO(modelo_path)
        print("✅ Modelo carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return
    
    # ========================================
    # ETAPA 5: ABRE E ANALISA O VÍDEO
    # ========================================
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("❌ Erro ao abrir o vídeo!")
        return
    
    # Obtém informações do vídeo
    fps = int(cap.get(cv2.CAP_PROP_FPS))              # Frames por segundo
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    # Largura em pixels
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Altura em pixels
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total de frames
    
    print(f"📊 Info do vídeo: {width}x{height}, {fps} FPS, {total_frames} frames")
    print("\n▶️ Iniciando teste... Pressione 'q' para sair")
    
    # ========================================
    # ETAPA 6: LOOP PRINCIPAL DE PROCESSAMENTO
    # ========================================
    pessoas_detectadas = 0  # Contador atual de pessoas no frame
    frame_count = 0         # Contador de frames processados
    
    while True:
        # Lê o próximo frame do vídeo
        ret, frame = cap.read()
        if not ret:  # Se não conseguiu ler (fim do vídeo)
            print("📹 Fim do vídeo!")
            break
        
        frame_count += 1
        
        # OTIMIZAÇÃO: Processa apenas a cada 3 frames para melhor performance
        if frame_count % 3 == 0:
            try:
                # Executa detecção YOLO no frame atual
                results = model(frame, verbose=False)  # verbose=False evita prints
                
                pessoas_no_frame = 0  # Contador de pessoas neste frame
                
                # Verifica se encontrou alguma detecção
                if results[0].boxes is not None:
                    # Processa cada detecção encontrada
                    for box in results[0].boxes:
                        conf = box.conf[0].float()  # Nível de confiança da detecção
                        
                        # Só conta se a confiança for alta (maior que 30%)
                        if conf > 0.3:
                            pessoas_no_frame += 1
                            
                            # DESENHA CAIXA DELIMITADORA ao redor da pessoa
                            x1, y1, x2, y2 = box.xyxy[0].int().tolist()  # Coordenadas da caixa
                            
                            # Desenha retângulo verde
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            
                            # Adiciona texto com nível de confiança
                            cv2.putText(frame, f'Pessoa ({conf:.2f})', 
                                       (x1, y1-10),  # Posição do texto
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Atualiza contador global
                pessoas_detectadas = pessoas_no_frame
                
            except Exception as e:
                print(f"⚠️ Erro no frame {frame_count}: {e}")
                continue
        
        # ========================================
        # ETAPA 7: ADICIONA INFORMAÇÕES NA TELA (PAINEL MAIOR)
        # ========================================
        
        # PAINEL DE INFORMAÇÕES (fundo escuro) - AUMENTADO
        cv2.rectangle(frame, (10, 10), (450, 130), (0, 0, 0), -1)  # Era 350x100, agora 450x130
        cv2.rectangle(frame, (10, 10), (450, 130), (255, 255, 255), 3)  # Contorno mais grosso
        
        # TEXTOS INFORMATIVOS (MAIORES)
        # Contador principal
        cv2.putText(frame, f"PESSOAS DETECTADAS: {pessoas_detectadas}", 
                   (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)  # Era 0.6, agora 0.8
        
        # Progresso do vídeo
        cv2.putText(frame, f"Frame: {frame_count}/{total_frames}", 
                   (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)  # Era 0.5, agora 0.6
        
        # Instruções
        cv2.putText(frame, "Pressione 'q' para sair", 
                   (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)  # Era 0.5, agora 0.6
        
        # Modelo sendo usado
        cv2.putText(frame, f"Modelo: {os.path.basename(modelo_path)}", 
                   (25, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # ========================================
        # ETAPA 8: REDIMENSIONA E MOSTRA O FRAME (JANELA MAIOR)
        # ========================================
        
        # Se o vídeo for muito pequeno, aumenta
        if width < 800:
            scale = 800 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        # Se o vídeo for muito grande, redimensiona para caber na tela
        elif width > 1400:  # Era 1200, agora 1400
            scale = 1400 / width  # Calcula fator de escala
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        
        # Mostra o frame processado com JANELA MAIOR
        cv2.namedWindow('TESTE - Contador de Pessoas', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('TESTE - Contador de Pessoas', 1100, 750)  # Janela inicial maior
        cv2.imshow('TESTE - Contador de Pessoas', frame)
        
        # Verifica se usuário pressionou 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # ========================================
    # ETAPA 9: FINALIZAÇÃO E LIMPEZA
    # ========================================
    cap.release()         # Libera o arquivo de vídeo
    cv2.destroyAllWindows()  # Fecha janelas do OpenCV
    
    # Mostra resultado final
    print("\n" + "="*50)
    print("✅ TESTE CONCLUÍDO!")
    print(f"📊 Último frame: {pessoas_detectadas} pessoas detectadas")
    print("="*50)

# ========================================
# EXECUÇÃO DO SCRIPT
# ========================================
if __name__ == "__main__":
    """
    Ponto de entrada do programa de teste.
    Executa a função principal quando o script é rodado diretamente.
    """
    testar_contador_video()

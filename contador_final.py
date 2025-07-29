#!/usr/bin/env python3
"""
CONTADOR + GRAVADOR SIMPLES - VERSÃO QUE FUNCIONA
"""
import cv2
from ultralytics import YOLO
import os
from datetime import datetime

def contador_com_gravacao_funcional():
    """Contador que funciona e grava automaticamente"""
    
    print("🎬 CONTADOR COM GRAVAÇÃO - VERSÃO FUNCIONAL")
    print("=" * 50)
    
    # Menu simples
    print("\n📋 OPÇÕES:")
    print("1. Processar vídeo e gravar")
    print("2. Usar câmera e gravar")
    
    opcao = input("\nEscolha (1 ou 2): ").strip()
    
    # Carrega modelo YOLO
    model = YOLO("yolov8n.pt")
    print("✅ Modelo YOLO carregado!")
    
    if opcao == "1":
        # VÍDEO
        video_path = input("Caminho do vídeo (ou ENTER para padrão): ").strip()
        if not video_path:
            video_path = "videos para treinamento/MVI_5049.mp4"
        
        if not os.path.exists(video_path):
            print(f"❌ Vídeo não encontrado: {video_path}")
            return
        
        cap = cv2.VideoCapture(video_path)
        fonte = "VIDEO"
        
    elif opcao == "2":
        # CÂMERA
        cap = cv2.VideoCapture(0)
        fonte = "CAMERA"
        
    else:
        print("❌ Opção inválida!")
        return
    
    if not cap.isOpened():
        print("❌ Erro ao abrir fonte!")
        return
    
    # Configuração da gravação
    fps = int(cap.get(cv2.CAP_PROP_FPS)) if opcao == "1" else 20
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Nome do arquivo de saída
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"contador_resultado_{timestamp}.mp4"
    
    # Configurar gravação
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    print(f"🎬 Gravando em: {output_file}")
    print(f"📊 {width}x{height} @ {fps}fps")
    print("🛑 Pressione 'q' para parar")
    
    pessoas_detectadas = 0
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Detecção YOLO (a cada frame para melhor estabilidade)
        results = model(frame, verbose=False)
        
        pessoas_no_frame = 0
        detections = []  # Lista para armazenar detecções
        
        if results[0].boxes is not None:
            for box in results[0].boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Classe 0 = pessoa, confiança > 0.4 (mais sensível)
                if cls == 0 and conf > 0.4:
                    pessoas_no_frame += 1
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                    detections.append((x1, y1, x2, y2, conf))
        
        pessoas_detectadas = pessoas_no_frame
        
        # Desenha todas as detecções com estilo melhorado
        for x1, y1, x2, y2, conf in detections:
            # Caixa azul principal (mais grossa)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 100, 0), 4)  # Azul forte
            
            # Caixa interna mais fina para dar profundidade
            cv2.rectangle(frame, (x1+2, y1+2), (x2-2, y2-2), (255, 150, 50), 2)  # Azul claro
            
            # Fundo do texto para melhor legibilidade
            text = f'PESSOA {conf:.2f}'
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            cv2.rectangle(frame, (x1, y1-35), (x1 + text_size[0] + 10, y1), (255, 100, 0), -1)
            
            # Texto em branco sobre fundo azul
            cv2.putText(frame, text, 
                       (x1 + 5, y1-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Interface visual melhorada
        cv2.rectangle(frame, (10, 10), (550, 200), (0, 0, 0), -1)  # Fundo preto
        cv2.rectangle(frame, (15, 15), (545, 195), (255, 100, 0), 3)  # Borda azul
        
        # Texto principal - PESSOAS (azul)
        cv2.putText(frame, f"PESSOAS DETECTADAS: {pessoas_detectadas}", 
                   (30, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 150, 50), 4)
        
        # Status da gravação (vermelho)
        cv2.putText(frame, "🔴 GRAVANDO EM TEMPO REAL", 
                   (30, 105),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
        
        # Fonte (branco)
        cv2.putText(frame, f"Fonte: {fonte} | Confianca: >40%", 
                   (30, 140),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Frame count e FPS (cinza claro)
        cv2.putText(frame, f"Frame: {frame_count} | FPS: {fps}", 
                   (30, 170),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
        
        # GRAVA O FRAME
        out.write(frame)
        
        # Mostra na tela
        cv2.namedWindow('CONTADOR + GRAVAÇÃO', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('CONTADOR + GRAVAÇÃO', 1000, 700)
        cv2.imshow('CONTADOR + GRAVAÇÃO', frame)
        
        # Controle de saída
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break
    
    # Finaliza
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"✅ CONCLUÍDO!")
    print(f"📁 Arquivo salvo: {os.path.abspath(output_file)}")
    print(f"🎯 Total de frames processados: {frame_count}")

if __name__ == "__main__":
    contador_com_gravacao_funcional()

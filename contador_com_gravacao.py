# ========================================
# CONTADOR DE PESSOAS COM GRAVAÇÃO
# ========================================
# Versão do contador que salva o vídeo processado

import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
import time
import os
from datetime import datetime

class ContadorComGravacao:
    """
    Contador de pessoas que salva o vídeo processado
    """
    
    def __init__(self, modelo_path="runs/detect/train/weights/best.pt"):
        """Inicializa o contador com gravação"""
        # Carrega modelo
        if os.path.exists(modelo_path):
            self.model = YOLO(modelo_path)
            print("✅ Usando modelo treinado!")
        else:
            self.model = YOLO("yolov8n.pt")
            print("⚠️ Usando modelo pré-treinado!")
        
        # Variáveis de controle
        self.track_history = defaultdict(lambda: [])
        self.pessoas_contadas = set()
        self.contador_entrada = 0
        self.contador_saida = 0
        self.linha_contagem_y = None
        
        # Variáveis para gravação
        self.video_writer = None
        self.gravando = False
        self.nome_arquivo_saida = None
    
    def definir_linha_contagem(self, frame):
        """Define linha de contagem no meio da tela"""
        height, width = frame.shape[:2]
        self.linha_contagem_y = height // 2
        return self.linha_contagem_y
    
    def desenhar_linha_contagem(self, frame):
        """Desenha linha de contagem"""
        if self.linha_contagem_y is not None:
            cv2.line(frame, (0, self.linha_contagem_y), 
                    (frame.shape[1], self.linha_contagem_y), (0, 255, 0), 3)
            cv2.putText(frame, "LINHA DE CONTAGEM", (10, self.linha_contagem_y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    def verificar_passagem(self, track_id, centro_y):
        """Verifica passagem pela linha"""
        if self.linha_contagem_y is None:
            return
        
        historico = self.track_history[track_id]
        
        if len(historico) >= 2:
            y_anterior = historico[-2][1]
            y_atual = centro_y
            
            # Entrada (cima para baixo)
            if y_anterior < self.linha_contagem_y and y_atual >= self.linha_contagem_y:
                if track_id not in self.pessoas_contadas:
                    self.contador_entrada += 1
                    self.pessoas_contadas.add(track_id)
                    print(f"🚶 Pessoa {track_id} ENTROU! Total: {self.contador_entrada}")
            
            # Saída (baixo para cima)
            elif y_anterior > self.linha_contagem_y and y_atual <= self.linha_contagem_y:
                if track_id not in self.pessoas_contadas:
                    self.contador_saida += 1
                    self.pessoas_contadas.add(track_id)
                    print(f"🚶 Pessoa {track_id} SAIU! Total: {self.contador_saida}")
    
    def adicionar_info_tela(self, frame):
        """Adiciona informações na tela com PAINEL MAIOR"""
        # Painel principal (MAIOR)
        cv2.rectangle(frame, (10, 10), (500, 160), (0, 0, 0), -1)  # Era 450x140, agora 500x160
        cv2.rectangle(frame, (10, 10), (500, 160), (255, 255, 255), 3)  # Borda mais grossa
        
        # Textos (MAIORES)
        cv2.putText(frame, f"CONTADOR DE PESSOAS", (25, 45),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)  # Era 0.7, agora 0.9
        cv2.putText(frame, f"Entradas: {self.contador_entrada}", (25, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  # Era 0.6, agora 0.7
        cv2.putText(frame, f"Saidas: {self.contador_saida}", (25, 105),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  # Era 0.6, agora 0.7
        cv2.putText(frame, f"Total: {self.contador_entrada - self.contador_saida}", (25, 135),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 3)  # Era 0.6, agora 0.7
        
        # Status da gravação (MAIOR)
        if self.gravando:
            cv2.putText(frame, "🔴 GRAVANDO", (280, 45),  # Posição ajustada
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)  # Maior e mais visível
    
    def processar_frame(self, frame):
        """Processa frame com detecção e rastreamento"""
        if self.linha_contagem_y is None:
            self.definir_linha_contagem(frame)
        
        # Detecção + tracking
        results = self.model.track(frame, persist=True, verbose=False)
        
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confidences = results[0].boxes.conf.float().cpu().tolist()
            
            for box, track_id, conf in zip(boxes, track_ids, confidences):
                x, y, w, h = box
                centro_x = int(x)
                centro_y = int(y)
                
                # Atualiza histórico
                self.track_history[track_id].append((centro_x, centro_y))
                if len(self.track_history[track_id]) > 30:
                    self.track_history[track_id].pop(0)
                
                # Verifica passagem
                self.verificar_passagem(track_id, centro_y)
                
                # Desenha bounding box
                x1 = int(x - w/2)
                y1 = int(y - h/2)
                x2 = int(x + w/2)
                y2 = int(y + h/2)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f'ID: {track_id} ({conf:.2f})', 
                           (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                # Desenha rastro
                pontos = np.array(self.track_history[track_id], dtype=np.int32)
                if len(pontos) > 1:
                    cv2.polylines(frame, [pontos], False, (0, 255, 255), 2)
        
        # Adiciona elementos visuais
        self.desenhar_linha_contagem(frame)
        self.adicionar_info_tela(frame)
        
        return frame
    
    def iniciar_gravacao(self, largura, altura, fps=30):
        """Inicia gravação do vídeo"""
        # Nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.nome_arquivo_saida = f"contador_gravado_{timestamp}.mp4"
        
        # Codec para MP4
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Cria VideoWriter
        self.video_writer = cv2.VideoWriter(
            self.nome_arquivo_saida, 
            fourcc, 
            fps, 
            (largura, altura)
        )
        
        self.gravando = True
        print(f"🎬 Iniciando gravação: {self.nome_arquivo_saida}")
    
    def gravar_frame(self, frame):
        """Grava um frame no vídeo"""
        if self.gravando and self.video_writer is not None:
            self.video_writer.write(frame)
    
    def parar_gravacao(self):
        """Para a gravação"""
        if self.gravando and self.video_writer is not None:
            self.video_writer.release()
            self.gravando = False
            print(f"✅ Gravação salva: {self.nome_arquivo_saida}")
            print(f"📁 Local: {os.path.abspath(self.nome_arquivo_saida)}")
    
    def contar_com_gravacao_video(self, video_path):
        """Conta pessoas em vídeo e salva resultado"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("❌ Erro ao abrir vídeo!")
            return
        
        # Propriedades do vídeo
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📹 Vídeo: {width}x{height}, {fps} FPS, {total_frames} frames")
        print("🎬 Pressione 'g' para iniciar/parar gravação")
        print("🚪 Pressione 'q' para sair")
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Processa frame
            frame_processado = self.processar_frame(frame)
            
            # Grava se estiver gravando
            if self.gravando:
                self.gravar_frame(frame_processado)
            
            # Adiciona contador de progresso
            progresso = f"Frame: {frame_count}/{total_frames}"
            cv2.putText(frame_processado, progresso, (width - 200, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Redimensiona se necessário (PERMITE JANELAS MAIORES)
            if width > 1500:  # Era 1200, agora 1500
                scale = 1500 / width
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame_processado = cv2.resize(frame_processado, (new_width, new_height))
            
            # JANELA MAIOR E REDIMENSIONÁVEL
            cv2.namedWindow('Contador com Gravação', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Contador com Gravação', 1200, 800)  # Janela inicial maior
            cv2.imshow('Contador com Gravação', frame_processado)
            
            # Controles de teclado
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('g'):
                if not self.gravando:
                    self.iniciar_gravacao(width, height, fps)
                else:
                    self.parar_gravacao()
        
        # Finaliza
        if self.gravando:
            self.parar_gravacao()
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Relatório final
        print("\n" + "="*50)
        print("📊 RESULTADOS FINAIS:")
        print(f"🚶‍♂️ Entradas: {self.contador_entrada}")
        print(f"🚶‍♀️ Saídas: {self.contador_saida}")
        print(f"👥 Total atual: {self.contador_entrada - self.contador_saida}")
        if hasattr(self, 'nome_arquivo_saida') and self.nome_arquivo_saida:
            print(f"🎬 Vídeo salvo: {self.nome_arquivo_saida}")
        print("="*50)
    
    def contar_com_gravacao_camera(self):
        """Conta pessoas na câmera e permite gravar"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Erro ao abrir câmera!")
            return
        
        # Propriedades da câmera
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = 30  # FPS padrão para gravação
        
        print(f"📹 Câmera: {width}x{height}")
        print("🎬 Pressione 'g' para iniciar/parar gravação")
        print("🚪 Pressione 'q' para sair")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Processa frame
            frame_processado = self.processar_frame(frame)
            
            # Grava se estiver gravando
            if self.gravando:
                self.gravar_frame(frame_processado)
            
            # JANELA MAIOR E REDIMENSIONÁVEL PARA CÂMERA
            cv2.namedWindow('Contador Câmera com Gravação', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Contador Câmera com Gravação', 1000, 700)
            cv2.imshow('Contador Câmera com Gravação', frame_processado)
            
            # Controles
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('g'):
                if not self.gravando:
                    self.iniciar_gravacao(width, height, fps)
                else:
                    self.parar_gravacao()
        
        # Finaliza
        if self.gravando:
            self.parar_gravacao()
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Relatório final
        print("\n" + "="*50)
        print("📊 RESULTADOS FINAIS:")
        print(f"🚶‍♂️ Entradas: {self.contador_entrada}")
        print(f"🚶‍♀️ Saídas: {self.contador_saida}")
        print(f"👥 Total atual: {self.contador_entrada - self.contador_saida}")
        if hasattr(self, 'nome_arquivo_saida') and self.nome_arquivo_saida:
            print(f"🎬 Vídeo salvo: {self.nome_arquivo_saida}")
        print("="*50)

def main():
    """Função principal"""
    print("🎬 CONTADOR DE PESSOAS COM GRAVAÇÃO")
    print("="*50)
    
    contador = ContadorComGravacao()
    
    print("\n🎯 ESCOLHA UMA OPÇÃO:")
    print("1. Processar vídeo e gravar resultado")
    print("2. Usar câmera e gravar")
    print("3. Sair")
    
    while True:
        opcao = input("\nEscolha (1-3): ").strip()
        
        if opcao == "1":
            video_path = input("Caminho do vídeo: ").strip().strip('"\'')
            if os.path.exists(video_path):
                contador.contar_com_gravacao_video(video_path)
            else:
                print("❌ Vídeo não encontrado!")
        
        elif opcao == "2":
            contador.contar_com_gravacao_camera()
        
        elif opcao == "3":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()

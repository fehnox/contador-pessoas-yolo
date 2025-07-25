# ========================================
# CONTADOR COM TAMANHO PERSONALIZÁVEL
# ========================================
# Versão que permite escolher o tamanho da interface

import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
import os
import threading
import time
from datetime import datetime

class ContadorPersonalizavel:
    """Contador com interface personalizável"""
    
    def __init__(self, modelo_path="runs/detect/train/weights/best.pt"):
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
        
        # Configurações de interface (personalizáveis)
        self.tamanho_painel = "medio"  # pequeno, medio, grande, gigante
        self.tamanho_janela = "medio"  # pequeno, medio, grande, fullscreen
        self.tamanho_fonte = "medio"   # pequeno, medio, grande
        
        # Configurações de gravação
        self.gravando = False
        self.video_writer = None
        self.nome_arquivo_gravacao = None
    
    def configurar_interface(self):
        """Permite ao usuário configurar o tamanho da interface"""
        print("\n🎨 CONFIGURAÇÃO DA INTERFACE")
        print("="*50)
        
        # Tamanho do painel
        print("📊 TAMANHO DO PAINEL DE INFORMAÇÕES:")
        print("1. Pequeno (300x100)")
        print("2. Médio (450x140)") 
        print("3. Grande (600x180)")
        print("4. Gigante (750x220)")
        
        opcao = input("Escolha (1-4): ").strip()
        if opcao == "1":
            self.tamanho_painel = "pequeno"
        elif opcao == "2": 
            self.tamanho_painel = "medio"
        elif opcao == "3":
            self.tamanho_painel = "grande"
        elif opcao == "4":
            self.tamanho_painel = "gigante"
        
        # Tamanho da janela
        print("\n🖼️ TAMANHO DA JANELA:")
        print("1. Pequena (1200x900)")
        print("2. Média (1600x1200)")
        print("3. Grande (1920x1080)")
        print("4. Tela Cheia")
        
        opcao = input("Escolha (1-4): ").strip()
        if opcao == "1":
            self.tamanho_janela = "pequeno"
        elif opcao == "2":
            self.tamanho_janela = "medio"
        elif opcao == "3":
            self.tamanho_janela = "grande"
        elif opcao == "4":
            self.tamanho_janela = "fullscreen"
        
        # Tamanho da fonte
        print("\n🔤 TAMANHO DA FONTE:")
        print("1. Pequena")
        print("2. Média")
        print("3. Grande")
        
        opcao = input("Escolha (1-3): ").strip()
        if opcao == "1":
            self.tamanho_fonte = "pequeno"
        elif opcao == "2":
            self.tamanho_fonte = "medio"
        elif opcao == "3":
            self.tamanho_fonte = "grande"
        
        print(f"\n✅ Configuração salva!")
        print(f"📊 Painel: {self.tamanho_painel}")
        print(f"🖼️ Janela: {self.tamanho_janela}")
        print(f"🔤 Fonte: {self.tamanho_fonte}")
        
        # Pergunta sobre gravação
        print(f"\n🎬 GRAVAÇÃO DE VÍDEO:")
        print("Deseja gravar o vídeo da sessão?")
        gravar = input("(s/n): ").strip().lower()
        
        if gravar in ['s', 'sim', 'y', 'yes']:
            self.configurar_gravacao = True
            print("✅ Gravação será ativada!")
        else:
            self.configurar_gravacao = False
            print("❌ Sem gravação")
    
    def iniciar_gravacao(self, frame_exemplo):
        """Inicia gravação de vídeo"""
        if not hasattr(self, 'configurar_gravacao') or not self.configurar_gravacao:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.nome_arquivo_gravacao = f"contador_personalizado_{timestamp}.mp4"
            
            # Configurações do vídeo
            height, width = frame_exemplo.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(
                self.nome_arquivo_gravacao, fourcc, 20.0, (width, height)
            )
            
            self.gravando = True
            print(f"🎬 Gravação iniciada: {self.nome_arquivo_gravacao}")
            
        except Exception as e:
            print(f"❌ Erro ao iniciar gravação: {e}")
            self.configurar_gravacao = False
    
    def gravar_frame(self, frame):
        """Grava um frame"""
        if self.gravando and self.video_writer:
            try:
                self.video_writer.write(frame)
            except Exception as e:
                print(f"❌ Erro ao gravar frame: {e}")
    
    def parar_gravacao(self):
        """Para a gravação"""
        if self.gravando and self.video_writer:
            self.gravando = False
            self.video_writer.release()
            print(f"✅ Gravação finalizada!")
            print(f"📁 Arquivo salvo: {os.path.abspath(self.nome_arquivo_gravacao)}")
    
    def get_config_painel(self):
        """Retorna configurações do painel baseado no tamanho escolhido"""
        configs = {
            "pequeno": {"largura": 300, "altura": 100, "x": 10, "y": 10},
            "medio": {"largura": 450, "altura": 140, "x": 10, "y": 10},
            "grande": {"largura": 600, "altura": 180, "x": 10, "y": 10},
            "gigante": {"largura": 750, "altura": 220, "x": 10, "y": 10}
        }
        return configs[self.tamanho_painel]
    
    def get_config_fonte(self):
        """Retorna configurações da fonte baseado no tamanho escolhido"""
        configs = {
            "pequeno": {"titulo": 0.6, "texto": 0.5, "espessura": 1},
            "medio": {"titulo": 0.9, "texto": 0.7, "espessura": 2},
            "grande": {"titulo": 1.2, "texto": 0.9, "espessura": 3}
        }
        return configs[self.tamanho_fonte]
    
    def get_config_janela(self):
        """Retorna configurações da janela baseado no tamanho escolhido"""
        configs = {
            "pequeno": {"largura": 1200, "altura": 900},
            "medio": {"largura": 1600, "altura": 1200},
            "grande": {"largura": 1920, "altura": 1080},
            "fullscreen": {"largura": -1, "altura": -1}  # Será detectado automaticamente
        }
        return configs[self.tamanho_janela]
    
    def definir_linha_contagem(self, frame):
        """Define linha de contagem"""
        height, width = frame.shape[:2]
        self.linha_contagem_y = height // 2
        return self.linha_contagem_y
    
    def desenhar_linha_contagem(self, frame):
        """Desenha linha de contagem"""
        if self.linha_contagem_y is not None:
            cv2.line(frame, (0, self.linha_contagem_y), 
                    (frame.shape[1], self.linha_contagem_y), (0, 255, 0), 4)
            
            fonte_config = self.get_config_fonte()
            cv2.putText(frame, "LINHA DE CONTAGEM", (15, self.linha_contagem_y - 15),
                       cv2.FONT_HERSHEY_SIMPLEX, fonte_config["texto"], (0, 255, 0), 
                       fonte_config["espessura"])
    
    def verificar_passagem(self, track_id, centro_y):
        """Verifica passagem pela linha"""
        if self.linha_contagem_y is None:
            return
        
        historico = self.track_history[track_id]
        
        if len(historico) >= 2:
            y_anterior = historico[-2][1]
            y_atual = centro_y
            
            if y_anterior < self.linha_contagem_y and y_atual >= self.linha_contagem_y:
                if track_id not in self.pessoas_contadas:
                    self.contador_entrada += 1
                    self.pessoas_contadas.add(track_id)
                    print(f"🚶 Pessoa {track_id} ENTROU! Total: {self.contador_entrada}")
            
            elif y_anterior > self.linha_contagem_y and y_atual <= self.linha_contagem_y:
                if track_id not in self.pessoas_contadas:
                    self.contador_saida += 1
                    self.pessoas_contadas.add(track_id)
                    print(f"🚶 Pessoa {track_id} SAIU! Total: {self.contador_saida}")
    
    def adicionar_info_tela(self, frame):
        """Adiciona informações na tela com tamanho personalizável"""
        painel_config = self.get_config_painel()
        fonte_config = self.get_config_fonte()
        
        # Desenha painel
        x, y = painel_config["x"], painel_config["y"]
        w, h = painel_config["largura"], painel_config["altura"]
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 3)
        
        # Calcula posições dos textos baseado no tamanho do painel
        espacamento = h // 5
        y_texto = y + espacamento
        
        # Título
        cv2.putText(frame, "CONTADOR DE PESSOAS", 
                   (x + 15, y_texto),
                   cv2.FONT_HERSHEY_SIMPLEX, fonte_config["titulo"], 
                   (0, 255, 0), fonte_config["espessura"])
        
        # Entradas
        y_texto += espacamento
        cv2.putText(frame, f"Entradas: {self.contador_entrada}", 
                   (x + 15, y_texto),
                   cv2.FONT_HERSHEY_SIMPLEX, fonte_config["texto"], 
                   (0, 255, 0), fonte_config["espessura"] - 1)
        
        # Saídas
        y_texto += espacamento
        cv2.putText(frame, f"Saidas: {self.contador_saida}", 
                   (x + 15, y_texto),
                   cv2.FONT_HERSHEY_SIMPLEX, fonte_config["texto"], 
                   (0, 255, 0), fonte_config["espessura"] - 1)
        
        # Total
        y_texto += espacamento
        total = self.contador_entrada - self.contador_saida
        cv2.putText(frame, f"Total Atual: {total}", 
                   (x + 15, y_texto),
                   cv2.FONT_HERSHEY_SIMPLEX, fonte_config["texto"], 
                   (0, 255, 255), fonte_config["espessura"])
        
        # Status da gravação (se ativada)
        if self.gravando:
            cv2.putText(frame, "🔴 GRAVANDO", 
                       (frame.shape[1] - 150, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    def processar_frame(self, frame):
        """Processa frame"""
        if self.linha_contagem_y is None:
            self.definir_linha_contagem(frame)
        
        results = self.model.track(frame, persist=True, verbose=False)
        
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confidences = results[0].boxes.conf.float().cpu().tolist()
            
            for box, track_id, conf in zip(boxes, track_ids, confidences):
                x, y, w, h = box
                centro_x = int(x)
                centro_y = int(y)
                
                self.track_history[track_id].append((centro_x, centro_y))
                if len(self.track_history[track_id]) > 30:
                    self.track_history[track_id].pop(0)
                
                self.verificar_passagem(track_id, centro_y)
                
                # Desenha bounding box
                x1 = int(x - w/2)
                y1 = int(y - h/2) 
                x2 = int(x + w/2)
                y2 = int(y + h/2)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
                cv2.putText(frame, f'ID: {track_id} ({conf:.2f})', 
                           (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                
                # Rastro
                pontos = np.array(self.track_history[track_id], dtype=np.int32)
                if len(pontos) > 1:
                    cv2.polylines(frame, [pontos], False, (0, 255, 255), 3)
        
        self.desenhar_linha_contagem(frame)
        self.adicionar_info_tela(frame)
        
        return frame
    
    def executar(self):
        """Executa o contador com configurações personalizadas"""
        # Configuração da interface
        self.configurar_interface()
        
        print("\n🚀 CONTADOR PERSONALIZADO")
        print("1. Usar com vídeo")
        print("2. Usar com câmera")
        
        opcao = input("Escolha (1-2): ").strip()
        
        if opcao == "1":
            video_path = input("Caminho do vídeo: ").strip().strip('"\'')
            if os.path.exists(video_path):
                self.processar_video(video_path)
            else:
                print("❌ Vídeo não encontrado!")
        elif opcao == "2":
            self.processar_camera()
    
    def configurar_janela(self, nome_janela):
        """Configura a janela com o tamanho escolhido"""
        janela_config = self.get_config_janela()
        
        if self.tamanho_janela == "fullscreen":
            cv2.namedWindow(nome_janela, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(nome_janela, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            cv2.namedWindow(nome_janela, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(nome_janela, janela_config["largura"], janela_config["altura"])
    
    def processar_video(self, video_path):
        """Processa vídeo com interface personalizada"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("❌ Erro ao abrir vídeo!")
            return
        
        nome_janela = "Contador Personalizado - Vídeo"
        self.configurar_janela(nome_janela)
        
        print("▶️ Processando vídeo... Pressione 'q' para sair")
        
        primeiro_frame = True
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Inicia gravação no primeiro frame
            if primeiro_frame and hasattr(self, 'configurar_gravacao'):
                self.iniciar_gravacao(frame)
                primeiro_frame = False
            
            frame_processado = self.processar_frame(frame)
            
            # Grava frame se ativado
            self.gravar_frame(frame_processado)
            
            cv2.imshow(nome_janela, frame_processado)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Para gravação se ativa
        self.parar_gravacao()
        
        self.mostrar_resultados()
    
    def processar_camera(self):
        """Processa câmera com interface personalizada"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Erro ao abrir câmera!")
            return
        
        nome_janela = "Contador Personalizado - Câmera"
        self.configurar_janela(nome_janela)
        
        print("📹 Câmera ativa... Pressione 'q' para sair")
        
        primeiro_frame = True
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Inicia gravação no primeiro frame
            if primeiro_frame and hasattr(self, 'configurar_gravacao'):
                self.iniciar_gravacao(frame)
                primeiro_frame = False
            
            frame_processado = self.processar_frame(frame)
            
            # Grava frame se ativado
            self.gravar_frame(frame_processado)
            
            cv2.imshow(nome_janela, frame_processado)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Para gravação se ativa
        self.parar_gravacao()
        
        self.mostrar_resultados()
    
    def mostrar_resultados(self):
        """Mostra resultados finais"""
        print("\n" + "="*60)
        print("📊 RESULTADOS FINAIS:")
        print(f"🚶‍♂️ Pessoas que entraram: {self.contador_entrada}")
        print(f"🚶‍♀️ Pessoas que saíram: {self.contador_saida}")
        print(f"👥 Total atual no ambiente: {self.contador_entrada - self.contador_saida}")
        print("="*60)

def main():
    """Função principal"""
    print("🎨 CONTADOR DE PESSOAS PERSONALIZÁVEL")
    print("="*50)
    print("Configure o tamanho da interface como preferir!")
    
    contador = ContadorPersonalizavel()
    contador.executar()

if __name__ == "__main__":
    main()

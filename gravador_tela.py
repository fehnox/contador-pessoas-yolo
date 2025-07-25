# ========================================
# GRAVADOR DE TELA PARA DEMONSTRAÇÕES
# ========================================
# Script para gravar a tela enquanto o contador roda

import cv2
import numpy as np
import pyautogui
import threading
import time
from datetime import datetime
import os

class GravadorTela:
    """
    Grava a tela do computador para demonstrações
    """
    
    def __init__(self):
        self.gravando = False
        self.video_writer = None
        self.thread_gravacao = None
        
    def iniciar_gravacao_tela(self, area=None, fps=20):
        """
        Inicia gravação da tela
        
        Args:
            area: Tupla (x, y, width, height) para gravar área específica
            fps: Frames por segundo
        """
        if area is None:
            # Grava tela inteira
            screen_size = pyautogui.size()
            area = (0, 0, screen_size.width, screen_size.height)
        
        x, y, width, height = area
        
        # Nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"demo_contador_{timestamp}.mp4"
        
        # Configurações do vídeo
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(
            nome_arquivo, fourcc, fps, (width, height)
        )
        
        print(f"🎬 Iniciando gravação da tela: {nome_arquivo}")
        print(f"📊 Área: {width}x{height} em ({x}, {y})")
        print("🛑 Pressione Ctrl+C para parar")
        
        self.gravando = True
        self.nome_arquivo = nome_arquivo
        
        # Inicia thread de gravação
        self.thread_gravacao = threading.Thread(
            target=self._gravar_loop, 
            args=(area, fps)
        )
        self.thread_gravacao.start()
        
        return nome_arquivo
    
    def _gravar_loop(self, area, fps):
        """Loop principal de gravação"""
        x, y, width, height = area
        delay = 1.0 / fps
        
        while self.gravando:
            try:
                # Captura screenshot
                screenshot = pyautogui.screenshot(region=area)
                
                # Converte para array numpy
                frame = np.array(screenshot)
                
                # Converte RGB para BGR (OpenCV usa BGR)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Escreve frame
                self.video_writer.write(frame)
                
                time.sleep(delay)
                
            except Exception as e:
                print(f"❌ Erro na gravação: {e}")
                break
    
    def parar_gravacao(self):
        """Para a gravação"""
        if self.gravando:
            self.gravando = False
            
            # Aguarda thread terminar
            if self.thread_gravacao:
                self.thread_gravacao.join()
            
            # Libera video writer
            if self.video_writer:
                self.video_writer.release()
            
            print(f"✅ Gravação finalizada!")
            print(f"📁 Salvo em: {os.path.abspath(self.nome_arquivo)}")

def gravar_demonstracao():
    """
    Grava uma demonstração do contador funcionando
    """
    print("🎬 GRAVADOR DE DEMONSTRAÇÃO")
    print("="*50)
    print("Este script grava sua tela enquanto você usa o contador")
    print()
    
    # Opções de gravação
    print("📊 OPÇÕES DE GRAVAÇÃO:")
    print("1. Gravar tela inteira")
    print("2. Gravar área específica") 
    print("3. Cancelar")
    
    opcao = input("\nEscolha (1-3): ").strip()
    
    if opcao == "3":
        print("❌ Cancelado!")
        return
    
    gravador = GravadorTela()
    
    try:
        if opcao == "1":
            # Tela inteira
            nome_arquivo = gravador.iniciar_gravacao_tela()
        
        elif opcao == "2":
            # Área específica
            print("\n📏 Defina a área para gravar:")
            try:
                x = int(input("X inicial: "))
                y = int(input("Y inicial: "))
                width = int(input("Largura: "))
                height = int(input("Altura: "))
                
                area = (x, y, width, height)
                nome_arquivo = gravador.iniciar_gravacao_tela(area)
            except ValueError:
                print("❌ Valores inválidos!")
                return
        
        else:
            print("❌ Opção inválida!")
            return
        
        # Aguarda gravação
        print("\n⏯️ Gravação iniciada!")
        print("🎯 Agora execute o contador em outra janela")
        print("⏹️ Pressione ENTER aqui para parar a gravação")
        
        input()  # Aguarda usuário pressionar ENTER
        
        gravador.parar_gravacao()
        
    except KeyboardInterrupt:
        print("\n🛑 Gravação interrompida!")
        gravador.parar_gravacao()
    except Exception as e:
        print(f"❌ Erro: {e}")
        gravador.parar_gravacao()

if __name__ == "__main__":
    # Verifica se pyautogui está instalado
    try:
        import pyautogui
        gravar_demonstracao()
    except ImportError:
        print("❌ PyAutoGUI não instalado!")
        print("💡 Execute: pip install pyautogui")
        print("Depois rode este script novamente.")

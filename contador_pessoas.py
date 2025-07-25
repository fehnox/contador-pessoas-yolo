# ========================================
# CONTADOR DE PESSOAS COM YOLO E TRACKING
# ========================================
# Este script implementa um sistema completo de contagem de pessoas
# usando detecção YOLO e rastreamento de objetos

# Importações necessárias
import cv2  # OpenCV para processamento de imagem e vídeo
import numpy as np  # NumPy para operações matemáticas com arrays
from ultralytics import YOLO  # YOLOv8 para detecção de objetos
from collections import defaultdict  # Para criar dicionários com valores padrão
import time  # Para operações relacionadas ao tempo

class ContadorPessoas:
    """
    Classe principal para contagem de pessoas em vídeos ou câmera ao vivo.
    
    Esta classe implementa:
    - Detecção de pessoas usando modelo YOLO
    - Rastreamento individual de cada pessoa
    - Contagem de entradas e saídas baseada em linha virtual
    - Interface visual com informações em tempo real
    """
    def __init__(self, modelo_path="runs/detect/train/weights/best.pt"):
        """
        Inicializa o contador de pessoas com todas as variáveis necessárias.
        
        Args:
            modelo_path (str): Caminho para o arquivo do modelo YOLO treinado
                              Por padrão usa o modelo treinado em 'runs/detect/train/weights/best.pt'
        
        Variáveis inicializadas:
        - self.model: Carrega o modelo YOLO para detecção
        - self.track_history: Dicionário que armazena o histórico de movimento de cada pessoa
        - self.pessoas_contadas: Set para evitar contar a mesma pessoa múltiplas vezes
        - self.contador_entrada: Número total de pessoas que entraram
        - self.contador_saida: Número total de pessoas que saíram
        - self.linha_contagem_y: Posição Y da linha virtual de contagem
        """
        # Carrega o modelo YOLO (pode ser treinado ou pré-treinado)
        self.model = YOLO(modelo_path)
        
        # Dicionário para armazenar histórico de movimento de cada pessoa rastreada
        # defaultdict cria automaticamente uma lista vazia para novos IDs
        self.track_history = defaultdict(lambda: [])
        
        # Set para armazenar IDs de pessoas já contadas (evita contagem dupla)
        self.pessoas_contadas = set()
        
        # Contadores de entrada e saída
        self.contador_entrada = 0  # Pessoas que atravessaram de cima para baixo
        self.contador_saida = 0    # Pessoas que atravessaram de baixo para cima
        
        # Posição da linha de contagem (será definida automaticamente)
        self.linha_contagem_y = None
        
    def definir_linha_contagem(self, frame):
        """
        Define automaticamente a linha de contagem no meio vertical da tela.
        
        Esta linha virtual é usada para detectar quando uma pessoa "atravessa"
        de um lado para outro, permitindo contar entradas e saídas.
        
        Args:
            frame: Frame de vídeo para obter dimensões (altura e largura)
            
        Returns:
            int: Posição Y da linha de contagem (meio da tela)
        
        Como funciona:
        - Pega a altura do frame (número de pixels verticais)
        - Divide por 2 para encontrar o meio
        - Esta será a linha imaginária de contagem
        """
        height, width = frame.shape[:2]  # Obtém altura e largura do frame
        self.linha_contagem_y = height // 2  # Define linha no meio (divisão inteira)
        return self.linha_contagem_y
    
    def desenhar_linha_contagem(self, frame):
        """
        Desenha visualmente a linha de contagem no frame de vídeo.
        
        Esta função adiciona elementos visuais para mostrar onde está
        a linha de contagem, facilitando o entendimento do usuário.
        
        Args:
            frame: Frame de vídeo onde desenhar a linha
            
        Elementos desenhados:
        - Linha verde horizontal atravessando toda a largura
        - Texto "LINHA DE CONTAGEM" acima da linha
        - Cor verde (0, 255, 0) para boa visibilidade
        """
        if self.linha_contagem_y is not None:  # Só desenha se a linha foi definida
            # Desenha linha horizontal verde de uma extremidade à outra
            cv2.line(frame, 
                    (0, self.linha_contagem_y),  # Ponto inicial (x=0, y=linha)
                    (frame.shape[1], self.linha_contagem_y),  # Ponto final (x=largura, y=linha)
                    (0, 255, 0),  # Cor verde (B, G, R)
                    3)  # Espessura da linha
            
            # Adiciona texto explicativo acima da linha
            cv2.putText(frame, 
                       "LINHA DE CONTAGEM",  # Texto a ser exibido
                       (10, self.linha_contagem_y - 10),  # Posição (x, y)
                       cv2.FONT_HERSHEY_SIMPLEX,  # Fonte
                       0.7,  # Tamanho da fonte
                       (0, 255, 0),  # Cor verde
                       2)  # Espessura do texto
    
    def verificar_passagem(self, track_id, centro_y):
        """
        Verifica se uma pessoa atravessou a linha de contagem e atualiza os contadores.
        
        Esta é a função mais importante do sistema! Ela analisa o movimento
        de cada pessoa para detectar quando atravessam a linha virtual.
        
        Args:
            track_id (int): ID único da pessoa sendo rastreada
            centro_y (int): Posição Y atual do centro da pessoa
            
        Lógica de contagem:
        - Compara posição atual com posição anterior
        - Se atravessou de cima para baixo = ENTRADA
        - Se atravessou de baixo para cima = SAÍDA
        - Evita contar a mesma pessoa múltiplas vezes
        """
        # Só funciona se a linha de contagem foi definida
        if self.linha_contagem_y is None:
            return
        
        # Obtém o histórico de movimento desta pessoa específica
        historico = self.track_history[track_id]
        
        # Precisa de pelo menos 2 pontos para comparar movimento
        if len(historico) >= 2:
            # Posição Y no frame anterior (penúltimo ponto do histórico)
            y_anterior = historico[-2][1]
            # Posição Y atual
            y_atual = centro_y
            
            # DETECÇÃO DE ENTRADA (movimento de cima para baixo)
            # Condições: estava acima da linha E agora está na linha ou abaixo
            if y_anterior < self.linha_contagem_y and y_atual >= self.linha_contagem_y:
                # Só conta se esta pessoa ainda não foi contada
                if track_id not in self.pessoas_contadas:
                    self.contador_entrada += 1  # Incrementa contador de entrada
                    self.pessoas_contadas.add(track_id)  # Marca como já contada
                    print(f"🚶 Pessoa {track_id} ENTROU! Total: {self.contador_entrada}")
            
            # DETECÇÃO DE SAÍDA (movimento de baixo para cima)  
            # Condições: estava abaixo da linha E agora está na linha ou acima
            elif y_anterior > self.linha_contagem_y and y_atual <= self.linha_contagem_y:
                # Só conta se esta pessoa ainda não foi contada
                if track_id not in self.pessoas_contadas:
                    self.contador_saida += 1  # Incrementa contador de saída
                    self.pessoas_contadas.add(track_id)  # Marca como já contada
                    print(f"🚶 Pessoa {track_id} SAIU! Total: {self.contador_saida}")
    
    def processar_frame(self, frame):
        """
        Processa um único frame de vídeo/câmera realizando toda a lógica principal.
        
        Esta função é chamada para cada frame e executa:
        1. Detecção de pessoas usando YOLO
        2. Rastreamento individual de cada pessoa
        3. Atualização do histórico de movimento
        4. Verificação de passagens pela linha
        5. Desenho de elementos visuais
        
        Args:
            frame: Frame de vídeo a ser processado
            
        Returns:
            frame: Frame processado com todas as anotações visuais
        """
        # PASSO 1: Define a linha de contagem se ainda não foi definida
        if self.linha_contagem_y is None:
            self.definir_linha_contagem(frame)
        
        # PASSO 2: Executa detecção + rastreamento com YOLO
        # persist=True mantém o rastreamento entre frames
        # verbose=False evita prints desnecessários
        results = self.model.track(frame, persist=True, verbose=False)
        
        # PASSO 3: Verifica se foram encontradas pessoas no frame
        if results[0].boxes is not None and results[0].boxes.id is not None:
            # Extrai informações das detecções
            boxes = results[0].boxes.xywh.cpu()  # Coordenadas das caixas (x, y, width, height)
            track_ids = results[0].boxes.id.int().cpu().tolist()  # IDs de rastreamento
            confidences = results[0].boxes.conf.float().cpu().tolist()  # Níveis de confiança
            
            # PASSO 4: Processa cada pessoa detectada individualmente
            for box, track_id, conf in zip(boxes, track_ids, confidences):
                x, y, w, h = box  # Desempacota coordenadas da caixa
                
                # Calcula o centro da pessoa (ponto usado para rastreamento)
                centro_x = int(x)  # Posição X do centro
                centro_y = int(y)  # Posição Y do centro (importante para contagem)
                
                # PASSO 5: Atualiza histórico de movimento desta pessoa
                self.track_history[track_id].append((centro_x, centro_y))
                
                # Mantém apenas os últimos 30 pontos para não sobrecarregar memória
                if len(self.track_history[track_id]) > 30:
                    self.track_history[track_id].pop(0)  # Remove o ponto mais antigo
                
                # PASSO 6: Verifica se esta pessoa atravessou a linha de contagem
                self.verificar_passagem(track_id, centro_y)
                
                # PASSO 7: Desenha a caixa delimitadora (bounding box) ao redor da pessoa
                # Converte coordenadas do centro+tamanho para coordenadas dos cantos
                x1 = int(x - w/2)  # Canto superior esquerdo X
                y1 = int(y - h/2)  # Canto superior esquerdo Y
                x2 = int(x + w/2)  # Canto inferior direito X
                y2 = int(y + h/2)  # Canto inferior direito Y
                
                # Desenha retângulo azul ao redor da pessoa
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                
                # Adiciona texto com ID e confiança acima da caixa
                cv2.putText(frame, f'ID: {track_id} ({conf:.2f})', 
                           (x1, y1 - 10),  # Posição do texto
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                # PASSO 8: Desenha o rastro/trilha da pessoa (linha amarela)
                pontos = np.array(self.track_history[track_id], dtype=np.int32)
                if len(pontos) > 1:  # Precisa de pelo menos 2 pontos para desenhar linha
                    cv2.polylines(frame, [pontos], False, (0, 255, 255), 2)
        
        # PASSO 9: Adiciona elementos visuais finais
        self.desenhar_linha_contagem(frame)  # Desenha a linha verde de contagem
        self.adicionar_info_tela(frame)      # Adiciona painel com informações
        
        return frame  # Retorna o frame processado
    
    def adicionar_info_tela(self, frame):
        """
        Adiciona um painel informativo MAIOR no canto superior esquerdo da tela.
        
        Este painel mostra em tempo real:
        - Título do sistema
        - Número de pessoas que entraram
        - Número de pessoas que saíram  
        - Total atual de pessoas no ambiente
        
        Args:
            frame: Frame onde adicionar as informações
        """
        # DESENHA O PAINEL DE FUNDO (MAIOR)
        # Retângulo preto preenchido para fundo do painel - AUMENTADO
        cv2.rectangle(frame, 
                     (10, 10),      # Ponto superior esquerdo
                     (550, 180),    # Ponto inferior direito (era 400x120, agora 550x180)
                     (0, 0, 0),     # Cor preta (B, G, R)
                     -1)            # -1 = preenchido
        
        # Contorno branco ao redor do painel
        cv2.rectangle(frame, 
                     (10, 10),      # Ponto superior esquerdo
                     (550, 180),    # Ponto inferior direito
                     (255, 255, 255), # Cor branca
                     3)             # Espessura da borda (era 2, agora 3)
        
        # ADICIONA OS TEXTOS INFORMATIVOS (MAIORES)
        # Título principal em verde - FONTE MAIOR
        cv2.putText(frame, f"CONTADOR DE PESSOAS", 
                   (25, 50),                    # Posição (x, y) - mais espaçada
                   cv2.FONT_HERSHEY_SIMPLEX,    # Fonte
                   1.0,                         # Tamanho (era 0.7, agora 1.0)
                   (0, 255, 0),                 # Cor verde
                   3)                           # Espessura (era 2, agora 3)
        
        # Contador de entradas - FONTE MAIOR
        cv2.putText(frame, f"Entradas: {self.contador_entrada}", 
                   (25, 90),                    # Posição (era y=60, agora y=90)
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)  # Tamanho 0.8 (era 0.6)
        
        # Contador de saídas - FONTE MAIOR
        cv2.putText(frame, f"Saidas: {self.contador_saida}", 
                   (25, 125),                   # Posição (era y=85, agora y=125)
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)  # Tamanho 0.8 (era 0.6)
        
        # Total atual (entradas - saídas = pessoas presentes) - FONTE MAIOR
        total_atual = self.contador_entrada - self.contador_saida
        cv2.putText(frame, f"Total Atual: {total_atual}", 
                   (25, 160),                   # Posição (era y=110, agora y=160)
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, 
                   (0, 255, 255),               # Cor amarela para destaque
                   3)                           # Espessura maior para destaque
    
    def contar_em_video(self, video_path):
        """
        Executa a contagem de pessoas em um arquivo de vídeo.
        
        Esta função:
        1. Abre o arquivo de vídeo
        2. Processa frame por frame
        3. Aplica detecção e contagem
        4. Mostra resultado em tempo real
        5. Gera relatório final
        
        Args:
            video_path (str): Caminho completo para o arquivo de vídeo
        """
        # ABRE O ARQUIVO DE VÍDEO
        cap = cv2.VideoCapture(video_path)
        
        # Verifica se conseguiu abrir o vídeo
        if not cap.isOpened():
            print("❌ Erro ao abrir o vídeo!")
            return
        
        print("▶️ Iniciando contagem de pessoas no vídeo...")
        print("Pressione 'q' para sair")
        
        # LOOP PRINCIPAL - PROCESSA CADA FRAME
        while True:
            # Lê o próximo frame do vídeo
            ret, frame = cap.read()  # ret = sucesso, frame = imagem
            
            # Se não conseguiu ler (fim do vídeo), sai do loop
            if not ret:
                break
            
            # PROCESSA O FRAME (detecção + contagem + desenhos)
            frame_processado = self.processar_frame(frame)
            
            # REDIMENSIONA PARA VISUALIZAÇÃO MAIOR (se muito pequeno ou muito grande)
            height, width = frame_processado.shape[:2]
            
            # Se o vídeo for muito pequeno, aumenta para tamanho mínimo
            if width < 800:
                scale = 800 / width  # Escala para largura mínima de 800px
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame_processado = cv2.resize(frame_processado, (new_width, new_height))
                print(f"📈 Vídeo ampliado para: {new_width}x{new_height}")
            
            # Se o vídeo for muito grande, reduz para tamanho máximo
            elif width > 1400:  # Era 1200, agora 1400 para permitir janelas maiores
                scale = 1400 / width  # Escala para largura máxima de 1400px
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame_processado = cv2.resize(frame_processado, (new_width, new_height))
                print(f"📉 Vídeo reduzido para: {new_width}x{new_height}")
            
            # MOSTRA O FRAME PROCESSADO NA TELA (JANELA MAIOR)
            cv2.namedWindow('Contador de Pessoas', cv2.WINDOW_NORMAL)  # Janela redimensionável
            cv2.resizeWindow('Contador de Pessoas', 1200, 800)        # Tamanho inicial maior
            cv2.imshow('Contador de Pessoas', frame_processado)
            
            # VERIFICA SE USUÁRIO QUER SAIR (tecla 'q')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # FINALIZA E LIMPA RECURSOS
        cap.release()        # Libera o arquivo de vídeo
        cv2.destroyAllWindows()  # Fecha todas as janelas OpenCV
        
        # MOSTRA RELATÓRIO FINAL
        print("\n" + "="*50)
        print("📊 RESULTADOS FINAIS:")
        print(f"🚶‍♂️ Pessoas que entraram: {self.contador_entrada}")
        print(f"🚶‍♀️ Pessoas que saíram: {self.contador_saida}")
        print(f"👥 Total atual no ambiente: {self.contador_entrada - self.contador_saida}")
        print("="*50)
    
    def contar_em_camera(self, camera_id=0):
        """
        Executa a contagem de pessoas usando câmera ao vivo.
        
        Funciona igual ao vídeo, mas captura frames em tempo real
        da câmera conectada ao computador.
        
        Args:
            camera_id (int): ID da câmera (0 = câmera padrão, 1 = segunda câmera, etc.)
        """
        # ABRE A CÂMERA
        cap = cv2.VideoCapture(camera_id)
        
        # Verifica se conseguiu abrir a câmera
        if not cap.isOpened():
            print("❌ Erro ao abrir a câmera!")
            return
        
        print("📹 Iniciando contagem de pessoas na câmera...")
        print("Pressione 'q' para sair")
        
        # LOOP PRINCIPAL - CAPTURA E PROCESSA FRAMES EM TEMPO REAL
        while True:
            # Captura frame atual da câmera
            ret, frame = cap.read()
            if not ret:
                break
            
            # PROCESSA O FRAME (mesma lógica do vídeo)
            frame_processado = self.processar_frame(frame)
            
            # CONFIGURA JANELA MAIOR E REDIMENSIONÁVEL PARA CÂMERA
            cv2.namedWindow('Contador de Pessoas - Camera', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Contador de Pessoas - Camera', 1000, 700)  # Janela maior para câmera
            
            # MOSTRA O RESULTADO EM TEMPO REAL
            cv2.imshow('Contador de Pessoas - Camera', frame_processado)
            
            # VERIFICA SE USUÁRIO QUER SAIR
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # FINALIZA RECURSOS
        cap.release()
        cv2.destroyAllWindows()
        
        # MOSTRA ESTATÍSTICAS FINAIS
        print("\n" + "="*50)
        print("📊 RESULTADOS FINAIS:")
        print(f"🚶‍♂️ Pessoas que entraram: {self.contador_entrada}")  
        print(f"🚶‍♀️ Pessoas que saíram: {self.contador_saida}")
        print(f"👥 Total atual no ambiente: {self.contador_entrada - self.contador_saida}")
        print("="*50)

# ========================================
# FUNÇÃO PRINCIPAL DO PROGRAMA
# ========================================

def main():
    """
    Função principal que executa o programa contador de pessoas.
    
    Esta função:
    1. Verifica se existe um modelo treinado
    2. Cria uma instância do contador
    3. Mostra menu de opções para o usuário
    4. Executa a opção escolhida
    
    Menu de opções:
    1. Contar pessoas em arquivo de vídeo
    2. Contar pessoas na câmera ao vivo
    3. Sair do programa
    """
    print("🤖 Iniciando Contador de Pessoas com YOLO")
    
    # VERIFICA QUAL MODELO USAR
    import os
    modelo_path = "runs/detect/train/weights/best.pt"  # Modelo treinado
    
    # Se não existe modelo treinado, usa o pré-treinado
    if not os.path.exists(modelo_path):
        print(f"⚠️ Modelo não encontrado em: {modelo_path}")
        print("💡 Primeiro execute: python treinar_yolo.py")
        print("💡 Ou use um modelo pré-treinado: yolov8n.pt")
        modelo_path = "yolov8n.pt"  # Modelo pré-treinado genérico
    
    # CRIA O CONTADOR COM O MODELO ESCOLHIDO
    contador = ContadorPessoas(modelo_path)
    
    # MOSTRA MENU DE OPÇÕES
    print("\n" + "="*50)
    print("🎯 CONTADOR DE PESSOAS - OPÇÕES:")
    print("1. Contar pessoas em vídeo")      # Análise de arquivo de vídeo
    print("2. Contar pessoas na câmera")     # Análise em tempo real
    print("3. Sair")                         # Encerrar programa
    print("="*50)
    
    # LOOP DO MENU PRINCIPAL
    while True:
        # Solicita escolha do usuário
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        # OPÇÃO 1: PROCESSAR VÍDEO
        if opcao == "1":
            # Solicita caminho do arquivo de vídeo
            video_path = input("Digite o caminho do vídeo: ").strip()
            
            # Verifica se o arquivo existe
            if os.path.exists(video_path):
                contador.contar_em_video(video_path)  # Executa contagem
            else:
                print("❌ Arquivo de vídeo não encontrado!")
        
        # OPÇÃO 2: USAR CÂMERA
        elif opcao == "2":
            contador.contar_em_camera()  # Executa contagem com câmera
        
        # OPÇÃO 3: SAIR
        elif opcao == "3":
            print("👋 Saindo...")
            break  # Sai do loop e encerra o programa
        
        # OPÇÃO INVÁLIDA
        else:
            print("❌ Opção inválida!")

# ========================================
# EXECUÇÃO DO PROGRAMA
# ========================================
if __name__ == "__main__":
    """
    Ponto de entrada do programa.
    Esta linha garante que main() só seja executada
    quando o arquivo for executado diretamente,
    não quando for importado como módulo.
    """
    main()  # Chama a função principal

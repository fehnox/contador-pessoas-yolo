# 🚶‍♀️ CONTADOR DE PESSOAS COM YOLO 🚶‍♂️

Sistema inteligente de contagem de pessoas usando **YOLOv8** e **OpenCV** para detectar, rastrear e contar pessoas em vídeos ou câmera ao vivo.

## 📋 ÍNDICE
- [Características](#-características)
- [Arquivos do Projeto](#-arquivos-do-projeto)
- [Como Usar](#-como-usar)
- [Instalação](#-instalação)
- [Estrutura do Dataset](#-estrutura-do-dataset)
- [Como Funciona](#-como-funciona)
- [Configurações](#-configurações)
- [Resolução de Problemas](#-resolução-de-problemas)

## ✨ CARACTERÍSTICAS

### 🎯 Detecção Inteligente
- **Modelo YOLO personalizado** treinado especificamente para detectar pessoas
- **Alta precisão** com modelo otimizado para seu ambiente
- **Detecção em tempo real** com performance otimizada

### 📊 Sistema de Contagem Avançado
- **Rastreamento individual** - Cada pessoa recebe um ID único
- **Linha virtual de contagem** - Detecta quando pessoas atravessam uma linha imaginária
- **Contagem bidirecional** - Separa entradas e saídas
- **Total em tempo real** - Mostra quantas pessoas estão presentemente no ambiente

### 🖥️ Interface Visual
- **Caixas delimitadoras** ao redor de cada pessoa detectada
- **Rastros de movimento** mostrando o caminho de cada pessoa
- **Painel informativo** com estatísticas em tempo real
- **Linha de contagem visual** para facilitar o entendimento

### 📹 Múltiplas Fontes
- **Arquivos de vídeo** - Processa vídeos gravados (MP4, AVI, MOV, etc.)
- **Câmera ao vivo** - Funciona com webcam em tempo real
- **Interface simples** - Menu fácil de usar

## 📁 ARQUIVOS DO PROJETO

```
📦 person-counting/
├── 🤖 contador_pessoas.py      # Sistema completo com rastreamento
├── 🔧 contador_simples.py      # Versão básica para testes
├── 🎯 teste_video.py           # Script de teste rápido
├── 🏋️ treinar_yolo.py          # Script para treinar o modelo
├── 🎬 contador_com_gravacao.py # Contador que salva vídeo processado
├── 📺 gravador_tela.py         # Grava a tela para demonstrações
├── ⚙️ data.yaml                # Configuração do dataset
├── 📋 requirements.txt         # Dependências do projeto
├── 📖 README.md               # Este arquivo
├── 🎥 GUIA_GRAVACAO.md        # Guia completo de gravação
├── 🧠 yolov8n.pt              # Modelo YOLO pré-treinado
```
│
├── 📂 train/                  # Dataset de treinamento
│   ├── images/               # Imagens para treinar
│   └── labels/               # Anotações das imagens
│
├── 📂 valid/                  # Dataset de validação
│   ├── images/               # Imagens para validar
│   └── labels/               # Anotações das imagens
│
├── 📂 test/                   # Dataset de teste
│   ├── images/               # Imagens para testar
│   └── labels/               # Anotações das imagens
│
└── 📂 runs/                   # Resultados do treinamento
    └── detect/
        └── train/
            └── weights/
                ├── best.pt    # Melhor modelo treinado
                └── last.pt    # Último modelo treinado
```

## 🚀 COMO USAR

### 1️⃣ Sistema Completo (Recomendado)
```bash
python contador_pessoas.py
```
**Menu de opções:**
- `1` - Contar pessoas em arquivo de vídeo
- `2` - Contar pessoas na câmera ao vivo  
- `3` - Sair

### 2️⃣ Teste Rápido
```bash
python teste_video.py
```
Para testar se o modelo está funcionando com um vídeo.

### 3️⃣ Contador Simples (Apenas Câmera)
```bash
python contador_simples.py
```
Versão básica que usa apenas a câmera e conta pessoas visíveis.

### 4️⃣ Treinar Novo Modelo
```bash
python treinar_yolo.py
```
Para treinar um modelo personalizado com seu dataset.

### 5️⃣ Contador com Gravação 🎬
```bash
python contador_com_gravacao.py
```
Versão que permite salvar o vídeo processado.
- **Pressione 'g'** para iniciar/parar gravação
- **Vídeo salvo** automaticamente com timestamp

### 6️⃣ Gravação de Tela 📺
```bash
python gravador_tela.py
```
Grava a tela do computador para demonstrações.
- Requer: `pip install pyautogui`

## 📦 INSTALAÇÃO

### Pré-requisitos
- Python 3.8 ou superior
- Câmera conectada (para uso ao vivo)

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Dependências Incluídas
- `ultralytics` - Framework YOLO
- `opencv-python` - Processamento de imagem/vídeo
- `numpy` - Operações matemáticas
- `Pillow` - Manipulação de imagens

## 📊 ESTRUTURA DO DATASET

O sistema usa o formato YOLO para treinamento:

```
train/images/img001.jpg  ←→  train/labels/img001.txt
```

### Formato dos Labels (.txt):
```
classe x_centro y_centro largura altura
0 0.5 0.3 0.2 0.6
```
- `classe`: 0 = pessoa
- `x_centro`: Centro X normalizado (0.0 a 1.0)
- `y_centro`: Centro Y normalizado (0.0 a 1.0)  
- `largura`: Largura normalizada (0.0 a 1.0)
- `altura`: Altura normalizada (0.0 a 1.0)

## 🔧 COMO FUNCIONA

### 1. **Detecção (YOLO)**
- Modelo neural identifica pessoas em cada frame
- Gera caixas delimitadoras com nível de confiança
- Funciona em tempo real (30+ FPS)

### 2. **Rastreamento (Tracking)**
- Cada pessoa detectada recebe um ID único
- Sistema acompanha movimento entre frames
- Mantém histórico das posições

### 3. **Contagem (Linha Virtual)**
```
    🚶‍♀️ ← Pessoa entrando
────────────────────────── ← Linha de contagem (meio da tela)
    🚶‍♂️ → Pessoa saindo
```
- Linha imaginária no meio da tela
- Detecta quando pessoa atravessa a linha
- Diferencia direção do movimento

### 4. **Interface Visual**
```
┌─────────────────────────┐
│ CONTADOR DE PESSOAS     │
│ Entradas: 15            │
│ Saídas: 8               │  
│ Total Atual: 7          │
└─────────────────────────┘
```

## ⚙️ CONFIGURAÇÕES

### Ajustar Sensibilidade
No arquivo `contador_pessoas.py`, linha ~175:
```python
if conf > 0.3:  # Mude este valor
    # 0.3 = 30% de confiança mínima
    # Menor = mais sensível (pode ter falsos positivos)
    # Maior = menos sensível (pode perder pessoas)
```

### Mudar Posição da Linha
No arquivo `contador_pessoas.py`, método `definir_linha_contagem`:
```python
self.linha_contagem_y = height // 2  # Meio da tela
# Para 1/3 da tela: height // 3
# Para 2/3 da tela: (height * 2) // 3
```

### Otimizar Performance
No arquivo `contador_pessoas.py`, linha ~160:
```python
if frame_count % 3 == 0:  # Processa a cada 3 frames
    # 1 = Máxima precisão (mais lento)
    # 5 = Boa performance (menos preciso)
```

## 🔧 RESOLUÇÃO DE PROBLEMAS

### ❌ "Modelo não encontrado"
**Problema:** Não existe modelo treinado.  
**Solução:** 
```bash
python treinar_yolo.py  # Treina novo modelo
# OU usa modelo pré-treinado automaticamente
```

### ❌ "Erro ao abrir câmera"
**Problema:** Câmera não detectada.  
**Soluções:**
- Verificar se câmera está conectada
- Fechar outros programas que usam câmera
- Tentar camera_id diferente (0, 1, 2...)

### ❌ "Erro ao abrir vídeo"
**Problema:** Arquivo de vídeo inválido.  
**Soluções:**
- Verificar se caminho está correto
- Usar aspas no caminho: `"C:\pasta\video.mp4"`
- Formatos suportados: MP4, AVI, MOV, MKV, WMV

### ⚠️ Contagem imprecisa
**Possíveis causas:**
- Linha de contagem mal posicionada
- Confiança muito baixa/alta
- Pessoas se movendo muito rápido
- Iluminação inadequada

**Soluções:**
- Ajustar parâmetros de confiança
- Treinar modelo com mais dados similares
- Melhorar iluminação do ambiente

### 🐌 Performance lenta
**Soluções:**
- Aumentar intervalo de processamento (linha 160)
- Usar modelo menor (yolov8n.pt em vez de yolov8x.pt)
- Redimensionar vídeo para resolução menor

## 📈 MELHORIAS FUTURAS

- ✅ Contagem bidirecional
- ✅ Interface gráfica amigável
- ✅ Suporte múltiplos formatos de vídeo
- 🔄 Exportar relatórios (CSV, PDF)
- 🔄 API web para integração
- 🔄 Múltiplas linhas de contagem
- 🔄 Detecção de aglomerações
- 🔄 Alertas em tempo real

## 👨‍💻 AUTOR

Desenvolvido como projeto de contagem inteligente de pessoas usando IA.

---

## 🎯 RESUMO RÁPIDO

1. **Instalar:** `pip install -r requirements.txt`
2. **Executar:** `python contador_pessoas.py`
3. **Escolher:** Opção 1 (vídeo) ou 2 (câmera)
4. **Observar:** Contagem em tempo real na tela

**Pronto! Seu contador de pessoas está funcionando! 🎉**

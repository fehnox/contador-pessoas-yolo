# 🚶‍♂️ Sistema de Conta# Clone o repositório
git clone https://github.com/fehnox/contador-pessoas-yolo.git
cd contador-pessoas-yolo de Pessoas com YOLOv8

Um sistema inteligente de contagem de pessoas usando YOLOv8 e OpenCV, com interface personalizável e funcionalidades de gravação.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-ultralytics-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Características

- ✅ **Detecção Precisa**: Utiliza YOLOv8 para detecção de pessoas
- ✅ **Rastreamento Individual**: Cada pessoa recebe um ID único
- ✅ **Contagem Bidirecional**: Conta entradas e saídas separadamente
- ✅ **Interface Personalizável**: 4 tamanhos de painel, 4 tamanhos de janela
- ✅ **Gravação Integrada**: Salva vídeos das sessões de contagem
- ✅ **Múltiplas Fontes**: Funciona com vídeos e câmera ao vivo
- ✅ **Modelo Customizável**: Suporte para modelo pré-treinado ou custom

## 🚀 Início Rápido

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/contador-pessoas-yolo.git
cd contador-pessoas-yolo

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o contador personalizável
python contador_personalizavel.py
```

### Uso Básico

1. **Execute**: `python contador_personalizavel.py`
2. **Configure**: Escolha tamanhos de painel, janela e fonte
3. **Grave** (opcional): Ative gravação se desejar
4. **Use**: Selecione vídeo ou câmera

## 📁 Estrutura do Projeto

```
📦 contador-pessoas-yolo/
├── 🎨 contador_personalizavel.py    # Contador com interface personalizável
├── 📹 contador_com_gravacao.py      # Contador com gravação integrada
├── 🎯 contador_pessoas.py           # Sistema completo principal
├── 🎯 contador_simples.py           # Versão básica para câmera
├── 🧪 teste_video.py                # Teste com arquivos de vídeo
├── 🎬 gravador_tela.py             # Gravador de tela
├── 🏃 iniciar_facil.py             # Launcher simplificado
├── ⚙️ treinar_yolo.py              # Script para treinar modelo custom
├── 📋 requirements.txt              # Dependências do projeto
├── 📊 data.yaml                     # Configuração do dataset
├── 📖 README.md                     # Documentação
├── 📖 GUIA_GRAVACAO.md             # Guia de gravação
├── 🤖 yolov8n.pt                   # Modelo pré-treinado
├── 📂 test/                         # Imagens de teste
├── 📂 train/                        # Imagens de treino
├── 📂 valid/                        # Imagens de validação
├── 📂 runs/                         # Resultados de treinamento
└── 📂 videos do projeto/            # Vídeos de exemplo
```

## 🎮 Opções de Execução

### 🎨 Contador Personalizável (Recomendado)
```bash
python contador_personalizavel.py
```
- Interface totalmente configurável
- Escolha tamanhos de painel, janela e fonte
- Opção de gravação integrada

### 📹 Contador com Gravação
```bash
python contador_com_gravacao.py
```
- Versão com gravação automática
- Interface otimizada para demonstrações

### 🎯 Contador Principal
```bash
python contador_pessoas.py
```
- Sistema completo com todas as funcionalidades
- Interface fixa otimizada

### 🎯 Contador Simples
```bash
python contador_simples.py
```
- Versão básica apenas com câmera
- Interface minimalista

### 🧪 Teste com Vídeo
```bash
python teste_video.py
```
- Para testar com arquivos de vídeo
- Útil para validação do modelo

### 🎬 Gravação de Tela
```bash
python gravador_tela.py
```
- Grava a tela enquanto usa o contador
- Ideal para criar demonstrações

## ⚙️ Configurações

### Tamanhos de Interface (Contador Personalizável)

| Tipo | Pequeno | Médio | Grande | Gigante/Fullscreen |
|------|---------|-------|--------|--------------------|
| **Painel** | 300x100 | 450x140 | 600x180 | 750x220 |
| **Janela** | 1200x900 | 1600x1200 | 1920x1080 | Tela Cheia |
| **Fonte** | 0.5-0.6 | 0.7-0.9 | 0.9-1.2 | - |

### Funcionalidades por Versão

| Recurso | Simples | Principal | Com Gravação | Personalizável | Teste |
|---------|---------|-----------|--------------|----------------|-------|
| Contagem | ✅ | ✅ | ✅ | ✅ | ✅ |
| Rastreamento | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gravação | ❌ | ❌ | ✅ | ✅ (opcional) | ❌ |
| Interface Customizável | ❌ | ❌ | ❌ | ✅ | ❌ |
| Câmera | ✅ | ✅ | ✅ | ✅ | ❌ |
| Vídeo | ❌ | ✅ | ✅ | ✅ | ✅ |
| Menu Interativo | ❌ | ✅ | ✅ | ✅ | ❌ |

## 🛠️ Tecnologias Utilizadas

- **[YOLOv8 (Ultralytics)](https://github.com/ultralytics/ultralytics)**: Detecção de pessoas
- **[OpenCV](https://opencv.org/)**: Processamento de vídeo e interface
- **[NumPy](https://numpy.org/)**: Manipulação de arrays
- **[Python 3.8+](https://python.org/)**: Linguagem principal

## 📊 Como Funciona

### 1. Detecção e Rastreamento
- **Modelo**: YOLOv8n (nano) para velocidade otimizada
- **Tracking**: Sistema de IDs únicos para cada pessoa
- **Linha Virtual**: Detecção de cruzamento para contagem
- **Histórico**: Rastro visual do movimento das pessoas

### 2. Sistema de Contagem
- **Entradas**: Pessoas que cruzam a linha de cima para baixo
- **Saídas**: Pessoas que cruzam a linha de baixo para cima
- **Total Atual**: Diferença entre entradas e saídas
- **Prevenção de Duplicatas**: Cada pessoa é contada apenas uma vez

### 3. Interface Visual
- **Bounding Boxes**: Caixas ao redor das pessoas detectadas
- **IDs e Confiança**: Mostra ID único e precisão da detecção
- **Rastros**: Linha colorida mostrando o caminho percorrido
- **Painel Informativo**: Estatísticas em tempo real
- **Linha de Contagem**: Linha verde horizontal para referência

### 4. Gravação e Exportação
- **Formato**: MP4 com codec mp4v
- **Qualidade**: Mantém resolução original
- **Timestamp**: Arquivos nomeados automaticamente
- **Gravação de Tela**: Captura toda a sessão de trabalho

## 🎓 Modelo Personalizado

### Como Treinar

```bash
# 1. Prepare seu dataset no formato YOLO
# 2. Configure o data.yaml
# 3. Execute o treinamento
python treinar_yolo.py

# 4. O modelo treinado ficará em runs/detect/train/weights/best.pt
```

### Estrutura do Dataset

```
📂 dataset/
├── 📂 train/
│   ├── 📂 images/     # Imagens de treinamento
│   └── 📂 labels/     # Labels no formato YOLO
├── 📂 valid/
│   ├── 📂 images/     # Imagens de validação
│   └── 📂 labels/     # Labels no formato YOLO
└── 📂 test/
    ├── 📂 images/     # Imagens de teste
    └── 📂 labels/     # Labels no formato YOLO
```

## 🎮 Controles

- **'q' ou ESC**: Sair do programa
- **Mouse**: Redimensionar janelas (versões com WINDOW_NORMAL)

## 📋 Dependências

```txt
ultralytics>=8.0.0
opencv-python>=4.5.0
numpy>=1.21.0
pillow>=8.0.0
pyautogui>=0.9.50
```

## 🐛 Resolução de Problemas

### Problemas Comuns

1. **Modelo não encontrado**
   - O sistema usa automaticamente o modelo pré-treinado se não encontrar modelo custom

2. **Câmera não funciona**
   - Verifique se a câmera não está sendo usada por outro programa
   - Teste com `python contador_simples.py`

3. **Performance baixa**
   - Use o modelo nano (yolov8n.pt) para melhor velocidade
   - Reduza a resolução do vídeo se necessário

4. **Erro de instalação**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Suporte

- 📧 **Email**: seu-email@exemplo.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/SEU_USUARIO/contador-pessoas-yolo/issues)
- 📖 **Wiki**: [Documentação Completa](https://github.com/SEU_USUARIO/contador-pessoas-yolo/wiki)

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a Branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Diretrizes de Contribuição

- Mantenha o código limpo e comentado
- Teste suas mudanças antes de submeter
- Atualize a documentação se necessário
- Siga as convenções de nomenclatura existentes

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

```
MIT License

Copyright (c) 2025 [SEU_NOME]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🏆 Créditos

Desenvolvido por **fehnox** como projeto acadêmico.

### Agradecimentos
- **Ultralytics** pela biblioteca YOLOv8
- **OpenCV** pela biblioteca de visão computacional
- **Roboflow** pelas ferramentas de dataset
- **Comunidade Python** pelo suporte e bibliotecas

---

## 📸 Screenshots

### Interface Personalizável
*Em breve: Capturas de tela do contador personalizável*

### Detecção em Ação
*Em breve: GIFs mostrando o sistema funcionando*

### Diferentes Tamanhos de Interface
*Em breve: Comparison dos diferentes tamanhos*

---

⭐ **Se este projeto te ajudou, deixe uma estrela!** ⭐

## 📊 Estatísticas

![GitHub stars](https://img.shields.io/github/stars/fehnox/contador-pessoas-yolo)
![GitHub forks](https://img.shields.io/github/forks/fehnox/contador-pessoas-yolo)
![GitHub issues](https://img.shields.io/github/issues/fehnox/contador-pessoas-yolo)
![GitHub last commit](https://img.shields.io/github/last-commit/fehnox/contador-pessoas-yolo)

---

**💡 Dica**: Para melhor experiência, use o `contador_personalizavel.py` que permite ajustar a interface completamente ao seu gosto!

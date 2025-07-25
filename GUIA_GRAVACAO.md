# 🎬 GUIA COMPLETO DE GRAVAÇÃO DO CONTADOR

Este arquivo explica todas as formas de gravar o contador funcionando para demonstrações, apresentações ou documentação.

## 🎯 **OPÇÕES DE GRAVAÇÃO**

### 1️⃣ **GRAVAÇÃO INTEGRADA (Recomendada)**
Salva o vídeo processado diretamente pelo contador:

```bash
python contador_com_gravacao.py
```

**Vantagens:**
- ✅ Qualidade máxima (sem perda)
- ✅ Arquivo otimizado
- ✅ Controles simples (tecla 'g')
- ✅ Não afeta performance

**Como usar:**
1. Execute o script
2. Escolha vídeo ou câmera
3. Pressione **'g'** para iniciar/parar gravação
4. Pressione **'q'** para sair

### 2️⃣ **GRAVAÇÃO DE TELA**
Grava a tela do computador:

```bash
# Primeiro instale a dependência:
pip install pyautogui

# Depois execute:
python gravador_tela.py
```

**Vantagens:**
- ✅ Grava interface completa
- ✅ Inclui menus e transições
- ✅ Bom para tutoriais

### 3️⃣ **GRAVAÇÃO MANUAL (Windows)**

#### **Usando Xbox Game Bar (Windows 10/11):**
1. **Pressione** `Windows + G`
2. **Clique** no botão de gravação (círculo)
3. **Execute** o contador
4. **Pressione** `Windows + Alt + R` para parar

#### **Usando OBS Studio (Profissional):**
1. **Baixe** OBS Studio (gratuito)
2. **Configure** captura de tela
3. **Inicie** gravação
4. **Execute** o contador

---

## 🚀 **EXEMPLO PRÁTICO - PASSO A PASSO**

### **Para gravar uma demonstração completa:**

1. **Prepare o ambiente:**
   ```bash
   cd "C:\Users\Pichau\Desktop\Faculdade Materias\Trabalho Yan\person counting.v1i.yolov8"
   ```

2. **Execute o contador com gravação:**
   ```bash
   python contador_com_gravacao.py
   ```

3. **No menu, escolha opção 1** (vídeo) ou 2 (câmera)

4. **Se escolheu vídeo, digite o caminho:**
   ```
   "C:\Users\Pichau\Desktop\Faculdade Materias\Trabalho Yan\videoplayback.mp4"
   ```

5. **Quando o contador abrir:**
   - **Pressione 'g'** → Inicia gravação (aparece 🔴 GRAVANDO)
   - **Deixe rodar** alguns minutos
   - **Pressione 'g'** novamente → Para gravação
   - **Pressione 'q'** → Sai do programa

6. **Arquivo será salvo como:**
   ```
   contador_gravado_20250124_143055.mp4
   ```

---

## 📁 **ARQUIVOS GERADOS**

### **Gravação Integrada:**
- `contador_gravado_YYYYMMDD_HHMMSS.mp4`
- Localização: Pasta do projeto
- Qualidade: Original (mesma do processamento)

### **Gravação de Tela:**
- `demo_contador_YYYYMMDD_HHMMSS.mp4`
- Localização: Pasta do projeto
- Qualidade: Dependente da resolução da tela

---

## ⚙️ **CONFIGURAÇÕES AVANÇADAS**

### **Ajustar qualidade da gravação:**
No arquivo `contador_com_gravacao.py`, linha ~87:
```python
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec padrão
# Opções:
# *'XVID' - Menor arquivo, boa qualidade
# *'mp4v' - Compatibilidade máxima
# *'H264' - Melhor qualidade (se disponível)
```

### **Ajustar FPS da gravação:**
```python
self.iniciar_gravacao(width, height, fps=30)  # Mude o FPS aqui
# fps=15  - Arquivo menor, movimento menos fluido
# fps=30  - Balanceado (recomendado)
# fps=60  - Muito fluido, arquivo grande
```

---

## 🎭 **DICAS PARA DEMONSTRAÇÕES**

### **Antes de gravar:**
1. ✅ **Teste** o contador primeiro
2. ✅ **Feche** outros programas
3. ✅ **Prepare** o vídeo de teste
4. ✅ **Limpe** a área de trabalho

### **Durante a gravação:**
1. 🎬 **Movimente-se devagar** para a câmera capturar
2. 📢 **Comente** o que está acontecendo
3. ⏱️ **Deixe** pelo menos 30 segundos gravando
4. 🔍 **Mostre** os contadores aumentando

### **Roteiro sugerido:**
```
1. "Olá! Vou demonstrar meu contador de pessoas com IA"
2. Execute: python contador_com_gravacao.py
3. "Vou escolher um vídeo de teste"
4. Escolha opção 1 e digite caminho
5. "Agora vou iniciar a gravação"
6. Pressione 'g'
7. "Observem a linha verde - é onde conta as pessoas"
8. "Vejam os números aumentando: entradas, saídas, total"
9. Deixe rodar uns 2-3 minutos
10. "Vou parar a gravação"
11. Pressione 'g' novamente
12. "E sair do programa"
13. Pressione 'q'
14. "Pronto! O vídeo foi salvo automaticamente"
```

---

## 🔧 **RESOLUÇÃO DE PROBLEMAS**

### **❌ "Erro ao iniciar gravação"**
**Causas:**
- Disco cheio
- Permissões insuficientes
- Codec não disponível

**Soluções:**
- Libere espaço em disco
- Execute como administrador
- Instale codecs: `pip install opencv-python[headless]`

### **❌ "Vídeo não reproduz"**
**Causas:**
- Player não suporta codec
- Arquivo corrompido

**Soluções:**
- Use VLC Media Player
- Converta com FFmpeg
- Grave novamente com codec diferente

### **❌ "Gravação muito lenta"**
**Soluções:**
- Reduza FPS para 15
- Use resolução menor
- Feche outros programas

---

## 📊 **TAMANHOS DE ARQUIVO ESPERADOS**

| Duração | Resolução | FPS | Tamanho Aprox. |
|---------|-----------|-----|----------------|
| 1 min   | 640x480   | 30  | ~15 MB        |
| 1 min   | 1280x720  | 30  | ~30 MB        |
| 5 min   | 640x480   | 30  | ~75 MB        |
| 5 min   | 1280x720  | 30  | ~150 MB       |

---

## 🎉 **EXEMPLOS DE USO**

### **Para apresentação acadêmica:**
```bash
python contador_com_gravacao.py
# Escolha vídeo com várias pessoas
# Grave 3-5 minutos
# Explique como funciona
```

### **Para demonstração profissional:**
```bash
python contador_com_gravacao.py
# Use câmera ao vivo
# Peça pessoas para passar na frente
# Mostre contagem em tempo real
```

### **Para tutorial/documentação:**
```bash
python gravador_tela.py
# Grave tela inteira
# Mostre menus e opções
# Explique cada passo
```

---

## 🎬 **CHECKLIST FINAL**

Antes de gravar sua demonstração:

- [ ] Contador funcionando
- [ ] Vídeo de teste preparado
- [ ] Boa iluminação (para câmera)
- [ ] Espaço em disco suficiente
- [ ] Outros programas fechados
- [ ] Roteiro preparado
- [ ] Gravação testada rapidamente

**Agora você está pronto para gravar uma demonstração profissional! 🚀**

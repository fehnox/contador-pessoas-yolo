#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SETUP AUTOMÁTICO DO CONTADOR DE PESSOAS
========================================
Script para configurar o ambiente automaticamente
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(title):
    """Imprime cabeçalho formatado"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def run_command(command, description):
    """Executa comando e mostra progresso"""
    print(f"\n📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - Concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        print(f"Output: {e.output}")
        return False

def check_python_version():
    """Verifica versão do Python"""
    print_header("VERIFICANDO PYTHON")
    
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário!")
        print("💡 Por favor, atualize seu Python")
        return False
    
    print("✅ Versão do Python OK!")
    return True

def install_requirements():
    """Instala dependências"""
    print_header("INSTALANDO DEPENDÊNCIAS")
    
    requirements = [
        "ultralytics>=8.0.0",
        "opencv-python>=4.5.0", 
        "numpy>=1.21.0",
        "pillow>=8.0.0",
        "pyautogui>=0.9.50"
    ]
    
    for req in requirements:
        if not run_command(f"pip install {req}", f"Instalando {req.split('>=')[0]}"):
            print(f"⚠️ Falha ao instalar {req}")
    
    return True

def download_yolo_model():
    """Baixa modelo YOLO se não existir"""
    print_header("VERIFICANDO MODELO YOLO")
    
    model_path = Path("yolov8n.pt")
    
    if model_path.exists():
        print("✅ Modelo YOLOv8n já existe!")
        return True
    
    print("📥 Baixando modelo YOLOv8n...")
    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")  # Isso baixa automaticamente
        print("✅ Modelo YOLOv8n baixado!")
        return True
    except Exception as e:
        print(f"❌ Erro ao baixar modelo: {e}")
        return False

def create_folders():
    """Cria pastas necessárias"""
    print_header("CRIANDO ESTRUTURA DE PASTAS")
    
    folders = [
        "runs/detect/train/weights",
        "screenshots", 
        "demos",
        "videos_output"
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"📁 Criado: {folder}")
    
    print("✅ Estrutura de pastas criada!")
    return True

def test_installation():
    """Testa a instalação"""
    print_header("TESTANDO INSTALAÇÃO")
    
    try:
        # Testa imports
        print("🔍 Testando imports...")
        import cv2
        import numpy as np
        from ultralytics import YOLO
        print("✅ Imports OK!")
        
        # Testa modelo YOLO
        print("🤖 Testando modelo YOLO...")
        model = YOLO("yolov8n.pt")
        print("✅ Modelo YOLO OK!")
        
        # Testa OpenCV
        print("📹 Testando OpenCV...")
        print(f"OpenCV versão: {cv2.__version__}")
        print("✅ OpenCV OK!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def show_usage():
    """Mostra instruções de uso"""
    print_header("COMO USAR")
    
    print("🎯 OPÇÕES DISPONÍVEIS:")
    print("├── python contador_personalizavel.py  # Recomendado - Interface personalizável")
    print("├── python contador_com_gravacao.py    # Com gravação automática")
    print("├── python contador_pessoas.py         # Sistema completo")
    print("├── python contador_simples.py         # Versão básica")
    print("├── python teste_video.py              # Teste com vídeos")
    print("└── python gravador_tela.py            # Gravação de tela")
    
    print("\n🚀 INÍCIO RÁPIDO:")
    print("1. Execute: python contador_personalizavel.py")
    print("2. Configure interface (tamanhos)")
    print("3. Escolha gravação (s/n)")
    print("4. Selecione vídeo ou câmera")
    print("5. Pressione 'q' para sair")
    
    print("\n📖 DOCUMENTAÇÃO:")
    print("├── README_GITHUB.md  # Documentação completa")
    print("├── GUIA_GRAVACAO.md  # Guia de gravação")
    print("└── requirements.txt  # Lista de dependências")

def main():
    """Função principal"""
    print_header("SETUP CONTADOR DE PESSOAS COM YOLO")
    
    print("🎯 Este script vai configurar tudo automaticamente!")
    print("⏱️ Tempo estimado: 2-5 minutos")
    
    input("\n🚀 Pressione ENTER para continuar...")
    
    # Passos do setup
    steps = [
        ("Verificar Python", check_python_version),
        ("Instalar dependências", install_requirements),
        ("Baixar modelo YOLO", download_yolo_model),
        ("Criar pastas", create_folders),
        ("Testar instalação", test_installation)
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        if step_func():
            success_count += 1
        else:
            print(f"⚠️ Falha em: {step_name}")
    
    # Resultado final
    print_header("RESULTADO DO SETUP")
    
    if success_count == len(steps):
        print("🎉 SETUP CONCLUÍDO COM SUCESSO!")
        print("✅ Tudo está pronto para usar!")
        show_usage()
    else:
        print(f"⚠️ Setup parcial: {success_count}/{len(steps)} passos concluídos")
        print("💡 Verifique os erros acima e tente novamente")
    
    print(f"\n{'='*60}")
    print("🙏 Obrigado por usar o Contador de Pessoas!")
    print("⭐ Se gostou, deixe uma estrela no GitHub!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DEMONSTRAÇÃO RÁPIDA - CONTADOR DE PESSOAS
==========================================
Script para mostrar as funcionalidades rapidamente
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Banner do projeto"""
    banner = """
🚶‍♂️ CONTADOR DE PESSOAS COM YOLO 🚶‍♀️
============================================
Sistema Inteligente de Contagem de Pessoas
    """
    print(banner)

def show_menu():
    """Mostra menu principal"""
    print("\n🎯 DEMONSTRAÇÕES DISPONÍVEIS:")
    print("="*50)
    print("1. 🎨 Contador Personalizável (Recomendado)")
    print("2. 📹 Contador com Gravação")
    print("3. 🎯 Contador Principal")
    print("4. 🎯 Contador Simples (Câmera)")
    print("5. 🧪 Teste com Vídeo")
    print("6. 🎬 Gravador de Tela")
    print("7. 📊 Treinar Modelo")
    print("8. ⚙️ Setup Automático")
    print("9. 📖 Ver Documentação")
    print("0. ❌ Sair")
    print("="*50)

def run_script(script_name, description):
    """Executa um script Python"""
    print(f"\n🚀 Executando: {description}")
    print("="*50)
    
    if not Path(script_name).exists():
        print(f"❌ Arquivo não encontrado: {script_name}")
        return False
    
    try:
        # Executa o script
        subprocess.run([sys.executable, script_name], check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao executar {script_name}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ Execução interrompida pelo usuário")
        return True

def show_documentation():
    """Mostra documentação rápida"""
    print("\n📖 DOCUMENTAÇÃO RÁPIDA")
    print("="*50)
    
    docs = {
        "README_GITHUB.md": "Documentação completa do projeto",
        "GUIA_GRAVACAO.md": "Como gravar vídeos das sessões",
        "requirements.txt": "Lista de dependências necessárias",
        "data.yaml": "Configuração do dataset para treinamento"
    }
    
    for file, desc in docs.items():
        if Path(file).exists():
            print(f"✅ {file:<20} - {desc}")
        else:
            print(f"❌ {file:<20} - {desc} (não encontrado)")
    
    print("\n💡 DICAS DE USO:")
    print("• Pressione 'q' para sair de qualquer contador")
    print("• Use o contador personalizável para melhor experiência") 
    print("• Ative gravação para salvar demonstrações")
    print("• Teste com vídeos antes de usar câmera ao vivo")

def check_files():
    """Verifica se arquivos principais existem"""
    required_files = [
        "contador_personalizavel.py",
        "contador_com_gravacao.py", 
        "contador_pessoas.py",
        "contador_simples.py",
        "teste_video.py",
        "gravador_tela.py",
        "treinar_yolo.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("⚠️ ARQUIVOS FALTANDO:")
        for file in missing_files:
            print(f"   ❌ {file}")
        return False
    
    return True

def main():
    """Função principal"""
    print_banner()
    
    # Verifica arquivos
    if not check_files():
        print("\n💡 Alguns arquivos estão faltando!")
        print("Certifique-se de ter todos os arquivos do projeto.")
        return
    
    while True:
        show_menu()
        
        try:
            opcao = input("\n🎯 Escolha uma opção (0-9): ").strip()
            
            if opcao == "0":
                print("\n👋 Até logo!")
                break
            
            elif opcao == "1":
                run_script("contador_personalizavel.py", 
                          "Contador com Interface Personalizável")
            
            elif opcao == "2":
                run_script("contador_com_gravacao.py", 
                          "Contador com Gravação Automática")
            
            elif opcao == "3":
                run_script("contador_pessoas.py", 
                          "Sistema Completo Principal")
            
            elif opcao == "4":
                run_script("contador_simples.py", 
                          "Contador Simples (Apenas Câmera)")
            
            elif opcao == "5":
                run_script("teste_video.py", 
                          "Teste com Arquivo de Vídeo")
            
            elif opcao == "6":
                run_script("gravador_tela.py", 
                          "Gravador de Tela para Demonstrações")
            
            elif opcao == "7":
                run_script("treinar_yolo.py", 
                          "Treinamento de Modelo Personalizado")
            
            elif opcao == "8":
                run_script("setup.py", 
                          "Setup Automático do Ambiente")
            
            elif opcao == "9":
                show_documentation()
            
            else:
                print("❌ Opção inválida! Escolha entre 0-9.")
            
            if opcao != "9":
                input("\n⏸️ Pressione ENTER para voltar ao menu...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            input("⏸️ Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()

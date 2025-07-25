#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 INICIALIZADOR FÁCIL DO CONTADOR DE PESSOAS
==============================================
Este script facilita a execução do contador para iniciantes.
Basta executar este arquivo que ele cuida de tudo!
"""

import os
import sys

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    arquivos_necessarios = [
        'contador_pessoas.py',
        'data.yaml',
        'requirements.txt'
    ]
    
    arquivos_faltando = []
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            arquivos_faltando.append(arquivo)
    
    return arquivos_faltando

def verificar_python():
    """Verifica se Python está instalado corretamente"""
    try:
        import ultralytics
        import cv2
        import numpy
        return True, "Todas as dependências estão instaladas ✅"
    except ImportError as e:
        return False, f"Dependência faltando: {e}"

def mostrar_banner():
    """Mostra banner de boas-vindas"""
    banner = """
    ═══════════════════════════════════════════════
    🚶‍♀️ CONTADOR DE PESSOAS COM IA 🚶‍♂️
    ═══════════════════════════════════════════════
    
    🤖 Sistema inteligente de contagem usando YOLO
    📹 Funciona com vídeos e câmera ao vivo
    📊 Rastreamento individual de pessoas
    ⚡ Interface fácil de usar
    
    ═══════════════════════════════════════════════
    """
    print(banner)

def menu_principal():
    """Mostra menu principal e retorna a escolha"""
    print("\n🎯 ESCOLHA UMA OPÇÃO:")
    print("=" * 50)
    print("1️⃣  Contador COMPLETO (com rastreamento)")
    print("2️⃣  Contador SIMPLES (apenas câmera)")
    print("3️⃣  Teste RÁPIDO (testar com vídeo)")
    print("4️⃣  Treinar NOVO MODELO")
    print("5️⃣  Ajuda e Instruções")
    print("0️⃣  Sair")
    print("=" * 50)
    
    while True:
        try:
            escolha = input("\n👉 Digite sua escolha (0-5): ").strip()
            if escolha in ['0', '1', '2', '3', '4', '5']:
                return escolha
            else:
                print("❌ Opção inválida! Digite um número de 0 a 5.")
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            sys.exit(0)

def executar_comando(comando, descricao):
    """Executa um comando Python"""
    print(f"\n🚀 {descricao}")
    print(f"📝 Executando: python {comando}")
    print("─" * 50)
    
    try:
        os.system(f"python {comando}")
    except KeyboardInterrupt:
        print("\n⚠️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
    
    input("\n🔙 Pressione ENTER para voltar ao menu...")

def mostrar_ajuda():
    """Mostra instruções detalhadas"""
    ajuda = """
    📖 COMO USAR O CONTADOR DE PESSOAS:
    ═══════════════════════════════════════
    
    🎯 OPÇÃO 1 - CONTADOR COMPLETO:
    • Melhor opção para uso profissional
    • Rastreia cada pessoa individualmente
    • Conta entradas e saídas separadamente
    • Funciona com vídeos e câmera
    
    📹 Para usar com vídeo:
    • Escolha opção 1 no menu
    • Digite o caminho completo do vídeo
    • Exemplo: C:\\Users\\Seu Nome\\Videos\\teste.mp4
    • Use aspas se o caminho tiver espaços
    
    📷 Para usar com câmera:
    • Escolha opção 2 no menu
    • Câmera abrirá automaticamente
    • Pressione 'q' para sair
    
    🔧 OPÇÃO 2 - CONTADOR SIMPLES:
    • Versão básica apenas com câmera
    • Conta pessoas visíveis no momento
    • Mais rápido e simples
    
    🧪 OPÇÃO 3 - TESTE RÁPIDO:
    • Para testar se está funcionando
    • Use com um vídeo pequeno primeiro
    • Verifica se modelo está carregado
    
    🏋️ OPÇÃO 4 - TREINAR MODELO:
    • Treina novo modelo com seus dados
    • Demora algumas horas
    • Melhora a precisão para seu ambiente
    
    ⚡ DICAS IMPORTANTES:
    • Pressione 'q' para sair de qualquer vídeo
    • Use boa iluminação para melhor detecção
    • Pessoas muito rápidas podem não ser contadas
    • Primeiro teste com vídeo, depois câmera
    
    ═══════════════════════════════════════
    """
    print(ajuda)
    input("🔙 Pressione ENTER para voltar ao menu...")

def main():
    """Função principal do inicializador"""
    while True:
        limpar_tela()
        mostrar_banner()
        
        # Verifica arquivos necessários
        arquivos_faltando = verificar_arquivos()
        if arquivos_faltando:
            print("❌ ERRO: Arquivos necessários não encontrados:")
            for arquivo in arquivos_faltando:
                print(f"   • {arquivo}")
            print("\n💡 Certifique-se de estar na pasta correta do projeto!")
            input("🔙 Pressione ENTER para tentar novamente...")
            continue
        
        # Verifica dependências Python
        deps_ok, deps_msg = verificar_python()
        if not deps_ok:
            print(f"❌ ERRO: {deps_msg}")
            print("💡 Execute: pip install -r requirements.txt")
            input("🔙 Pressione ENTER para continuar mesmo assim...")
        else:
            print(f"✅ {deps_msg}")
        
        # Mostra menu e processa escolha
        escolha = menu_principal()
        
        if escolha == '0':
            print("\n👋 Obrigado por usar o Contador de Pessoas!")
            print("🚀 Volte sempre que precisar contar pessoas com IA! 🚀")
            break
            
        elif escolha == '1':
            executar_comando("contador_pessoas.py", "Iniciando Contador Completo")
            
        elif escolha == '2':
            executar_comando("contador_simples.py", "Iniciando Contador Simples")
            
        elif escolha == '3':
            executar_comando("teste_video.py", "Iniciando Teste Rápido")
            
        elif escolha == '4':
            print("\n⚠️ ATENÇÃO: O treinamento pode demorar várias horas!")
            confirma = input("Tem certeza que quer continuar? (s/N): ").lower()
            if confirma in ['s', 'sim', 'yes', 'y']:
                executar_comando("treinar_yolo.py", "Iniciando Treinamento do Modelo")
            else:
                print("❌ Treinamento cancelado.")
                input("🔙 Pressione ENTER para voltar...")
                
        elif escolha == '5':
            limpar_tela()
            mostrar_ajuda()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Saindo do programa...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("🔙 Pressione ENTER para sair...")
        sys.exit(1)

@echo off
echo ========================================
echo    CONTADOR DE PESSOAS - INICIALIZAR
echo ========================================
echo.

REM Muda para o diretório do projeto
cd /d "C:\Users\Pichau\Desktop\Faculdade Materias\Trabalho Yan\person counting.v1i.yolov8"

echo 📁 Diretório atual: %CD%
echo.

echo 🔍 Verificando arquivos necessários...
if exist "contador_pessoas.py" (
    echo ✅ contador_pessoas.py encontrado
) else (
    echo ❌ contador_pessoas.py NÃO encontrado!
    pause
    exit
)

if exist "yolov8n.pt" (
    echo ✅ Modelo YOLO encontrado
) else (
    echo ⚠️ Modelo yolov8n.pt não encontrado, mas pode usar modelo treinado
)

echo.
echo 🚀 Iniciando contador de pessoas...
echo 💡 Pressione Ctrl+C para sair a qualquer momento
echo.

REM Executa o contador
python contador_pessoas.py

echo.
echo 👋 Contador finalizado!
pause

#!/bin/bash

# Atualiza os pacotes do Termux
pkg update -y

# Instala as dependências necessárias
pkg install -y git python

# Clona o repositório do GitHub
git clone https://github.com/MrPythonBrasil/btc.git

# Entra na pasta do projeto
cd btc

# Instala as dependências do Python
pip install -r requirements.txt

# Dá permissão de execução ao script principal
chmod +x btc.py

# Mensagem final
echo "Instalação concluída! Para executar o script, use:"
echo "python btc.py"

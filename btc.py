import random
import string
from colorama import Fore, Style, init
import time
import threading
import requests

# Inicializa o colorama para funcionar no Windows também
init(autoreset=True)

# Configurações do webhook do Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1346604669568286781/Wb5rjHvW9vmCPlMcWDwQ89nShkg8E8SwAF7w35fWq-jkTS768zXo1ROQUFov8LnMCzKX"

# Título em ASCII art
TITULO = """
 /$$$$$$$  /$$$$$$ /$$$$$$$$ /$$$$$$   /$$$$$$  /$$$$$$ /$$   /$$
| $$__  $$|_  $$_/|__  $$__//$$__  $$ /$$__  $$|_  $$_/| $$$ | $$
| $$  \ $$  | $$     | $$  | $$  \__/| $$  \ $$  | $$  | $$$$| $$
| $$$$$$$   | $$     | $$  | $$      | $$  | $$  | $$  | $$ $$ $$
| $$__  $$  | $$     | $$  | $$      | $$  | $$  | $$  | $$  $$$$
| $$  \ $$  | $$     | $$  | $$    $$| $$  | $$  | $$  | $$\  $$$
| $$$$$$$/ /$$$$$$   | $$  |  $$$$$$/|  $$$$$$/ /$$$$$$| $$ \  $$
|_______/ |______/   |__/   \______/  \______/ |______/|__/  \__/
                                                                 
                                                                 
"""

def gerar_endereco_falso():
    """Gera um endereço falso de Bitcoin (uma string aleatória)."""
    caracteres = string.ascii_letters + string.digits
    endereco = ''.join(random.choice(caracteres) for _ in range(34))
    return endereco

def buscar_cotacao_bitcoin():
    """Busca a cotação atual do Bitcoin em USD usando a API do CoinGecko."""
    try:
        resposta = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados["bitcoin"]["usd"]
    except Exception as e:
        print(Fore.RED + f"Erro ao buscar cotação do Bitcoin: {e}")
        return None

def enviar_webhook(mensagem):
    """Envia uma mensagem para o webhook do Discord."""
    try:
        dados = {"content": mensagem}
        resposta = requests.post(WEBHOOK_URL, json=dados)
        resposta.raise_for_status()
    except Exception as e:
        print(Fore.RED + f"Erro ao enviar mensagem para o Discord: {e}")

def simular_mineracao():
    """Simula a mineração de Bitcoins falsos."""
    print(Fore.YELLOW + TITULO)
    print(Fore.YELLOW + "Iniciando mineração de Bitcoins falsos...")
    print(Fore.YELLOW + "Digite 'parar' e pressione Enter para encerrar.")
    
    quantidade_bitcoins = 0
    valor_total = 0.0

    while True:
        endereco = gerar_endereco_falso()

        # Probabilidades variadas para geração de Bitcoins
        probabilidade = random.random()
        if probabilidade < 0.0001:  # 0,01% de chance para 1 Bitcoin
            quantidade = 1.0
        elif probabilidade < 0.001:  # 0,1% de chance para 0,1 Bitcoin
            quantidade = 0.1
        elif probabilidade < 0.01:  # 1% de chance para 0,01 Bitcoin
            quantidade = 0.01
        else:
            quantidade = 0.0

        if quantidade > 0:
            cotacao_bitcoin = buscar_cotacao_bitcoin()
            if cotacao_bitcoin:
                quantidade_bitcoins += quantidade
                valor_total += quantidade * cotacao_bitcoin
                mensagem = (
                    f"```diff\n"
                    f"+ Endereço minerado: {endereco} | Parabéns! Você ganhou {quantidade:.2f} BTC!\n"
                    f"+ Quantidade de Bitcoins: {quantidade_bitcoins:.2f} | Valor Total: ${valor_total:.2f}\n"
                    f"```"
                )
                print(Fore.GREEN + f"Endereço minerado: {endereco} | Parabéns! Você ganhou {quantidade:.2f} BTC!")
                print(Fore.GREEN + f"Quantidade de Bitcoins: {quantidade_bitcoins:.2f} | Valor Total: ${valor_total:.2f}")
                enviar_webhook(mensagem)
            else:
                mensagem = f"```fix\nEndereço minerado: {endereco} | Erro ao buscar cotação do Bitcoin.\n```"
                print(Fore.RED + f"Endereço minerado: {endereco} | Erro ao buscar cotação do Bitcoin.")
                enviar_webhook(mensagem)
        else:
            mensagem = f"```diff\n- Endereço minerado: {endereco} | Nenhum BTC encontrado neste bloco.\n```"
            print(Fore.RED + f"Endereço minerado: {endereco} | Nenhum BTC encontrado neste bloco.")
            enviar_webhook(mensagem)

        # Intervalo de 0.1 segundos
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        # Inicia a mineração em uma thread separada
        mineracao_thread = threading.Thread(target=simular_mineracao)
        mineracao_thread.daemon = True  # Permite que o programa termine mesmo com a thread rodando
        mineracao_thread.start()

        # Espera o usuário digitar 'parar'
        input()  # Quando o usuário digitar algo e pressionar Enter, o programa termina
        print(Fore.YELLOW + "\nMineração encerrada pelo usuário. Até mais!")
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nMineração interrompida pelo usuário. Até mais!")

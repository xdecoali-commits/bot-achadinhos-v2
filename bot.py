import os
import time
import threading
import requests
import telebot
from http.server import HTTPServer, BaseHTTPRequestHandler

# === CONFIGURAÇÃO DO BOT ===
# Certifique-se de colhar o Token ATUAL do BotFather para evitar o Erro 401
TOKEN = '9087207118:AAFQADdCvNmW-dQsrj5_zNchvq4Wt9rX3AY'
CHAT_ID = '@achadinhosggg'

# === SEUS PARÂMETROS E TAGS REAIS DE AFILIADO ===
AMAZON_TAG = "achadinhoamz01-20"   # Sua tag real da Amazon
SHOPEE_SUB_ID = "casapraticaabc"   # Seu SubID da Shopee
MELI_TOOL_ID = "xdecosantos"      # Seu ID/Tag do Mercado Livre

bot = telebot.TeleBot(TOKEN)

# Servidor HTTP para manter o Render ativo no Cron-Job.org
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot Achadinhos OK 24/7")
    def log_message(self, format, *args):
        return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# === CONVERSORES DE LINK PARA PRODUTOS DIRETOS ===

def converter_amazon(url):
    connector = "&" if "?" in url else "?"
    return f"{url}{connector}tag={AMAZON_TAG}"

def converter_mercadolivre(url):
    connector = "&" if "?" in url else "?"
    return f"{url}{connector}matt_tool={MELI_TOOL_ID}"

def converter_shopee(url):
    connector = "&" if "?" in url else "?"
    return f"{url}{connector}sub_id={SHOPEE_SUB_ID}"

# === OFERTAS COM LINKS DIRETOS E TAGS CONFIGURADAS ===

def obter_produtos():
    return [
        {
            'loja': 'Amazon 📦',
            'titulo': 'Echo Dot 5ª Geração com Alexa | Som de Alta Qualidade',
            'preco': 'R$ 379,00',
            'link': converter_amazon('https://www.amazon.com.br/dp/B09B23V213'),
            'imagem': 'https://m.media-amazon.com/images/I/71XO11Xw48L._AC_SL1000_.jpg'
        },
        {
            'loja': 'Mercado Livre 💛',
            'titulo': 'Fritadeira Sem Óleo Air Fryer Mondial 4L Inox',
            'preco': 'R$ 289,90',
            'link': converter_mercadolivre('https://www.mercadolivre.com.br/fritadeira-sem-oleo-air-fryer-mondial-afn-40-bi-4l-1500w-preto-inox/p/MLB19734123'),
            'imagem': 'https://http2.mlstatic.com/D_NQ_NP_630656-MLA74681602434_022024-O.jpg'
        },
        {
            'loja': 'Shopee 

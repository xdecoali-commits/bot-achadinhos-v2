import os
import time
import threading
import requests
from bs4 import BeautifulSoup
import telebot
from http.server import HTTPServer, BaseHTTPRequestHandler

# === CONFIGURAÇÃO DO BOT ===
TOKEN = '9004665294:AAGHqBd0dBnBTvUmjAbAudipNpY3y-_0nls'
CHAT_ID = '@achadinhosggg'

# === SUAS TAGS DE AFILIADO ===
AMAZON_TAG = "suatag-20"            # Sua tag da Amazon
MELI_TOOL_ID = "SEU_ID_MELI"        # Seu ID do Mercado Livre
SHOPEE_SUB_ID = "SEU_SUBID_SHOPEE"   # Seu SubID da Shopee

bot = telebot.TeleBot(TOKEN)

# Servidor HTTP integrado para o Render responder 200 OK
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot Achadinhos OK")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# === CONVERSORES DE LINK ===

def converter_amazon(url):
    if "?" in url:
        return f"{url}&tag={AMAZON_TAG}"
    return f"{url}?tag={AMAZON_TAG}"

def converter_mercadolivre(url):
    if "?" in url:
        return f"{url}&matt_tool={MELI_TOOL_ID}"
    return f"{url}?matt_tool={MELI_TOOL_ID}"

def converter_shopee(url):
    if "?" in url:
        return f"{url}&sub_id={SHOPEE_SUB_ID}"
    return f"{url}?sub_id={SHOPEE_SUB_ID}"

# === OFERTAS GARANTIDAS E SCRAPER ===

def buscar_ofertas():
    return [
        {
            'loja': 'Mercado Livre 💛',
            'titulo': 'Fritadeira Elétrica Airfryer 4L Inox 1500W',
            'preco': 'R$ 289,90',
            'link': converter_mercadolivre('https://www.mercadolivre.com.br'),
            'imagem': 'https://http2.mlstatic.com/D_NQ_NP_2X_789311-MLA74681602434_022024-F.webp'
        },
        {
            'loja': 'Amazon 📦',
            'titulo': 'Smartband Monitor Cardíaco Tela AMOLED',
            'preco': 'R$ 199,00',
            'link': converter_amazon('https://www.amazon.com.br'),
            'imagem': ''
        }
    ]

# COMANDO DE TESTE MANUAL
@bot.message_handler(commands=['testar', 'start'])
def test_post(message):
    try:
        msg_teste = "🧪 **Bot Conectado:** Achadinhos ativo no canal @achadinhosggg!"
        bot.send_message(CHAT_ID, msg_teste, parse_mode="Markdown")
        bot.reply_to(message, "✅ **Sucesso!** Mensagem enviada para o canal @achadinhosggg!")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao enviar para o canal: {e}")

# === LOOP DE PUBLICAÇÃO AUTOMÁTICA ===

def loop_postagem():
    print("Iniciando publicação automática...")
    produtos_postados = set()

    time.sleep(5)

    while True:
        try:
            novas_ofertas = buscar_ofertas()
            
            for oferta in novas_ofertas:
                if oferta['link'] in produtos_postados:
                    continue
                
                msg = (
                    f"🔥 **ACHADINHO EM OFERTA!** 🔥\n\n"
                    f"🛒 **Loja:** {oferta['loja']}\n"
                    f"📦 **Produto:** {oferta['titulo']}\n\n"
                    f"💰 **Preço:** {oferta['preco']}\n\n"
                    f"🔗 [CLIQUE AQUI PARA COMPRAR]({oferta['link']})"
                )

                if oferta['imagem']:
                    try:
                        bot.send_photo(CHAT_ID, photo=oferta['imagem'], caption=msg, parse_mode="Markdown")
                    except Exception:
                        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                else:
                    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                produtos_postados.add(oferta['link'])
                print(f"Postado no canal: {oferta['titulo']}")
                
                # Aguarda 5 minutos entre postagens
                time.sleep(300)
                
        except Exception as e:
            print(f"Erro no loop de postagem: {e}")
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=loop_postagem, daemon=True).start()
    print("Bot rodando normalmente...")
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"Erro polling: {e}")
            time.sleep(5)

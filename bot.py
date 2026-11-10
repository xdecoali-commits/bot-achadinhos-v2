import os
import time
import threading
import requests
import telebot
from http.server import HTTPServer, BaseHTTPRequestHandler

# === CONFIGURAÇÃO DO BOT ===
TOKEN = '9004665294:AAHoXtYoJn18YKB8T9rRj9hhjGK-sCmjiLM'
CHAT_ID = '@achadinhosggg'

# === SEUS LINKS E TAGS REAIS DE AFILIADO ===
AMAZON_SHORT_LINK = "https://a.co/d/0jePnojI"
SHOPEE_SUB_ID = "casapraticaabc"
MELI_TOOL_ID = "xdecosantos"

bot = telebot.TeleBot(TOKEN)

# Servidor HTTP com porta flexível para o Render
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

# === CONVERSORES DE LINK ===

def converter_amazon(url):
    return AMAZON_SHORT_LINK

def converter_mercadolivre(url):
    connector = "&" if "?" in url else "?"
    return f"{url}{connector}matt_tool={MELI_TOOL_ID}"

def converter_shopee(url):
    connector = "&" if "?" in url else "?"
    return f"{url}{connector}sub_id={SHOPEE_SUB_ID}"

# === LISTA DE OFERTAS ===

def obter_produtos():
    return [
        {
            'loja': 'Mercado Livre 💛',
            'titulo': 'Fritadeira Sem Óleo Air Fryer Mondial 4L Inox',
            'preco': 'R$ 289,90',
            'link': converter_mercadolivre('https://www.mercadolivre.com.br/fritadeira-sem-oleo-air-fryer-mondial-afn-40-bi-4l-1500w-preto-inox/p/MLB19734123'),
            'imagem': 'https://http2.mlstatic.com/D_NQ_NP_630656-MLA74681602434_022024-O.jpg'
        },
        {
            'loja': 'Amazon 📦',
            'titulo': 'Echo Dot 5ª Geração com Alexa | Som de alta qualidade',
            'preco': 'R$ 379,00',
            'link': converter_amazon('https://www.amazon.com.br/dp/B09B23V213'),
            'imagem': 'https://m.media-amazon.com/images/I/71XO11Xw48L._AC_SL1000_.jpg'
        }
    ]

# COMANDO DE TESTE MANUAL
@bot.message_handler(commands=['testar', 'start'])
def test_post(message):
    try:
        msg_teste = "<b>🧪 Bot de Achadinhos Conectado!</b>\n\nSistema rodando 24/7 no canal @achadinhosggg!"
        bot.send_message(CHAT_ID, msg_teste, parse_mode="HTML")
        bot.reply_to(message, "✅ <b>Sucesso!</b> Mensagem enviada para o canal @achadinhosggg.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao enviar: {e}")

# === LOOP DE PUBLICAÇÃO AUTOMÁTICA ===

def loop_postagem():
    print("Iniciando publicação automática...")
    time.sleep(3)
    
    produtos = obter_produtos()
    idx = 0

    while True:
        try:
            oferta = produtos[idx % len(produtos)]
            
            msg = (
                f"🔥 <b>ACHADINHO EM OFERTA!</b> 🔥\n\n"
                f"🛒 <b>Loja:</b> {oferta['loja']}\n"
                f"📦 <b>Produto:</b> {oferta['titulo']}\n\n"
                f"💰 <b>Preço:</b> {oferta['preco']}\n\n"
                f"🔗 <a href='{oferta['link']}'>CLIQUE AQUI PARA COMPRAR</a>"
            )

            if oferta['imagem']:
                try:
                    bot.send_photo(CHAT_ID, photo=oferta['imagem'], caption=msg, parse_mode="HTML")
                except Exception:
                    bot.send_message(CHAT_ID, msg, parse_mode="HTML")
            else:
                bot.send_message(CHAT_ID, msg, parse_mode="HTML")

            idx += 1
            time.sleep(300) # Publica a cada 5 minutos

        except Exception as e:
            print(f"Erro no loop: {e}")
            time.sleep(30)

# Inicialização limpa
if __name__ == "__main__":
    # Limpa Webhooks antigos do Telegram para liberar a conexão
    try:
        bot.remove_webhook()
        time.sleep(1)
    except Exception:
        pass

    threading.Thread(target=loop_postagem, daemon=True).start()
    
    # Polling sem travamento
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

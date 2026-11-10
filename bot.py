import os
import time
import threading
import requests
import telebot
from http.server import HTTPServer, BaseHTTPRequestHandler

# === CONFIGURAÇÃO DO BOT ===
# Importante: mantenha o seu Token ativo do BotFather aqui
TOKEN = '9004665294:AAEcrA5iFfg7za9-UP6yhZzEfYoUHIpQY7o'
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

# === CONVERSORES DE LINK COM FORMATAÇÃO PERFEITA ===

def converter_amazon(url):
    # Se a URL já tiver ?, usa &, senão usa ?
    clean_url = url.split('?')[0]
    return f"{clean_url}?tag={AMAZON_TAG}"

def converter_mercadolivre(url):
    clean_url = url.split('?')[0]
    return f"{clean_url}?matt_tool={MELI_TOOL_ID}"

def converter_shopee(url):
    clean_url = url.split('?')[0]
    return f"{clean_url}?sub_id={SHOPEE_SUB_ID}"

# === OFERTAS COM LINKS PERFEITOS E IMAGENS DIRETA ===

def obter_produtos():
    return [
        {
            'loja': 'Amazon 📦',
            'titulo': 'Echo Dot 5ª Geração com Alexa',
            'preco': 'R$ 379,00',
            'link': converter_amazon('https://www.amazon.com.br/dp/B09B23V213'),
            'imagem': 'https://m.media-amazon.com/images/I/71XO11Xw48L._AC_SL1500_.jpg'
        },
        {
            'loja': 'Mercado Livre 💛',
            'titulo': 'Fritadeira Sem Óleo Air Fryer Mondial 4L Inox',
            'preco': 'R$ 289,90',
            'link': converter_mercadolivre('https://www.mercadolivre.com.br/fritadeira-sem-oleo-air-fryer-mondial-afn-40-bi-4l-1500w-preto-inox/p/MLB19734123'),
            'imagem': 'https://http2.mlstatic.com/D_NQ_NP_908386-MLU78988622765_092024-O.jpg'
        }
    ]

# COMANDO DE TESTE MANUAL
@bot.message_handler(commands=['testar', 'start'])
def test_post(message):
    try:
        msg_teste = "<b>🧪 Bot de Achadinhos Conectado!</b>\n\nLinks de produtos e imagens formatados com sucesso!"
        bot.send_message(CHAT_ID, msg_teste, parse_mode="HTML")
        bot.reply_to(message, "✅ <b>Sucesso!</b> Mensagem enviada para o canal @achadinhosggg.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao enviar: {e}")

# === LOOP DE PUBLICAÇÃO AUTOMÁTICA ===

def loop_postagem():
    print("Iniciando publicação automática de produtos...")
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
                except Exception as err:
                    print(f"Erro imagem: {err}")
                    bot.send_message(CHAT_ID, msg, parse_mode="HTML")
            else:
                bot.send_message(CHAT_ID, msg, parse_mode="HTML")

            idx += 1
            time.sleep(300)

        except Exception as e:
            print(f"Erro no loop: {e}")
            time.sleep(30)

if __name__ == "__main__":
    try:
        bot.remove_webhook()
        time.sleep(1)
    except Exception:
        pass

    threading.Thread(target=loop_postagem, daemon=True).start()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

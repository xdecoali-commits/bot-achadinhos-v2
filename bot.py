import os
import time
import threading
import requests
import telebot
from http.server import HTTPServer, BaseHTTPRequestHandler

# === CONFIGURAÇÃO DO BOT ===
TOKEN = '9087207118:AAFQADdCvNmW-dQsrj5_zNchvq4Wt9rX3AY'
CHAT_ID = '@achadinhosggg'

# === SEUS LINKS E TAGS REAIS DE AFILIADO ===
AMAZON_SHORT_LINK = "https://a.co/d/0jePnojI"
SHOPEE_SUB_ID = "casapraticaabc"
MELI_TOOL_ID = "xdecosantos"

bot = telebot.TeleBot(TOKEN)

# Servidor HTTP para responder 200 OK ao Cron-Job.org
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot Achadinhos OK 24/7")

def run_server():
    port = int(os.environ.get("PORT", 8080))
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

# === LISTA DINÂMICA DE PRODUTOS ===

def obter_produtos_para_envio():
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
        },
        {
            'loja': 'Shopee 🧡',
            'titulo': 'Achadinhos Casa Prática ABC & Utilidades Domésticas',
            'preco': 'Confira os Descontos',
            'link': converter_shopee('https://shopee.com.br'),
            'imagem': ''
        }
    ]

# COMANDO DE TESTE MANUAL
@bot.message_handler(commands=['testar', 'start'])
def test_post(message):
    try:
        msg_teste = "<b>🧪 Bot de Achadinhos 24/7 no Ar!</b>\n\nSistema conectado com sucesso ao canal @achadinhosggg."
        bot.send_message(CHAT_ID, msg_teste, parse_mode="HTML")
        bot.reply_to(message, "✅ <b>Teste Ok!</b> Mensagem enviada para o canal @achadinhosggg.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao enviar para o canal: {e}")

# === LOOP CONTINUO DE PUBLICAÇÃO 24/7 ===

def loop_postagem():
    print("Iniciando publicação automática continua...")
    time.sleep(5)
    
    produtos = obter_produtos_para_envio()
    indice = 0

    while True:
        try:
            oferta = produtos[indice % len(produtos)]
            
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
                    print(f"[{time.strftime('%H:%M:%S')}] Enviada foto + oferta: {oferta['titulo']}")
                except Exception as err_img:
                    print(f"Erro ao enviar foto ({err_img}), enviando texto...")
                    bot.send_message(CHAT_ID, msg, parse_mode="HTML")
            else:
                bot.send_message(CHAT_ID, msg, parse_mode="HTML")
                print(f"[{time.strftime('%H:%M:%S')}] Enviada oferta em texto: {oferta['titulo']}")

            indice += 1

            # Aguarda 5 minutos (300 segundos) até a próxima postagem
            time.sleep(300)

        except Exception as e:
            print(f"Erro na publicação: {e}")
            time.sleep(30)

if __name__ == "__main__":
    # Inicia o loop de postagens automáticas numa thread dedicada
    threading.Thread(target=loop_postagem, daemon=True).start()
    print("Bot rodando 24/7...")

    # Polling infinito com reconexão automática
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=90)
        except Exception as e:
            print(f"Erro polling: {e}")
            time.sleep(10)

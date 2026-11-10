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

# Servidor HTTP para manter o Render ativo
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
    return AMAZON_SHORT_LINK

def converter_mercadolivre(url):
    connector = "&" if "?" in url else "?"
    return f"{url}{connector}matt_tool={MELI_TOOL_ID}"

def converter_shopee(url):
    connector = "&" if "?" in url else "?"
    return f"{url}{connector}sub_id={SHOPEE_SUB_ID}"

# === LISTA DE OFERTAS PARA ENVIO ===

def buscar_ofertas():
    # Geramos um parâmetro dinâmico para garantir que o bot poste sem ignorar por repetição
    t = int(time.time())
    return [
        {
            'loja': 'Mercado Livre 💛',
            'titulo': 'Fritadeira Sem Óleo Air Fryer Mondial 4L Inox',
            'preco': 'R$ 289,90',
            'link': converter_mercadolivre(f'https://www.mercadolivre.com.br/p/MLB19734123?v={t}'),
            'imagem': 'https://http2.mlstatic.com/D_NQ_NP_630656-MLA74681602434_022024-O.jpg'
        },
        {
            'loja': 'Amazon 📦',
            'titulo': 'Echo Dot 5ª Geração com Alexa',
            'preco': 'R$ 379,00',
            'link': converter_amazon('https://www.amazon.com.br'),
            'imagem': 'https://m.media-amazon.com/images/I/71XO11Xw48L._AC_SL1000_.jpg'
        }
    ]

# COMANDO DE TESTE MANUAL
@bot.message_handler(commands=['testar', 'start'])
def test_post(message):
    try:
        msg_teste = "<b>🧪 Bot de Achadinhos Conectado!</b>\n\nLinks diretos e foto configurados para o canal @achadinhosggg!"
        bot.send_message(CHAT_ID, msg_teste, parse_mode="HTML")
        bot.reply_to(message, "✅ <b>Teste Ok!</b> Mensagem enviada para o canal @achadinhosggg.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao enviar: {e}")

# === LOOP DE PUBLICAÇÃO AUTOMÁTICA ===

def loop_postagem():
    print("Iniciando loop de publicação...")
    time.sleep(2)

    while True:
        try:
            novas_ofertas = buscar_ofertas()
            
            for oferta in novas_ofertas:
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
                        print(f"Foto e mensagem postadas: {oferta['titulo']}")
                    except Exception as err_img:
                        print(f"Erro foto, enviando apenas texto: {err_img}")
                        bot.send_message(CHAT_ID, msg, parse_mode="HTML")
                else:
                    bot.send_message(CHAT_ID, msg, parse_mode="HTML")
                    print(f"Mensagem enviada: {oferta['titulo']}")
                
                # Aguarda 5 minutos entre postagens
                time.sleep(300)
                
        except Exception as e:
            print(f"Erro no loop de postagem: {e}")
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=loop_postagem, daemon=True).start()
    print("Bot rodando...")
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"Erro polling: {e}")
            time.sleep(5)

import os
import time
import threading
import requests
from bs4 import BeautifulSoup
import telebot
from http.server import HTTPServer, BaseHTTPRequestHandler

# === CONFIGURAÇÃO DO BOT ===
TOKEN = '9087207118:AAFQADdCvNmW-dQsrj5_zNchvq4Wt9rX3AY'
CHAT_ID = '@achadinhosggg'

# === SEUS LINKS E TAGS REAIS DE AFILIADO ===
AMAZON_SHORT_LINK = "https://a.co/d/0jePnojI"
SHOPEE_SUB_ID = "casapraticaabc"
MELI_SOCIAL_PROFILE = "xdecosantos"

bot = telebot.TeleBot(TOKEN)

# Servidor HTTP para manter o Render acordado
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

# === CONVERSORES DE LINK PERSONALIZADOS ===

def converter_amazon(url):
    # Retorna o link curto de afiliado ou injeta o parâmetro se for URL longa
    if "a.co" in url or "amazon.com" in url:
        return AMAZON_SHORT_LINK
    return url

def converter_mercadolivre(url):
    # Se for link de produto, redireciona para a vitrine social do perfil no Mercado Livre
    if "mercadolivre.com.br" in url:
        return f"https://www.mercadolivre.com.br/social/{MELI_SOCIAL_PROFILE}"
    return url

def converter_shopee(url):
    connector = "&" if "?" in url else "?"
    return f"{url}{connector}sub_id={SHOPEE_SUB_ID}"

# === BUSCA DE OFERTAS DA VITRINE E AFILIADOS ===

def buscar_ofertas():
    return [
        {
            'loja': 'Mercado Livre 💛 (Vitrine @xdecosantos)',
            'titulo': 'Fritadeira Sem Óleo Air Fryer Mondial 4L Inox',
            'preco': 'R$ 289,90',
            'link': converter_mercadolivre('https://www.mercadolivre.com.br/p/MLB19734123'),
            'imagem': 'https://http2.mlstatic.com/D_NQ_NP_630656-MLA74681602434_022024-O.jpg'
        },
        {
            'loja': 'Amazon 📦',
            'titulo': 'Oferta Especial Selecionada Amazon',
            'preco': 'Confira o Preço Exclusivo',
            'link': converter_amazon('https://www.amazon.com.br'),
            'imagem': 'https://m.media-amazon.com/images/I/71XO11Xw48L._AC_SL1000_.jpg'
        },
        {
            'loja': 'Shopee 🧡 (Casa Prática ABC)',
            'titulo': 'Utilidades Domésticas & Achadinhos Casa Prática',
            'preco': 'Menor Preço Garantido',
            'link': converter_shopee('https://shopee.com.br'),
            'imagem': ''
        }
    ]

# COMANDO DE TESTE MANUAL
@bot.message_handler(commands=['testar', 'start'])
def test_post(message):
    try:
        msg_teste = "🧪 **Bot de Achadinhos Conectado!**\n\nTodos os links de afiliados configurados para:\n- Mercado Livre: @xdecosantos\n- Shopee: casapraticaabc\n- Amazon: a.co/d/0jePnojI"
        bot.send_message(CHAT_ID, msg_teste, parse_mode="Markdown")
        bot.reply_to(message, "✅ **Teste Ok!** Mensagem enviada para o canal @achadinhosggg.")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao enviar: {e}")

# === LOOP DE PUBLICAÇÃO AUTOMÁTICA ===

def loop_postagem():
    print("Iniciando publicação automática de achadinhos com os seus links...")
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
                    except Exception as err_img:
                        print(f"Erro ao enviar foto: {err_img}")
                        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                else:
                    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                produtos_postados.add(oferta['link'])
                print(f"Postado no canal: {oferta['titulo']}")
                
                # Publica uma oferta a cada 5 minutos
                time.sleep(300)
                
        except Exception as e:
            print(f"Erro no loop de postagem: {e}")
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=loop_postagem, daemon=True).start()
    print("Bot Achadinhos ativo e configurado com seus links...")
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"Erro polling: {e}")
            time.sleep(5)

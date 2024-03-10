import telebot
import wikipediaapi

API_TOKEN = '6694896297:AAHtDtk2-rtvW8G4uI7gLQAvvN56KU1ccVc'  
bot = telebot.TeleBot(API_TOKEN)

wiki_wiki = wikipediaapi.Wikipedia(
    language='pt',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='MeuBot/1.0 (https://github.com/seu_usuario/seu_repositorio)'
)

search_results = {}  # Dicionário para armazenar resultados de pesquisa por chat_id

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bem-vindo ao Bot Dona Cida da Wikipedia! Digite /search seguido do termo que deseja pesquisar.")

@bot.message_handler(commands=['search'])
def search_wikipedia(message):
    search_query = message.text.split('/search ', 1)[1]
    try:
        page = wiki_wiki.page(search_query)
        if page.exists():
            result = page.summary[:1000] + '...' if len(page.summary) > 1000 else page.summary
            search_results[message.chat.id] = {'query': search_query, 'result': result}
            bot.reply_to(message, result)
        else:
            bot.reply_to(message, "Nenhum resultado encontrado para esta pesquisa.")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Ocorreu um erro ao processar sua pesquisa.")

@bot.message_handler(commands=['mais'])
def more_info(message):
    chat_id = message.chat.id
    if chat_id in search_results:
        search_query = search_results[chat_id]['query']
        try:
            page = wiki_wiki.page(search_query)
            if page.exists():
                result = page.summary
                bot.reply_to(message, result)
            else:
                bot.reply_to(message, "Nenhum resultado encontrado para esta pesquisa.")
        except Exception as e:
            print(e)
            bot.reply_to(message, "Ocorreu um erro ao processar sua pesquisa.")
    else:
        bot.reply_to(message, "Não há resultados anteriores para mostrar. Por favor, faça uma nova pesquisa usando /search.")

bot.polling()

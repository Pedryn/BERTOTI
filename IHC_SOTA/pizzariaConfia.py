import telebot
import re

API_TOKEN = '6694896297:AAHtDtk2-rtvW8G4uI7gLQAvvN56KU1ccVc' 
bot = telebot.TeleBot(API_TOKEN)

pizzas_disponiveis = {
    "calabresa": "Calabresa - R$ 30.00",
    "margherita": "Margherita - R$ 25.00",
    "portuguesa": "Portuguesa - R$ 35.00",
    "frango catupiry":"Frango Catupiry - R$ 27.99",
    "calzone": "Calzone - R$ 32.50",
    "4 queijos": "4 Queijos - R$ 24.99",
    "peperoni": "Peperoni - R$ 33.50",
    "mussarela": "Mussarela - R$ 22.00",
    "strogonoff": "Strogonoff - R$ 35.00",
    "chocolate": "Chocolate - R$ 35.00"
}

@bot.message_handler(commands=['start'])
def iniciar_pedido(message):
    bot.send_message(message.chat.id, "Olá! Bem-vindo à Pizzaria Confia! Deseja pedir uma pizza?")
    texto_opcoes = "Temos as seguintes opções:\n\n"
    for nome, descricao in pizzas_disponiveis.items():
        texto_opcoes += f"- {descricao}\n"
    texto_opcoes += "\nQual você deseja?"
    bot.send_message(message.chat.id, texto_opcoes)

@bot.message_handler(func=lambda message: message.text.lower().startswith(("quero", "uma", "duas", "três")))
def processar_pedido(message):
    texto_pedido = message.text.lower()
    pizzas_pedidas = {}  # Usamos um dicionário para armazenar as pizzas e suas quantidades
    valor_total = 0

    # Busca por quantidade e nome da pizza
    for nome_pizza in pizzas_disponiveis:
        padrao = rf"\b(\d+)?\s*(pizza(s)? de )?{nome_pizza}\b"
        ocorrencias = re.findall(padrao, texto_pedido)
        for quantidade, _, _ in ocorrencias:
            quantidade = int(quantidade) if quantidade else 1
            pizzas_pedidas[nome_pizza] = pizzas_pedidas.get(nome_pizza, 0) + quantidade  # Atualiza a quantidade no dicionário
            valor_total += quantidade * float(pizzas_disponiveis[nome_pizza].split(" - R$ ")[1])

    if not pizzas_pedidas:
        bot.send_message(message.chat.id, "Desculpe, não entendi seu pedido. Por favor, escolha uma pizza da lista.")
    else:
        texto_confirmacao = "Ok, você pediu:\n"
        for pizza, quantidade in pizzas_pedidas.items():
            texto_confirmacao += f"- {quantidade} {pizzas_disponiveis[pizza]}\n"  
        texto_confirmacao += f"\nTotal: R$ {valor_total:.2f}\nQual o endereço para entrega?"
        bot.send_message(message.chat.id, texto_confirmacao)


@bot.message_handler(func=lambda message: True)  # Capturar qualquer mensagem como endereço
def confirmar_pedido(message):
    endereco = message.text
    bot.send_message(message.chat.id, f"Pedido finalizado! Sua pizza será entregue em: {endereco}\nTempo de preparação: 30-40 minutos\nTempo de entrega: 20-30 minutos\nObrigado e volte sempre!")

print("Pizzaria Bot está online!")
bot.polling()
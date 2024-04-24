import sys, json, os
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel, PeerChat
from telethon import events

sys.stdout.reconfigure(encoding='utf-8')


def read_config(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        data = json.load(arquivo)
    return data

api = read_config('config.json')
api_id = api['api_id']
api_hash = api['api_hash']
group_id = api['group_id']
destiny_id = api['destiny_id']
last_message_id_file = api['last_message_id_file']

client = TelegramClient('session_name', api_id, api_hash)

def change_message(message):
    new_message = message.replace("📱 Clique aqui para fazer o cadastro", "📱 Crie seu cadastro aqui: \nhttps://bit.ly/FortuneTiger2Hack\n")
    new_message = new_message.replace("🎯 ENTRADA CONFIRMADA 🎯", "🎰 FALHA IDENTIFICADA 🎯")
    if message.find("🆘🆘 ATENÇÃO 🆘🆘") != -1:
        new_message = '''
🆘🆘 ATENÇÃO 🆘🆘

COMO JOGAR NO HACKER DO FORTUNE TIGER🐯

VOCÊS VÃO ENTRAR NO LINK ABAIXO SE CADASTRAR NA PLATAFORMA QUE O HACK OPERA

https://bit.ly/FortuneTiger2Hack

FAÇA UM DEPÓSITO DE R$ 30,00 OU MAIS 

APÓS CADASTRAR E DEPOSITAR VAI VOLTAR AQUI PRO TELEGRAM E ESPERAR O SINAL

APÓS ISSO VOCÊ IRA ENTRAR NO FORTUNE TIGER.

E SO SEGUIR AS CALL

CADASTRE-SE AGORA E COMECE A PEGAR OS GREEENS ✅✅✅

⚠️⚠️ NOSSOS SINAIS HACK SÓ FUNCIONAM NA BR4BET!

TEM PESSOAS APOSTANDO EM OUTRAS CASAS E TOMANDO RED!
        '''
    return new_message

async def forward_message(event):
    message = event.message
    message.text = change_message(message.text)
    await client.send_message(destiny_id, message)
    print("Nova mensagem encaminhada com sucesso!")

async def main():
    await client.start()
    entity = PeerChannel(group_id) if group_id < 0 else PeerChat(group_id)
    last_message_id = await load_last_message_id()

    @client.on(events.NewMessage(chats=[entity]))
    async def event_handler(event):
        message = event.message
        raw_text = message.raw_text
        print("Nova mensagem recebida:")
        print(f"ID da mensagem: {message.id}")
        print(f"Conteúdo da mensagem: {raw_text}")
        if message.id > last_message_id:
            # if message.media is None and message.text is not None:
            await forward_message(event)
            await update_last_message_id(message.id)

    await client.run_until_disconnected()

async def load_last_message_id():
    if os.path.exists(last_message_id_file):
        with open(last_message_id_file, "r") as file:
            data = json.load(file)
            return data.get("last_message_id", 0)
    else:
        return 0

async def update_last_message_id(last_id):
    data = {"last_message_id": last_id}
    with open(last_message_id_file, "w") as file:
        json.dump(data, file)

if __name__ == "__main__":
    client.loop.run_until_complete(main())

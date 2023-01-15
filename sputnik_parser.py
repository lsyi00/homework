import configparser
import csv

from telethon.sync import TelegramClient
from datetime import datetime
from telethon.tl.functions.messages import GetHistoryRequest

async def parser(channel):
    messages = []
    offset_id = 0
    limit = 50 # кол-во сообщений, сохраняющихся за каждый цикл работы
    limit_count_messages = 0 # кол-во сообщений для парсинга (0 - без ограничений)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        hist_messages = history.messages
        for msg in hist_messages:
            messages.append(msg.to_dict())

        count_messages = len(messages) # счетчик числа спарсенных сообщений
        offset_id = hist_messages[len(hist_messages) - 1].id

        if limit_count_messages != 0 and count_messages >= limit_count_messages:
            break

        with open('messages.csv', 'w', newline='', encoding='utf-8') as file_msg:
            writer = csv.writer(file_msg, delimiter=',')
            for msg in messages:
                try:
                    writer.writerow([msg["date"], msg["message"]])
                except:
                    pass # если сообщения отсутстуют

with open("user_data.txt") as f:
    lines = f.readlines()
    lines = [line.rstrip() for line in lines]
    api_id = int(lines[0].split(" ")[2])
    api_hash = lines[1].split(" ")[2]
    phone = lines[2].split(" ")[2]

client = TelegramClient(phone, api_id, api_hash)
client.start()


async def main():
    url = "https://t.me/Sputnik_results"
    channel = await client.get_entity(url)
    await parser(channel)

with client:
    client.loop.run_until_complete(main())
import discord

async def send_paginated_message(channel, api_content):
    max_chars = 2000
    start = 0
    text = api_content
    while start < len(text):
        end = start + max_chars
        if end > len(text):
            end = len(text)
        chunk = text[start:end]
        chunk = chunk.replace('/', '\/')
        chunk = chunk.replace('>', '\>')
        await channel.send(chunk)
        start = end
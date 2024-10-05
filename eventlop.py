import asyncio

# Mevcut event loop'ı kapatma
for task in asyncio.all_tasks():
    task.cancel()

# Event loop'ı temizleme
loop = asyncio.get_event_loop()
loop.stop()
loop.close()

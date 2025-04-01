import asyncio

async def greet(name):
    print(f'Hi, {name}!');
    for step in range(1,5):
        print(f'{step}, {name}...')
        await asyncio.sleep(1)
    print(f'How are you going, {name}')

async def main():
    tasks = [greet('Ivan'), greet('Peter'), greet('Boss')]
    await asyncio.gather(*tasks)

asyncio.run(main())
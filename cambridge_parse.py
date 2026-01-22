import asyncio
from patchright.async_api import async_playwright

async def run_async_automation():
    async with async_playwright() as p:
        # Запускаємо браузер
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            # 1. Перехід на сайт
            await page.goto("https://dictionary.cambridge.org/dictionary/")
            print("Перейшли на сайт")
            
            # 2. Використання локатора для пошуку посилання
            await page.locator('xpath=/html/body/header/div/div[1]/nav/ul/li[5]/a/span[1]').click()
    
            print("Клікнули на посилання через локатор")
            
            # 3. Очікування заголовка з використанням локатора
            print("logginnn")
            
            print("клікнули на словник Тепер логінився у фейсбук")
            await asyncio.sleep(80)
            print("зараз перейдемо")
            await page.goto('https://dictionary.cambridge.org/plus/wordlist/160851659_real_world')
            async def scroll_to_bottom():
                prev_height = 0
                while True:
                    # Прокручуємо до низу
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await asyncio.sleep(5)  # Чекаємо завантаження
                    
                    # Отримуємо поточну висоту сторінки
                    current_height = await page.evaluate("document.body.scrollHeight")
                    
                    # Якщо висота не змінилась - виходимо
                    if current_height == prev_height:
                        break
                    
                    prev_height = current_height
            
            # Прокручуємо до низу, щоб завантажити всі слова
            await scroll_to_bottom()
        
            
            await asyncio.sleep(10)
            await page.locator('xpath=/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[5]/ul').wait_for()
            items = await page.locator('li.wordlistentry-row').all()
            results = []

            for ind,item in enumerate(items):
                print(f"element number {ind}")
                try:
                    # 1. Посилання з <a>
                    link = await item.locator('a.tb[href]').get_attribute('href')
                    
                    # 2. Текст з span.phrase.haxa.lmr-10
                    phrase = await item.locator('span.phrase.haxa.lmr-10').text_content()
                    
                    # 3. Текст з span.pos.fs14.ti
                    pos = await item.locator('span.pos.fs14.ti').text_content()
                    
                    # 4. Текст з div.def.fs16.fs18-s.fs19-m.lmb-10
                    definition = await item.locator('div.def.fs16.fs18-s.fs19-m.lmb-10').text_content()
                    
                    results.append({
                        'link': link,
                        'phrase': phrase.strip() if phrase else None,
                        'part_of_speech': pos.strip() if pos else None,
                        'definition': definition.strip() if definition else None
                    })
                    
                except Exception as e:
                    print(f"Помилка при парсингу елемента: {e}")
                    continue
            
            # Виводимо результати
            import json
            with open('real_world_wordlist.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Успішно спарсено {len(results)} елементів")
            for i, result in enumerate(results[:3], 1):  # Перші 3 результати
                print(f"\nРезультат #{i}:")
                print(f"Посилання: {result['link']}")
                print(f"Фраза: {result['phrase']}")
                print(f"Частина мови: {result['part_of_speech']}")
                print(f"Визначення: {result['definition']}")
            
            
            
        except Exception as e:
            print(f"Сталася помилка: {e}")
        finally:
            await browser.close()

# Запускаємо асинхронну функцію
async def main():
    await run_async_automation()

if __name__ == "__main__":
    asyncio.run(main())
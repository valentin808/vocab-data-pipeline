import asyncio
import json
from patchright.async_api import async_playwright


#скріпт призначения для пошуку транскрипції слів

async def add_pronunciation_data():
    with open('real_world_wordlist.json', 'r', encoding='utf-8') as f:
        words = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        try:
            for i, word in enumerate(words):
                if not word.get('link'):
                    continue
                
                page = None
                try:
                    page = await context.new_page()
                    await page.goto(word['link'], wait_until="domcontentloaded", timeout=15000)
                    
                    # Обробка британської вимови
                    uk_pron = page.locator('span.uk.dpron-i')
                    if await uk_pron.count() > 0:
                        ipa_elements = uk_pron.locator('span.ipa.dipa.lpr-2.lpl-1')
                        if await ipa_elements.count() > 0:
                            # Беремо перший елемент, якщо є кілька
                            word['pronunciation_uk'] = await ipa_elements.first.text_content()
                    
                    # Обробка американської вимови
                    us_pron = page.locator('span.us.dpron-i')
                    if await us_pron.count() > 0:
                        ipa_elements = us_pron.locator('span.ipa.dipa.lpr-2.lpl-1')
                        if await ipa_elements.count() > 0:
                            # Беремо перший елемент, якщо є кілька
                            word['pronunciation_us'] = await ipa_elements.first.text_content()
                    
                    print(f"Processed {i+1}/{len(words)}: {word.get('phrase')}")
                
                except Exception as e:
                    print(f"Error for {word.get('phrase')}: {str(e)}")
                finally:
                    if page:
                        await page.close()
                
                await asyncio.sleep(1)
            
            with open('real_world_with_pronunciation.json', 'w', encoding='utf-8') as f:
                json.dump(words, f, ensure_ascii=False, indent=2)
        
        finally:
            await context.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(add_pronunciation_data())
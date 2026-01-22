import asyncio
import json
from patchright.async_api import async_playwright

async def add_pronunciation_data():
    with open('real_world_with_pronunciation.json', 'r', encoding='utf-8') as f:
        words = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        try:
            for i, word in enumerate(words):
                page = None
                try:
                    page = await context.new_page()
                    await page.goto('https://www.deepl.com/uk/translator', wait_until="domcontentloaded", timeout=15000)
                    
                    # Обробка британської вимови
                    print("fisrt step")
                    await asyncio.sleep(2)
                    uk_pron = page.locator('xpath=/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/main/div[2]/nav/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/section/div/div[2]/div[1]/section/div/div[1]/d-textarea/div[1]')
                    await uk_pron.wait_for()
                    await uk_pron.fill(word['phrase'])
                    await asyncio.sleep(2)
                    trans=page.locator('xpath=/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/main/div[2]/nav/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/section/div/div[2]/div[3]/section/div[1]/d-textarea/div')
                    await trans.wait_for()
                    text= await trans.text_content(timeout=3000)
                    word['translate']=text
                    print(text)
                    
                    
                    print(f"Processed {i+1}/{len(words)}: {word.get('phrase')}")
                
                except Exception as e:
                    print(f"Error for {word.get('phrase')}: {str(e)}")
                finally:
                    if page:
                        await page.close()
                
                
                await asyncio.sleep(1)
            
            with open('real_world_with_translate.json', 'w', encoding='utf-8') as f:
                json.dump(words, f, ensure_ascii=False, indent=2)
        
        finally:
            await context.close()
            await browser.close()

if __name__ == "__main__":
    print('here')
    asyncio.run(add_pronunciation_data())
    
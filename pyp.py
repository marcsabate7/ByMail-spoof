import asyncio
from pyppeteer import launch

async def main(domain):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://phonebook.cz/')
    content = domain
    await page.evaluate(f"""() => {{
        document.getElementById('domain').value = '{content}';
    }}""")

    await page.click('#submit1')
    await asyncio.sleep(6)
    emails = await page.querySelector('pre')
    final_emails = await page.evaluate('(emails) => emails.textContent', emails)
    print(final_emails)
    print(type(final_emails))
    await browser.close()

asyncio.get_event_loop().run_until_complete(main("semic.es"))
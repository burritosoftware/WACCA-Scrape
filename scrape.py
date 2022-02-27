import aiohttp
import asyncio
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

# Loading .env values
load_dotenv()

baseurl = 'https://wacca.marv-games.jp/web/friend/find/result'

async def main():
    # Cookies and required headers for connecting to My Page
    session_id = open('cookie.txt', 'r', encoding='utf-8').read()
    cookies = {'WSID': session_id, 'WUID': session_id}
    headers = {'Connection': 'keep-alive', 'Host': 'wacca.marv-games.jp', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'}
    async with aiohttp.ClientSession(cookies=cookies, cookie_jar=aiohttp.CookieJar()) as session:
        # Friend code form data
        data = aiohttp.FormData({'friendCode': os.getenv('FRIENDCODE')}, quote_fields=True, charset=None)
        async with session.post(baseurl, data=data, headers=headers) as resp:
            html = await resp.text()
            # Filtering for next authentication cookie and printing it out
            jar = session.cookie_jar.filter_cookies(baseurl)
            for key, cookie in jar.items():
                if cookie.key == 'WSID':
                    with open('cookie.txt', 'w', encoding='utf-8') as f:
                        f.write(cookie.value)
                        f.close()
            soup = BeautifulSoup(html, "html.parser")
            results = soup.find_all("div", class_="user-info__detail__name")
            for friendname in results:
                print(friendname.text)

asyncio.run(main())
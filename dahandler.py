import asyncio
import html
from bs4 import BeautifulSoup
import aiohttp
import async_timeout

class Dahandler:

    def __init__(self):
        self.session = aiohttp.ClientSession()


    async def fetch(self, url):
        """ Get the source code of an URL"""
        with async_timeout.timeout(10):
            async with self.session.get(url) as response:
                return await response.text(encoding="utf8")

    async def getrandomdeviation(self):
        """ Get random deviation on deviantArt """
        pagesource = BeautifulSoup(await self.fetch("https://www.deviantart.com/random/deviation"), "html.parser")
        deviation = dict()

        head = pagesource.find("head")

        deviation["url"] = head.find("meta", {"property":"og:url"})["content"]
        deviation["img"] = head.find("meta", {"property":"og:image"})["content"]
        deviation["title"] = html.unescape(head.find("meta", {"property":"og:title"})["content"])
        deviation["desc"] = html.unescape(head.find("meta", {"property":"og:description"})["content"])

        print(deviation)
        return deviation

    async def getuserinfo(self, url):
        """ Get user info from a deviation """

        info = dict()
        pagesource = BeautifulSoup(await self.fetch(url), "html.parser")

        entry = pagesource.find('span', {"class":"dev-title-avatar"})

        info["url"] = entry.find("a")["href"]
        info["name"] = html.unescape(entry.find("img")["title"])
        info["avatar_url"] = entry.find("img")["src"]

        print(info)

        return info

    async def cleanup(self):
        """ Clean everything that was left opened"""
        await self.session.close()

async def main():
    dh = Dahandler()
    deviation = await dh.getrandomdeviation()
    await dh.getuserinfo(deviation["url"])
    await dh.cleanup()
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



        
import aiohttp
import asyncio
import re
import json


transcripts = ['' for x in range(0, 1779)]

async def grab_comic_transcript(comicnumber):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://xkcd.com/{}/info.0.json'.format(comicnumber)) as resp:
            try:
                x = await resp.json()
                text = x['transcript']
                #re.sub(r'\W+', '', text)
                text = re.sub(r"[^ \w!?\.']", '',text)
                transcripts[comicnumber]=text
                print(text)
            except json.JSONDecodeError:
                print('huh')




loop = asyncio.get_event_loop()  
loop.run_until_complete(asyncio.wait([grab_comic_transcript(x) for x in range(1,1777)]))


ofile = open('transcripts.txt', 'w')
ofile.write(' '.join(transcripts))


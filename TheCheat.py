from re import L
import requests
import discord
from bs4 import BeautifulSoup

client = discord.Client()

token = 'token  '


@client.event
async def on_message(msg):
    if msg.author.bot:
        return

    if msg.content.startswith('더!조회 '):
        adress = msg.content[4:]
        data = requests.post('https://thecheat.co.kr/rb/?mod=_search_result',
                             data={'keyword': adress})

        soup = BeautifulSoup(data.text, 'html.parser')

        if not """<td style="width:390px;background:green;height:30px; line-height:30px;background:url('./layouts/2014/images/search/tit_searchStep2_mentYes.png') no-repeat left 0"></td>""" in str(soup):
            await msg.channel.send((f'조회한 계좌: {adress}\n피해 사례가 없습니다.'))
        else:
            msgs = []

            for i in range(int((len(soup.select(".first")) - 1) / 2)):
                msgs.append('유형:{0}\n금액:{1}\n피해물품:{2}\n용의자 계좌번호:{3}'.format(soup.select(".first")[i + i].get_text(), soup.select(".first")[
                            i + i + 1].get_text(), soup.select(".cont")[i].get_text().lstrip().rstrip().split("\n")[0], soup.select(".view_sp")[i].get_text()))

            result = '\n'.join(msgs)
            await msg.channel.send(f'조회한 계좌: {adress}\n등록된 피해 사례: {int((len(soup.select(".first")) - 1) / 2)}건\n{result}')

client.run(token)

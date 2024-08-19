#region ──────────────── 봇 초기 설정 ────────────────
import discord
from discord.ext import commands
from discord import Embed
import asyncio
import requests
import os
import re

intents = discord.Intents.default()
intents.message_content = True  
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
#endregion ──────────────── 끝 ────────────────

#region ──────────────── 봇 설정 ────────────────
# 서버 ID 화이트리스트 / 채널 ID 화이트리스트에 없다면 모든 채널 사용 가능
whitelisted_servers = [0, 0]

# 채널 ID 화이트리스트 (서버 ID를 키로 사용) / 서버 ID [채널 ID, 채널 ID]
whitelisted_channels = {
    0: [0]  
}
@bot.event # 봇 ~ 하는 중 설정
async def on_ready():
    print(f'준비 완료 {bot.user}')
    game = discord.Game('!명령어') 
    await bot.change_presence(status=discord.Status.online, activity=game)

# 화이트리스트에 있는 명령어 정의 / 화이트리스트에 없으면 !검색 ~~~으로 적용됨.
whitelist_commands = ['명령어', '검색', '레이드', '방어구', '사이트', '마소', '상자', '점검', 'lfg', '영단어', '맹공']

@bot.event #화이트리스트 관련
async def on_message(message):
    # 봇이 보낸 메시지인지 확인
    if message.author == bot.user:
        return

    # 메시지가 화이트리스트에 있는 서버에서 왔는지 확인
    if message.guild and message.guild.id in whitelisted_servers:
        # 채널 ID 화이트리스트가 있는지 확인
        if message.guild.id in whitelisted_channels:
            # 메시지가 화이트리스트에 있는 채널에서 왔는지 확인
            if message.channel.id in whitelisted_channels[message.guild.id]:
                # '!'로 시작하는 메시지가 입력되었을 때
                ctx = await bot.get_context(message)
                if message.content.startswith('!'):
                    command = message.content[1:]  # 메시지의 나머지 부분을 명령어로 설정합니다.
                    if command not in whitelist_commands:
                        # 명령어가 화이트리스트에 없는 경우 '!검색' 명령어의 기능을 수행합니다.
                        await default_search(ctx, keyword=command)
                    else:
                        await bot.process_commands(message)
                else:
                    await bot.process_commands(message)
            else:
                return  # 화이트리스트에 없는 채널에서 온 메시지는 무시
        else:
            # 채널 ID 화이트리스트가 없으면 모든 채널에서 명령어 사용 가능
            ctx = await bot.get_context(message)
            if message.content.startswith('!'):
                command = message.content[1:]  # 메시지의 나머지 부분을 명령어로 설정합니다.
                if command not in whitelist_commands:
                    # 명령어가 화이트리스트에 없는 경우 '!검색' 명령어의 기능을 수행합니다.
                    await default_search(ctx, keyword=command)
                else:
                    await bot.process_commands(message)
            else:
                await bot.process_commands(message)
    else:
        return  # 화이트리스트에 없는 서버에서 온 메시지는 무시
#endregion ──────────────── 끝 ────────────────

#region ──────────────── 검색 ────────────────
async def default_search(ctx, keyword):
    folder = 'C:\\Users\\XXX\\Desktop\\XXX\\Bot\\Destiny 2\\txt_무기'  # txt_무기 파일 내 DB에만 접근
    keyword = keyword.lower().strip()

    results = []  # 검색 결과를 저장할 리스트를 생성합니다.
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    clean_line = re.sub(r'『.*?』', '', line).strip()  # 『와 』 안의 문자를 제거
                    if keyword in clean_line.lower():
                        name, ext = os.path.splitext(filename)
                        if i + 2 < len(lines):
                            next_line_1 = lines[i + -2].strip()
                            next_line_2 = lines[i + -1].strip()
                            results.append(f'**{name} > {next_line_1} > {next_line_2}**\n{line.replace("『", "").replace("』", "").strip()}\n')
                        else:
                            results.append(f'**{name}**\n{line.replace("『", "").replace("』", "").strip()}\n')
    message = '\n'.join(results)
    if not results:
        await ctx.send(검색_결과_없음)
    elif len(message) > 2000:  # 메시지 길이가 2000자를 초과하는 경우
        await ctx.send(메시지_초과)
    else:
        await ctx.send(message)

검색_결과_없음 = ('검색 결과가 없습니다. \n-# ㆍDB에 존재하지 않거나 철자, 띄어쓰기를 확인해 주세요.\n-# ㆍ무기의 추천 퍽 조합을 아시나요? 제보해주시면 DB에 업데이트됩니다!')
메시지_초과 = ('메시지가 2천 자를 넘습니다. 정확히 검색해 주세요.')
#endregion ──────────────── 끝 ────────────────

#region ──────────────── 명령어 ────────────────
@bot.command()
async def 명령어(ctx):
    with open(r"C:\Users\XXX\Desktop\XXX\Bot\Destiny 2\txt_기타\명령어.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    await ctx.send(content)

@bot.command()
async def 레이드(ctx):
    with open(r"C:\Users\XXX\Desktop\XXX\Bot\Destiny 2\txt_기타\레이드.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    await ctx.send(content)

@bot.command()
async def 방어구(ctx):
    with open(r"C:\Users\XXX\Desktop\XXX\Bot\Destiny 2\txt_기타\방어구.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    await ctx.send(content)

@bot.command()
async def 사이트(ctx):
    with open(r"C:\Users\XXX\Desktop\XXX\Bot\Destiny 2\txt_기타\사이트.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    await ctx.send(content)

@bot.command()
async def 마소(ctx):
    await ctx.send("""사진 링크 입력""")

@bot.command(name='점검')
async def send_info(ctx):
    embed = Embed(title="점검 일정", description="매주 (화) 22:45 데스티니 서버 종료, (수) 02:00 서버 오픈.", color=0x5CDBF0)
    embed.add_field(name="초기화", value="매주 수요일 02:00 (점검 후) 주간 일정 초기화. \n NPC 쥴은 토~화 출현", inline=False)
    embed.add_field(name="공식 트위터", value="[BungieHelp](<https://twitter.com/BungieHelp>)", inline=True)
    embed.add_field(name="기타", value="[업데이트](<https://www.bungie.net/7/en/News/updates>) / [서버 점검 세부 설명](<https://help.bungie.net/hc/ko/articles/360049199271-%EB%8D%B0%EC%8A%A4%ED%8B%B0%EB%8B%88-%EC%84%9C%EB%B2%84-%EB%B0%8F-%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8-%EC%83%81%ED%83%9C>) / [접속 관련 오류코드 검색](<https://help.bungie.net/hc/ko/articles/360049196971-%EC%98%A4%EB%A5%98-%EC%BD%94%EB%93%9C-CAT>)", inline=False)
    embed.set_footer(text="점검 시간 변동 시 공식 트위터 확인 필요.")
    await ctx.send(embed=embed)

@bot.command(name='상자')
async def send_embed(ctx):
    embed = discord.Embed(
        title="레이드 상자 체크포인트",
        description="""
[체크포인트 트위치 라이브(crymate)](<https://www.twitch.tv/crymate9341>)
[체크포인트 트위치 라이브(luckbot)](<https://www.twitch.tv/luckbot9>)
[체크포인트 트위치 라이브(travelerschosenteam)](<https://www.twitch.tv/travelerschosenteam>)
[기타 체크포인트(d2checkpoint)](https://d2checkpoint.com/>)

/합류 CRY_OCEAN#9878
/합류 CRY_FIELD#5002
        """,
        color=discord.Color.blue()
    )

    embed.add_field(name="유리 금고", value="""
[유금 입구 / 상자 2개](<https://youtu.be/YWInbp-yX20>)
[유금 고르곤의 미궁 / 상자 1개](<https://www.youtube.com/watch?v=4sye7sFvf0M>)
[유금 문지기 앞 / 상자 1개](<https://www.youtube.com/watch?v=gabLKHs4vVw>)
                    """, inline=False)
    
    embed.add_field(name="크로타의 최후", value="""
[크로타 미로 / 상자 1개](<https://www.youtube.com/watch?v=Ii-RxvcNuAY>)
                    """, inline=False)
    
    embed.add_field(name="왕의 몰락", value="""
[왕몰 점프맵 / 상자 2개](<https://www.youtube.com/watch?v=XYAn8SOm9eo>)
                    """, inline=False)

    embed.add_field(name="신봉자", value="""
[신봉자 / 상자 1개](<https://www.youtube.com/watch?v=V5zecq8WvZY>)
                    """, inline=False)

    embed.add_field(name="기타", value="""
[기타 레이드 상자(위 상자 위치 포함) / 상자 27개](<https://youtu.be/tLntjbXvk8M?t=32>)
                    """, inline=False)
    
    embed.set_footer(text="유튜브 참고해서 갈 것, 쳌포 덮어씌우면 블락")
    await ctx.send(embed=embed)

@bot.command()
async def lfg(ctx):
    with open(r"C:\Users\XXX\Desktop\XXX\Bot\Destiny 2\txt_기타\lfg.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    await ctx.send(content)

@bot.command()
async def 영단어(ctx):
    with open(r"C:\Users\XXX\Desktop\XXX\Bot\Destiny 2\txt_기타\영단어.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    await ctx.send(content)

@bot.command()
async def 맹공(ctx):
    with open(r"C:\Users\XXX\Desktop\XXX\Bot\Destiny 2\txt_기타\맹공.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    await ctx.send(content)
#endregion ──────────────── 끝 ────────────────

# 봇 토큰
bot.run('0')




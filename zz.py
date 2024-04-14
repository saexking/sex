import discord
from discord.ext import commands
import requests
import pytz
from datetime import datetime

API_KEY = "919ebabcc97ed4cb3fd75bdc16497430"
CITY_ID = "1835848"
TOKEN = "MTIyODYyNzEzNzA0OTY2MTQ0MA.GaKZDx.1Jeww2LeDcpXzNHDUSmUInTaUUNC2ELhQWIEew"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?    ', intents=intents)

# 특정 사용자 ID 설정
allowed_users = [844038404681367613]

@bot.event
async def on_ready():
    print(f'{bot.user.name}가 준비됐어요!')

@bot.command()
async def 지급(ctx):
    if ctx.author.id in allowed_users:  # 권한 확인
        role = discord.utils.get(ctx.guild.roles, name="육군인원ㅣRoka Personnel")  # 역할 가져오기
        if role is not None:
            for member in ctx.guild.members:  # 서버의 모든 멤버에게 역할 부여
                await member.add_roles(role)
            await ctx.send("**서버에 있는 모든 유저에게 역할을 지급했습니다.**")
        else:
            await ctx.send("**육군인원ㅣRoka Personnel 역할을 찾을 수 없어요.**")
    else:
        await ctx.send("**이 명령어를 사용할 수 있는 권한이 없어요.**")

@bot.command()
async def 핑(ctx):
    latency = bot.latency * 1000
    await ctx.send(f'**`{latency:.2f}ms`**')

@bot.command()
async def 시간(ctx):
    try:
        tz = pytz.timezone('Asia/Seoul')
        current_time = datetime.now(tz)
        await ctx.send(f'**`한국의 현재 시간 : {current_time.strftime("%Y-%m-%d %H:%M:%S")}`**')
    except pytz.UnknownTimeZoneError:
        await ctx.send('**`시간을 가져올 수 없습니다.`**')

@bot.command()
async def 날씨(ctx):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']

        await ctx.send(f"**`서울 날씨 {weather}, 기온: {temp}℃, 습도: {humidity}%`**")
    except Exception as e:
        print(e)
        await ctx.send('**`날씨 정보를 가져올 수 없어요.`**')

@bot.command()
@commands.has_permissions(administrator=True)
async def 청소(ctx, 횟수: int):
    if 횟수 > 1000:
        await ctx.send("**최대 1000개의 메시지를 지울 수 있습니다.**")
    else:
        deleted = await ctx.channel.purge(limit=횟수 + 1)
        await ctx.send(f'**{len(deleted) - 1}개의 메시지를 삭제했습니다.**', delete_after=10)

@bot.command()
async def 전체공지(ctx):
    if ctx.author.id in allowed_users:
        try:
            embed = discord.Embed(
                title="중요 공지",
                description="청운부대 서버의 스카우트-요청 채널에 알맞은 양식을 작성하여, 스카우트를 받고 고위 간부가 되어 보세요!\n\n병사, 부사관, 장교를 대상으로 로벅스 이벤트, 꽁머니 이벤트, 진급 행사 등을 주기적으로 개최하니, 나가지 말고 혜택을 누리세요!",  # 전송할 메시지
                color=discord.Color.blurple()  # 임베드 색상 설정
            )
            for member in ctx.guild.members:
                await member.send(embed=embed)
            await ctx.send("**서버의 모든 멤버에게 임베드 형식으로 메시지를 전송했습니다.**")
        except Exception as e:
            print(f"메시지 전송 중 오류 발생: {e}")
            await ctx.send("**메시지를 전송하는 중에 오류가 발생했습니다.**")
    else:
        await ctx.send("**이 명령어를 사용할 수 있는 권한이 없습니다.**")

@bot.command()
async def 도배(ctx, 횟수: int, *, 메시지: str):
    if ctx.author.id in allowed_users:
        if 횟수 > 10000:
            await ctx.send("**도배는 나빠요:sob:**")
        else:
            for _ in range(횟수):
                await ctx.send(메시지)
    else:
        await ctx.send("**이 명령어를 사용할 수 있는 권한이 없어요.**")

@bot.command()
async def 설치(ctx):
    embed = discord.Embed(
        title="인증하기",
        description="아래 체크 이모지를 클릭하여 인증 하세요.",
        color=0xFFB6C1  # 연한 핑크색
    )
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")  # 체크 이모지 추가

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == bot.user:  # 봇이 보낸 메시지인지 확인
        if str(reaction.emoji) == "✅":  # 체크 이모지인지 확인
            role = discord.utils.get(user.guild.roles, name="육군인원ㅣRoka Personnel")  # 역할 가져오기
            await user.add_roles(role)  # 역할 지급
            await user.send(f"{user.mention}, 청운부대ㅣCheong Un Army 인증이 완료되었습니다.")  # 유저에게 메시지 보내기

bot.run(TOKEN)

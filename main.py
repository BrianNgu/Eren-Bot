import discord

from discord.ext import commands
from aiohttp import request
import json
import requests
import youtube_dl
import os
from mal import *
from random import randint
from random import choice
import random


client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    general_channel= client.get_channel("enter channel ID here")
    await general_channel.send('Bot is now running')

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel")
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Currently the audio is not paused.")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()

#Alberta[0], BC[1], Manitoba[2], NB[3], NL[4], Nova Scotia[5], Nunuvat[6], North West Terrioties[7], Ontario[8], PEI[9], Quebec[10], Sask[12] , Yukon [13]
@client.command(name = "activeCases")
async def covid_case(ctx):
    
    URL = "https://api.opencovid.ca/summary"
    covidCases= requests.get(URL).json()

    async with request("GET",URL,headers={}) as response:
        if response.status== 200:
            data = await response.json()
            await ctx.send('Number of Active Covid cases in Ontario are: '+ str(covidCases['summary'][8]['active_cases']))
        
@client.command(name = "totalVaccines")
async def covid_case(ctx):
    URL = "https://api.opencovid.ca/summary"
    covidCases= requests.get(URL).json()

    async with request("GET",URL,headers={}) as response:
        if response.status== 200:
            data = await response.json()
            await ctx.send('Total Vaccines distributed so far in Ontario are: '+ str(covidCases['summary'][8]['cumulative_cvaccine']))

@client.command(name = "totalDeaths")
async def covid_case(ctx):
    URL = "https://api.opencovid.ca/summary"
    covidCases= requests.get(URL).json()

    async with request("GET",URL,headers={}) as response:
        if response.status== 200:
            data = await response.json()
            await ctx.send('Total Deaths distributed so far in Ontario are: '+ str(covidCases['summary'][8]['cumulative_deaths']))

@client.command(name= "anime")
async def anime_name(ctx):

        randomValue = randint(1, 1000)
        anime = Anime(randomValue)
        embed = discord.Embed(title="Check out this anime!", description="Anime Title: " + anime.title + "\nMyAnimeList Rating: " + str(anime.score), color=discord.Color.gold())
        await ctx.channel.send(embed=embed)
@client.command(name = "dog")
async def dogfact(ctx):
        request = requests.get('https://some-random-api.ml/img/dog')
        dogjson = json.loads(request.text)
        request2 = requests.get('https://some-random-api.ml/facts/dog')
        factjson = json.loads(request2.text)

        embed = discord.Embed(title="Random Dog Facts!", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.channel.send(embed=embed)
@client.command(name = "meme")
async def memes(ctx):
        request = requests.get('https://some-random-api.ml/meme')
        meme = json.loads(request.text)

        embed = discord.Embed(title="Memes!", color=discord.Color.blue())
        embed.set_image(url=meme['image'])
        await ctx.channel.send(embed=embed)

@client.command(name = "yoda")
async def yoda(ctx):
    yoda_quotes = [
        '"Do. Or do not. There is no try." \n-Yoda',
      '"You must unlearn what you have learned." \n-Yoda',
      '"When nine hundred years old you reach, look as good you will not." \n-Yoda',
      '"Truly wonderful, the mind of a child is." \n-Yoda',
      '"A Jedi uses the Force for knowledge and defense, never for attack." \n-Yoda',
      '"Adventure. Excitement. A Jedi craves not these things." \n-Yoda',
      '"Size matters not. Judge me by my size, do you?" \n-Yoda',
      '"Fear is the path to the dark side…fear leads to anger…anger leads to hate…hate leads to suffering." \n-Yoda',
      '"Wars not make one great." \n-Yoda',
      '"Luminous beings are we…not this crude matter." \n-Yoda',
      '"Difficult to see. Always in motion is the future." \n-Yoda',
      '"Control, control, you must learn control!" \n-Yoda']
    response = random.choice(yoda_quotes)
    await ctx.channel.send(response)
@client.command(name = "obiwan")
async def obiwan(ctx):
    obi_wan_quotes = [
        '"You must do what you feel is right, of course." \n-Obi-Wan Kenobi',
      '"Mos Eisley Spaceport. You will never find a more wretched hive of scum and villainy. We must be cautious." \n-Obi-Wan Kenobi',
      '"Your eyes can deceive you. Don’t trust them." \n-Obi-Wan Kenobi',
      '"Remember... the Force will be with you, always." \n-Obi-Wan Kenobi',
      '"In my experience, there is no such thing as luck." \n-Obi-Wan Kenobi',
      '"These are not the droids you are looking for." \n-Obi-Wan Kenobi',
      '"I felt a great disturbance in the Force, as if millions of voices suddenly cried out in terror and were suddenly silenced." \n-Obi-Wan Kenobi',
      '"Use the Force, Luke."\n-Obi-Wan Kenobi',
      '"You cannot win, Darth Vader. If you strike me down, I shall become more powerful than you could possibly imagine." \n-Obi-Wan Kenobi',
      '"That is no moon. It is a space station." \n-Obi-Wan Kenobi',
      '"Luke! Do not give in to hate. That leads to the Dark Side." \n-Obi-Wan Kenobi',
      '"Who is the more foolish, the fool or the fool who follows him?"" \n-Obi-Wan Kenobi',
      '"And these blast points, too accurate for Sandpeople. Only Imperial Stormtroopers are so precise." \n-Obi-Wan Kenobi']
    response = random.choice(obi_wan_quotes)
    await ctx.channel.send(response)
@client.command(name = "palpatine")
async def palpatine(ctx):
    emperor_quotes = [
        '"Young fool... Only now, at the end, do you understand..." \n-The Emperor',
      '"Your feeble skills are no match for the power of the Dark Side." \n-The Emperor',
      '"Now, you will pay the price for your lack of vision!" \n-The Emperor',
      '"I will make it legal." \n-Darth Sidious',
      '"Power! Unlimited Power!" \n-Darth Sidious',
      '"Execute Order 66." \n-Darth Sidious',
      '"The Dark Side Of The Force Is A Pathway To Many Abilities Some Consider To Be Unnatural." \n-Chancellor Palpatine',
      '"Everything That Has Transpired Has Done So According To My Design." \n-The Emperor',
      '"Your Feeble Skills Are No Match For The Power Of The Dark Side." \n-The Emperor',
      '"This Is Not The First Time You Have Proven To Be Clumsy, Lord Tyranus. You Know The Price Of Failure." \n-Darth Sidious',
      '"There, There Child. Soon You Will Cry No More." \n-Darth Sidious',
      '"Now Young Skywalker, You Will Die." \n-The Emperor',
      '"There Is No Mercy." \n-Darth Sidious',
      '"Your Faith In Your Friends Is Yours." \n-The Emperor',
      '"So Be It... Jedi." \n-The Emperor',
      '"Did you ever hear the tragedy of Darth Plagueis the wise?" \n-Chancellor Palpatine',
      '"I AM the senate!" \n-Chancellor Palpatine',
      '"It is treason, then..." \n-Chancellor Palpatine',
      '"I have waited a long time for this moment, my little green friend. At last, the Jedi are no more." \n-Darth Sidious',
      '"Your arrogance blinds you, Master Yoda. Now you will experience the full power of the Dark Side." \n-Darth Sidious',
      '"The Dark Side of the Force is a pathway to many abilities some consider to be unnatural." \n-Chancellor Palpatine'
    ]
    response = random.choice(emperor_quotes)
    await ctx.channel.send(response)
@client.command(name = "darthvader")
async def darthvader(ctx):
    darth_vader_quotes = [
        '"I find your lack of faith disturbing." \n-Darth Vader',
      '"The circle is now complete. When I left you, I was but the learner. Now I am the master." \n-Darth Vader',
      '"The Force is with you, young Skywalker, but you are not a Jedi yet." \n-Darth Vader',
      '"No. I am your father." \n-Darth Vader',
      '"Impressive. Most impressive." \n-Darth Vader',
      '"I am altering the deal. Pray I do not alter it any further." \n-Darth Vader',
      '"You underestimate the power of the Dark Side. If you will not fight, then you will meet your destiny." \n-Darth Vader',
      '"You have failed me for the last time, Admiral!" \n-Darth Vader',
      '"The Force is strong with this one." \n-Darth Vader',
      '"The ability to destroy a planet is insignificant next to the power of the Force." \n-Darth Vader'
    ]
    response = random.choice(darth_vader_quotes)
    await ctx.channel.send(response)
#Runs the client on the server
client.run("enter client ID here")
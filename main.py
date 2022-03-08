import discord
import os, sys, io
from alive import keepAlive

client = discord.Client()
lines = []

def compile(code):
  open('script.py','w').write('\n'.join(code))
  old_stdout = sys.stdout
  sys.stdout = buffer = io.StringIO()
  try:
    exec(open("script.py").read())

    sys.stdout = old_stdout
    prevPrint = buffer.getvalue()
    return prevPrint
  except Exception as e: return e

@client.event
async def on_ready():
    print(client.user)

@client.event
async def on_message(message):
  global lines
  if message.author != client.user:
    content = str(message.content)
    author = str(message.author)
    if content.split(':')[0] == 'compile':
      lines.clear()
      scriptbody = content.replace('compile:','').replace('```','')
      x = 0
      for i in range(len(scriptbody)):
        if scriptbody[i] == '\n':
          lines.append(scriptbody[x:i])
          x = i+1
      lines = lines[2:]
      try: await message.channel.send('```'+str(compile(lines))+'```')
      except: 
        await message.channel.send('Form is too long to be printed!')
    elif content == 'help python':
      embed = discord.Embed(title = '**Help**',
                            description = '''
                            PyBot runs python code and prints the                                               output for you on discord!
                            
                            While loops and input statements                                                    obviously don't work but pretty much                                                anything else does. Imports work and                                                there's also error exception!'''
                           )
      await message.channel.send(embed = embed)

keepAlive()
token = os.environ.get("DISCORDBOTSECRET")
client.run(token)

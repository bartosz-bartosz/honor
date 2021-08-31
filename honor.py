#! python3 

import pickle
import time
import discord
from discord.ext import commands


####### INPUT ---------------------------------------------------------------------

timestr = time.strftime("%Y%m%d-%H%M%S")
ldrs = pickle.load(open('leaderboard.pkl', 'rb'))

'''This section is for updating TOKEN'''
# token = ''
# with open('token.pkl', 'wb') as file
# 	pickle.dump(token, file)

token_file = open('token.pkl', 'rb')
TOKEN = pickle.load(token_file)

####### FUNCTIONS -----------------------------------------------------------------

def wrong_command():
	return 'BŁĘDNA KOMENDA'

def add_point(player, point):
	player = player.upper()
	if player in ldrs.keys():
		if point[0] == '+':
			num = float(point[1:].replace(',', '.'))
			ldrs[player] += num
			return f'**{player}** OTRZYMUJE **{num}** HONORU (RAZEM **{ldrs[player]}**)\n:+1: BRAWO {player}'
		elif point[0] == '-':
			num = float(point[1:].replace(',', '.'))
			ldrs[player] -= num
			return f'**{player}** TRACI **{num}** HONORU (RAZEM **{ldrs[player]}**)\n:-1: WSTYDŹ SIĘ {player}'
		else:
			return wrong_command()
	else:
		return f'NIE MA TAKIEGO GRACZA JAK {player}'

def set_points(player, point):
	player = player.upper()
	point = float(point)
	if player in ldrs.keys():
		ldrs[player] = point
		return f'ZRESETOWANO HONOR GRACZA {player} DO {point}'	
	else:
		return	wrong_command()

def reset_points():
	for k in ldrs.keys():
		ldrs[k] = 0.0
	return '\nZRESETOWANO WSZYSTKIE PUNKTY HONORU'

def show_ldrs(ldrs):
	table = ':chart_with_upwards_trend: **PUNKTY HONORU**: \n'
	ldrs = {k: v for k, v in sorted(ldrs.items(), key=lambda item: item[1], reverse=True)}
	position = 1
	for k, v in ldrs.items():
		nazwa = str(position) + '. ' + str(k) + ':'
		position += 1
		table += nazwa.ljust(10) + str(v).rjust(20) + '\n'
	return table

def show_player(player):
	player = player.upper()
	player_points = str(ldrs[player])
	return f'{player} MA TERAZ {player_points} HONORU'

def save_pickle(ldrs):
	pickle.dump(ldrs, open('leaderboard.pkl', 'wb'))
	print('ZAPISANO!')

def backup_pickle(ldrs):
	pickle.dump(ldrs, open('leaderboard_backup.pkl', 'wb'))
	print('\n> BACKUP DONE\n')


####### DISCORD FUNCTIONS ----------------------------------------------------------- 

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
	print('> HONOR JEST GOTOWY DO PROWADZENIA DZIAŁAŃ')

@bot.command(aliases=['honor'])
async def HONOR(ctx):
    await ctx.send(show_ldrs(ldrs))

@bot.command(aliases=['p'])
async def P(ctx, arg1, arg2):
	await ctx.send(add_point(arg1, arg2))
	save_pickle(ldrs)

@bot.command()
async def SET(ctx, arg1, arg2):
	await ctx.send(set_points(arg1, arg2))

@bot.command()
async def RESETUJ(ctx):
	await ctx.send(show_ldrs(ldrs))
	await ctx.send('.............')
	await ctx.send(reset_points())	

@bot.command(aliases=['save'])
async def SAVE(ctx):
	save_pickle(ldrs)
	await ctx.send('ZAPISANO')


####### RUN ----------------------------------------------------------------------

print(show_ldrs(ldrs))
backup_pickle(ldrs)

bot.run(TOKEN)
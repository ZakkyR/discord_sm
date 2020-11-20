import os
import sys
import discord
import db_access
from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']

PREFIX = 'sm!'

bot = commands.Bot(command_prefix=PREFIX, description='メッセージのショートカットが登録できるBOT')

'''
Events
'''


# 初期登録
@bot.event
async def on_guild_join(guild: discord.Guild):
    try:
        if db_access.count_server_mst(guild.id) != 0:
            db_access.upsert_server_mst(guild.id)

    except Exception as ex:
        print(ex, sys.exc_info()[0])


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name='{0}help'.format(PREFIX)))


'''
Commands
'''


@bot.command(description='メッセージショートカット登録', usage='sm!add [shortcut] [message_id]')
async def add(ctx: commands.context, shortcut: str, message_id: int):
    """
    メッセージショートカット登録
    shortcut: ショートカット名
    message_id: メッセージID
    """
    try:
        try:
            if db_access.get_shortcut_message(ctx.guild.id, shortcut) is not None:
                raise ValueError('ショートカット：`{0}`はすでに登録されています'.format(shortcut))

            sc_message = await ctx.fetch_message(message_id)

            if sc_message.content.startswith(PREFIX):
                raise ValueError('{0}から始まるメッセージは登録できません'.format(PREFIX))

            message_list = [sc_message.content, ] + [file['url'] for file in sc_message.attachments]
            db_access.insert_shortcut(ctx.guild.id, shortcut, '\n'.join(message_list))

            success_msg = [
                "メッセージを登録しました",
                "ショートカット：`{0}`".format(shortcut.strip()),
                "メッセージ：",
                "```",
                '\n'.join(message_list),
                "```",
            ]

            await ctx.send('\n'.join(success_msg))

        except discord.NotFound as ex:
            raise ValueError('メッセージIDが間違っています')

    except Exception as ex:
        await ctx.send(ex)


@bot.command(description='メッセージショートカット削除', usage='sm!delete [shortcut]')
async def delete(ctx: commands.context, shortcut: str):
    """
    メッセージショートカット削除
    shortcut: ショートカット名
    """
    try:
        if db_access.get_shortcut_message(ctx.guild.id, shortcut) is None:
            raise ValueError('ショートカット：`{0}`は存在しません'.format(shortcut))

        db_access.delete_shortcut(ctx.guild.id, shortcut)

        success_msg = 'ショートカット：`{0}` を削除しました'.format(shortcut)
        await ctx.send(success_msg)

    except Exception as ex:
        await ctx.send(ex)


@bot.command(name='list', description='メッセージショートカットリスト')
async def _list(ctx: commands.context):
    """
    登録されているショートカット一覧を表示
    """
    try:
        rows = db_access.get_shortcut_list(ctx.guild.id)
        sc_list = []

        for row in rows:
            sc_list.append("`{0}`".format(row[0]))

        if len(sc_list) == 0:
            raise ValueError('ショートカットは登録されていません')
        else:
            await ctx.send('\n'.join(sc_list))

    except Exception as ex:
        await ctx.send(ex)


@bot.listen('on_message')
async def get_message(message: discord.Message):
    if message.author.bot:
        return

    elif message.content.startswith(PREFIX):
        return

    try:
        msg = db_access.get_shortcut_message(message.guild.id, message.content)

        if msg is None:
            return

        await message.channel.send(msg)

    except Exception as ex:
        await message.channel.send(ex)


'''
Start Server
'''
bot.run(TOKEN)

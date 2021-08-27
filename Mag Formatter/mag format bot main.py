import discord
import os

client = discord.Client()

#Constants
trigger_text = '!magformat'
del_flag_text = '--no-delete'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def format_table_line(user_string, index=0, width=12):
    form_line = []
    if index == 0:
        form_line.append(" ".ljust(width))
    else:
        form_line.append(("Clicker # %d" % (index)).ljust(width))
    s_str = user_string.split(",")
    for entry in s_str:
        entry = entry.strip()[0:width - 1]
        form_line.append(" %s " % entry.ljust(width))
    return "|".join(form_line)


@client.event
async def on_message(message):
    #adds starting triple hashes
    to_send = "```"
    if message.content.startswith(trigger_text):
        user_message = message.content.split('\n')
        clicker_index = 0
        for line in user_message:
            #skips the first line containing the command and flags
            if line.startswith(trigger_text):
                continue
            to_send = "%s\n%s" % (to_send,
                                  format_table_line(line, clicker_index))
            clicker_index += 1
        #adds ending triple hashes
        to_send = "%s```" % to_send
        if del_flag_text in message.content:
            await message.delete()
        await message.channel.send(to_send)


client.run(os.getenv('TOKEN'))

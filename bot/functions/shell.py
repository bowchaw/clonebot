from subprocess import run as srun
from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher
from bot.helper.tg_helper.filters import CustomFilters
from bot.helper.tg_helper.list_of_commands import BotCommands
from bot.helper.tg_helper.msg_utils import sendMessage


def shell(update, context):
    message = update.effective_message
    cmd = message.text.split(" ", 1)
    if len(cmd) == 1:
        return sendMessage(
            "No command to execute was given.", context.bot, update.message
        )
    cmd = cmd[1]
    process = srun(cmd, capture_output=True, shell=True)
    reply = ""
    stderr = process.stderr.decode("utf-8")
    stdout = process.stdout.decode("utf-8")
    if len(stdout) != 0:
        reply += f"*Stdout*\n<code>{stdout}</code>\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"*Stderr*\n<code>{stderr}</code>\n"
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open("shell_output.txt", "w") as file:
            file.write(reply)
        with open("shell_output.txt", "rb") as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id,
            )
    elif len(reply) != 0:
        sendMessage(reply, context.bot, update.message)
    else:
        sendMessage("No Reply", context.bot, update.message)



SHELL_HANDLER = CommandHandler(
    BotCommands.ShellCommand, shell, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True,
)

R_HANDLER = CommandHandler(
    BotCommands.RCommand, shell, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True,
)

SH_HANDLER = CommandHandler(
    BotCommands.ShCommand, shell, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True,
)

JK_HANDLER = CommandHandler(
    BotCommands.JKCommand, shell, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True,
)

dispatcher.add_handler(SHELL_HANDLER)
dispatcher.add_handler(R_HANDLER)
dispatcher.add_handler(SH_HANDLER)
dispatcher.add_handler(JK_HANDLER)

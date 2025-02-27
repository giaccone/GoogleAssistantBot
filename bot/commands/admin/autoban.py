from utils import decorator
from telegram.error import TelegramError


@decorator.general_admin
@decorator.cancellacomandi
def init(update, context):
    """
    This command is executed sending the command:
        /autoban reason
    
    where 'reason' is a message to explain to the user the reason of the ban

    The command must be used in reply to the user's message. The bot sends a message
    in the chat to the user providing the 'reason'. After 60 seconds the user is banned.
    """
    # decode command
    reason = update.message.text.replace('/autoban ', '').strip()
    # get username
    name = "@" + update.message.reply_to_message.from_user.username \
        if update.message.reply_to_message.from_user.username is not None \
        else update.message.reply_to_message.from_user.name

    # set and send message to the user
    msg = f"{name}, sarai bannato dal gruppo fra 60 secondi per questo motivo:\n\n{reason}"
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=msg,
                             reply_to_message_id=update.message.reply_to_message.message_id)

    # set delayed action
    def delayed_ban(context, update=update):
        try:
            context.bot.ban_chat_member(chat_id=update.message.chat.id,
                                        user_id=update.message.reply_to_message.from_user.id)
        except TelegramError:
            print("an error occurred [AUTOBAN] function")
            update.message.send_message(chat_id=update.message.chat_id, text="Error during autoban operation")

    # schedule action
    seconds = 60
    context.job_queue.run_once(delayed_ban, seconds)

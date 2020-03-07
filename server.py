import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from functools import partial

import profile
import state
from controllers import profile_management

VERIFICATION_TOKEN = "841052885:AAHzY9v0Q_waTOFJsdnYtVcdMjyBVKJ9nyI"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# MAIN_MENU, PROFILE, SEARCH_PRODUCT, EDIT_PROFILE, DISPLAY_PROFILE = range(5)

reply_keyboard = [['Profile'],
                  ['Search Product'],
                  ['About', 'Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    user = update.effective_user
    message = profile_management.get_start_message(user)
    update.message.reply_text(
        message,
        reply_markup=markup)

    return state.MAIN_MENU


def search_product(update, context):
    update.message.reply_text('Alright, what kind of product are you looking for?"')
    return state.SEARCH_PRODUCT


def about(update, context):
    update.message.reply_text('Shopping Assistant Chatbot \nDeveloped By Yashar, Sahand, Saketh and Rajesh')
    return state.MAIN_MENU


def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:\n"
                              "{}\n"
                              "Until next time!\n"
                              "type /start to start over!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(VERIFICATION_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            state.MAIN_MENU: [MessageHandler(Filters.regex('^.*(Profile|profile).*$'), profile.profile),
                              MessageHandler(Filters.regex('^.*(Search|search|Product|product).*$'), search_product),
                              MessageHandler(Filters.regex('^(About|about)$'), about)],

            state.PROFILE: [MessageHandler(Filters.regex('^.*(Display|display|Show|show).*$'), profile.display),
                            MessageHandler(Filters.regex('^.*(Edit|edit|Modify|modify).*$'), profile.edit),
                            MessageHandler(Filters.regex('^(Back|back|Main|main)$'), start)],

            state.EDIT_PROFILE: [MessageHandler(Filters.regex('^.*(First|first).*$'), profile.goto_firstname_state),
                                 MessageHandler(Filters.regex('^.*(Last|last|Family|family).*$'), profile.goto_lastname_state),
                                 MessageHandler(Filters.regex('^.*(Gender|gender|Sex|sex).*$'), profile.goto_gender_state),
                                 MessageHandler(Filters.regex('^.*(Postal|postal).*$'), profile.goto_postalcode_state),
                                 MessageHandler(Filters.regex('^.*(Back|back|Main|main).*$'), profile.profile)],
            state.EDIT_FNAME: [MessageHandler(Filters.text, partial(profile.edit_field, field_name='first_name'))],
            state.EDIT_LNAME: [MessageHandler(Filters.text, partial(profile.edit_field, field_name='last_name'))],
            state.EDIT_GENDER: [MessageHandler(Filters.text, profile.edit_gender)],
            state.EDIT_POSTALCODE: [MessageHandler(Filters.text, partial(profile.edit_field, field_name='postal_code'))],

            state.SEARCH_PRODUCT: [MessageHandler(Filters.text, start)]
        },
        fallbacks=[MessageHandler(Filters.regex('^.*Done.*$'), done)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

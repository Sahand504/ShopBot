import state
from telegram import ReplyKeyboardMarkup

def profile(update, context):
    reply_keyboard = [['Edit Profile', 'Display Profile'], ['Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Do you want to see your profile or edit it?', reply_markup=markup)

    return state.PROFILE


def edit(update, context):
    reply_keyboard = [['Firstname', 'Lastname'],
                      ['Address', 'Phone Number'],
                      ['Shirt Size', 'Shoe Size'],
                      ['Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('What do you want to change in your profile?', reply_markup=markup)

    return state.EDIT_PROFILE

def goto_firstname_state(update, context):
    update.message.reply_text("Please tell me what\'s your firstname?")
    return state.EDIT_FNAME

def edit_firstname(update, context):
    firstname = update.message.text
    print(firstname)
    if firstname != 'Back':
        update.message.reply_text("Thanks %s" %firstname)
    return state.EDIT_PROFILE
#
#   TODO edit firstname
#

def display(update, context):
    name = "name"
    address = "address"
    phone_num = "123-123-1234"
    gender = "M"
    shirt_size = 'M'
    shoe_size = '10'

    print('Firstname: %s \nLastname: %s \nchat_id: %s \n'
          % (update.effective_user.first_name, update.effective_user.last_name, update.message.chat_id))

    update.message.reply_text('Firstname: %s \nLastname: %s \nchatid: %s \n'
          % (update.effective_user.first_name, update.effective_user.last_name, update.message.chat_id))

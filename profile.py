import state
from telegram import ReplyKeyboardMarkup
from controllers import profile_management

def profile(update, context):
    reply_keyboard = [['Edit Profile', 'Display Profile'], ['Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text('Do you want to see your profile or edit it?', reply_markup=markup)

    return state.PROFILE


def edit(update, context):
    reply_keyboard = [['Firstname', 'Lastname'],
                      ['Gender', 'Postal Code'],
                      ['Shirt Size', 'Shoe Size'],
                      ['Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text('What do you want to change in your profile?', reply_markup=markup)

    return state.EDIT_PROFILE

def goto_firstname_state(update, context):
    update.message.reply_text("Please tell me what\'s your firstname?")
    return state.EDIT_FNAME


def goto_lastname_state(update, context):
    update.message.reply_text("Please tell me what\'s your lastname?")
    return state.EDIT_LNAME


def goto_gender_state(update, context):
    reply_keyboard = [['Male', 'Female'], ['Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text('Please tell me what\'s your gender?', reply_markup=markup)
    return state.EDIT_GENDER


def goto_postalcode_state(update, context):
    update.message.reply_text("Please tell me what\'s your postal code?")
    return state.EDIT_POSTALCODE


def goto_shirtsize_state(update, context):
    user_id = update.effective_user["id"]
    reply_keyboard = ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"]
    user = profile_management.search_user(user_id)
    if "shirt_sizes" in user.keys():
        shirt_sizes = user["shirt_sizes"]
        for idx, reply_key in enumerate(reply_keyboard):
            if reply_key in shirt_sizes:
                print(reply_key)
                reply_keyboard[idx] += ' \u2714'
                print(reply_key)

    print(reply_keyboard)
    reply_keyboard = [reply_keyboard[:2], reply_keyboard[2:4], reply_keyboard[4:6], reply_keyboard[6:], ["Back"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text('Please tell me what shirt sizes usually work for you?', reply_markup=markup)
    return state.EDIT_SHIRTSIZE


def edit_field(update, context, field_name):
    field = update.message.text
    if field != 'Back':
        profile_management.update_user(update.effective_user["id"], field_name, field)
        update.message.reply_text("Thanks")
    return state.EDIT_PROFILE


def edit_gender(update, context):
    gender = update.message.text
    if gender == "Back":
        return edit(update, context)
    elif gender == "Male" or gender == "Female":
        profile_management.update_user(update.effective_user["id"], "gender", gender)
        return edit(update, context)

def edit_shirt_size(update, context):
    user_id = update.effective_user["id"]
    shirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"]
    shirt_size = update.message.text
    if shirt_size == "Back":
        return edit(update, context)
    elif shirt_size in shirt_sizes:
        profile_management.update_user_by_push(user_id, "shirt_sizes", shirt_size)
        return edit(update, context)
    elif str(shirt_size).__contains__(' \u2714'):
        profile_management.update_user_by_pull(user_id, "shirt_sizes", str(shirt_size).replace(' \u2714', ''))
        return edit(update, context)


def display(update, context):
    user_id = update.effective_user["id"]
    user_str = profile_management.user_info_tostr(user_id)
    print(user_str)
    update.message.reply_text(user_str)

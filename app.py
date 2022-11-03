# imports

import os

TOKEN = os.environ.get('TELEGRAM_ID')

import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
Updater,
CommandHandler,
MessageHandler,
Filters,
ConversationHandler,
CallbackContext,
)

from typing import Dict

from typing import Dict
# Enable logging
logging.basicConfig(
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# constants

SERVICE_CHOOSE, TYPE_OF_ARTICLE, TYPE_OF_SERVICE, TIMINNG_OF_SERVICE, TITLE_OF_PROJECT, DESCRIPTION_OF_PROJECT, FILE, RECIEVE = range(8)

SERVICE_LIST = ''' :خدمات مشاوره و همکاری

پایان نامه ۵ میلیون به بالا
پروپوزال ۱.۵ میلیون به بالا
آنالیز آماری ۵۰۰ هزار تا ۲ میلیون
نوشتن مقاله ۵ میلیون به بالا
پکیج کامل ۹ میلیون به بالا
گرافیکال ابسترکت ۵۰۰ هزار تومان به بالا
پیدا کردن ژورنال و سابمیت مقاله ۵۰۰ هزار تومان
چک کردن پلاجریسم ۲۵۰ هزار تومان
چک کردن پلاجریسم و پارافریز ۷۵۰ به بالا
چک و تصحیح گرامر متن انگلیسی ۵۰۰ هزار تومان
ثبت اختراع ۵ میلیون به بالا
پروپوزال فناوری ۲ میلیون به بالا

لازم به ذکر است خدمات بالا در
.حوزه نگارش می باشد . انجام کار عملی و میدانی ، غیر اخلاقی بوده و انجام نمی گیرد
'''

service_list = 'تعرفه کلی خدمات'
scientific = 'خدمات پژوهشی'
technology = 'خدمات فناوری'
channel = 'کانال تلگرامی راهین و ارتباط با ادمین'
scientific_service_keyboard = [['پایان نامه', 'پروپوزال', 'مقاله '],
                               ['پیدا کردن ژورنال و سابمیت', 'چک کردن پلاجریسم', 'گرافیکال ابسترکت'],
                               ['آنالیز آماری', 'پارافریزینگ', 'پکیج کامل دانشجویی، شامل تمامی موارد بالا']]
scientific_service_list = ['پایان نامه', 'پروپوزال', 'آنالیز آماری', 'مقاله','پیدا کردن ژورنال و سابمیت', 'چک کردن پلاجریسم', 'پارافریزینگ', 'پکیج کامل دانشجویی، شامل تمامی موارد بالا', 'گرافیکال ابسترکت']
technology_service_list = ['ثبت اختراع', 'پروپوزال فناوری']
article_list = ['پایان نامه', 'پروپوزال', 'مقاله', 'پکیج کامل دانشجویی، شامل تمامی موارد بالا']
no_article_list = ['پیدا کردن ژورنال و سابمیت', 'چک کردن پلاجریسم', 'پارافریزینگ', 'آنالیز آماری', 'ثبت اختراع', 'پروپوزال فناوری', 'گرافیکال ابسترکت']
article_type_list = ['مورد / شاهدی', 'مقطعی', 'کارآزمایی بالینی', 'توصیفی' ,'علوم پایه', 'کوهورت', 'بررسی بيماران', 'مروری']
article_type_keboard = [['مورد / شاهدی', 'مقطعی', 'کارآزمایی بالینی', 'توصیفی'],
                        [ 'علوم پایه', 'کوهورت', 'بررسی بيماران', 'مروری']]

# functions
# here ----------------------------------------------------------------------------------------------
def facts_2_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{k} - {v}' for k, v in user_data.items() if k != 'file_id']

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user to choose a service."""

    user_name = update.message.chat.username
    user_data = context.user_data
    user_data['choice'] = '@' + user_name
    user_data['username'] = user_data['choice']
    del user_data['choice']

    reply_keyboard = [[scientific, technology], [channel, service_list]]
    update.message.reply_text('!سلام، لطفا یکی از گزینه ها را انتخاب کنید',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               input_field_placeholder='نوع خدمت؟'),
                              parse_mode="markdown")

    return SERVICE_CHOOSE


def scientific_service(update: Update, context: CallbackContext) -> int:
    '''stores the service and asks the user to choose one of the scientific services'''
    reply_keyboard = scientific_service_keyboard
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['service'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user

    logger.info("the chosen service of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(':یکی از خدمات پژوهشی زیر را انتخاب کنید ',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                               one_time_keyboard=True,
                                                               input_field_placeholder='نوع خدمت پژوهشی؟'),
                              parse_mode="markdown")
    return TYPE_OF_ARTICLE


def technology_service(update: Update, context: CallbackContext) -> int:
    '''stores the service and asks the user to choose one of the technology services'''
    reply_keyboard = [technology_service_list]
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['service'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user
    logger.info("the chosen service of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(':یکی از خدمات فناوری زیر را انتخاب کنید ',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               input_field_placeholder=' نوع خدمت فناوری؟'),
                              parse_mode="markdown")
    return TYPE_OF_ARTICLE



def article(update: Update, context: CallbackContext) -> int:
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['service type'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user

    reply_keyboard = article_type_keboard
    update.message.reply_text('لطفا نوع مطالعه خود را مشخص کنید:',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               input_field_placeholder='نوع مطالعه؟'),
                              parse_mode="markdown")
    return TYPE_OF_SERVICE


def no_article(update: Update, context: CallbackContext) -> int:
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['service type'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user

    reply_keyboard = [['no type']]
    update.message.reply_text('لطفا جهت ادامه فرایند سابمیت دکمه no type را بزنید:',reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                              parse_mode="markdown")

    return TYPE_OF_SERVICE




def stype(update: Update, context: CallbackContext) -> int:
    """Stores the type of the chosen service and asks the user to pick a timing."""
    reply_keyboard = [['نیاز فوری', 'نیاز غیرفوری']]
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['article type'] = user_data['choice']
    del user_data['choice']

    user = update.message.from_user
    logger.info("the project type of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('.لطفا زمان تقریبی تحویل پروژه خود را مشخص کنید',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               input_field_placeholder='زمانبندی؟'),
                              parse_mode="markdown")

    return TIMINNG_OF_SERVICE


def timing(update: Update, context: CallbackContext) -> int:
    """Stores the chosen timing and asks for the title."""
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['timing'] = user_data['choice']
    del user_data['choice']

    user = update.message.from_user
    logger.info("timing of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('لطفا عنوان پروژه خود را مشخص کنید', parse_mode="markdown")

    return TITLE_OF_PROJECT


def title(update: Update, context: CallbackContext) -> int:
    """Stores the title and asks for a description of the project"""
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['title'] = user_data['choice']
    del user_data['choice']

    user = update.message.from_user
    logger.info("Location of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        ':لطفا در مورد پروژه خود توضیح دهید. توضیحات باید کامل باشند و تمام موارد درخواستی باید ذکر شوند',
        parse_mode="markdown")

    return DESCRIPTION_OF_PROJECT


def description(update: Update, context: CallbackContext) -> int:
    """Stores the description asks for the project file"""
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['description'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user
    logger.info("description of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        ' لطفا فایل کلی مربوط به پروژه خود را آپلود کنید (ترجیحا فایل زیپ). در صورت عدم وجود فایل /skip :را بزنید',
        parse_mode="markdown")

    return FILE


def pfile(update: Update, context: CallbackContext) -> int:
    '''stores the project file and ends the conversation'''
    user = update.message.from_user
    logger.info("description of %s: %s", user.first_name, update.message.text)
    project_file = update.message.document.get_file()
    fid = update.message.document.file_id
    path = project_file.download()

    user_data = context.user_data
    user_data['choice'] = fid
    user_data['file_id'] = user_data['choice']
    del user_data['choice']

    update.message.reply_text(' فایل دریافت شد. جهت تایید نهایی و ارسال به همکاران ما /send را بزنید',
                              parse_mode="markdown")

    return RECIEVE


def skip_file(update: Update, context: CallbackContext) -> int:
    '''skips the project file and ends the conversation'''
    user_data = context.user_data
    user_data['choice'] = 'NONE'
    user_data['file'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user
    logger.info("user %s did not send any file", user.first_name)
    update.message.reply_text(
        '.پروژه شما بدون فایل ارسالی با موفقیت ثبت شد.اطلاعات ثبت شده مورد بررسی قرار می گیرند و فایل نهایی پروژه توسط همکاران برای شما ارسال می شود',
        parse_mode="markdown")
    update.message.reply_text(f'{facts_2_str(user_data)}', parse_mode="markdown")
    context.bot.send_message(chat_id='@RahenTestBotChannel', text=f'{facts_2_str(user_data)}')

    return ConversationHandler.END


def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    fid = user_data['file_id']
    update.message.reply_text(
        'پروژه شما همراه با فایل ارسالی با موفقیت ثبت شد.اطلاعات ثبت شده مورد بررسی قرار می گیرند و هزینه و توضیحات نهایی پروژه توسط همکاران برای شما ارسال می گردد',
        parse_mode="markdown")
    update.message.reply_document(fid, caption=f'{facts_2_str(user_data)}')  # telegram.Bot.send_document
    context.bot.send_document(chat_id='@RahenTestBotChannel', document=fid, caption=f'{facts_2_str(user_data)}')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('خداحافظ دوست عزیز', reply_markup=ReplyKeyboardRemove(),
                              parse_mode="markdown")

    return ConversationHandler.END


def error(update: Update, context: CallbackContext) -> int:
    print(f'update {update} caused {context.error}')


def channel_func(update: Update, context: CallbackContext):
    update.message.reply_text('''
  آی دی کانال ما : t.me/RahenScience
  ارتباط با ما : @rahen_science''')


def service_list_func(update: Update, context: CallbackContext):
    update.message.reply_text(SERVICE_LIST)

# main function
# here ----------------------------------------------------------------------------------------------

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN,
                      use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Add conversation handler with the states TYPE_OF_SERVICE, TIMINNG_OF_SERVICE, TITLE_OF_PROJECT, DESCRIPTION_OF_PROJECT and FILE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SERVICE_CHOOSE: [MessageHandler(Filters.regex(f'^({scientific})$'), scientific_service),
                             # basically it is like an if/else statement
                             MessageHandler(Filters.regex(f'^({technology})$'), technology_service),
                             # you are determining which function to be run
                             MessageHandler(Filters.regex(f'^({channel})$'), channel_func),
                             # after getting a particular message and the state is the output message
                             MessageHandler(Filters.regex(f'^({service_list})$'), service_list_func)],
            # comming from the functions (it is spitted out by its associated function)

            TYPE_OF_ARTICLE: [MessageHandler(Filters.regex('^(' + '|'.join(article_list) + ')$'), article),
                              MessageHandler(Filters.regex('^(' + '|'.join(no_article_list) + ')$'), no_article)],

            TYPE_OF_SERVICE: [MessageHandler(Filters.regex('^(no type|' + '|'.join(article_type_list) + ')$'), stype)],

            TIMINNG_OF_SERVICE: [MessageHandler(Filters.regex('^(نیاز فوری|نیاز غیرفوری)$'), timing)],

            TITLE_OF_PROJECT: [MessageHandler(Filters.text & ~Filters.command, title)],
            # when the user dont have to choose anything and simply
            # want to type some text or command you use this expresion
            DESCRIPTION_OF_PROJECT: [MessageHandler(Filters.text & ~Filters.command, description)],

            FILE: [MessageHandler(Filters.document, pfile), CommandHandler('skip', skip_file)],
            # if you expect a document (any) as an output, you use this expresion

            RECIEVE: [CommandHandler('send', received_information)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_webhook(listen='0.0.0.0', port=os.environ.get('PORT', 443),
                          url_path=TOKEN,
                          webhook_url='https://rahen-science-app.herokuapp.com/'+TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
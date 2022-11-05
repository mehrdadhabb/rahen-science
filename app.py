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

LANGUAGE, SERVICE_CHOOSE, TYPE_OF_ARTICLE, TYPE_OF_SERVICE, TIMINNG_OF_SERVICE, TITLE_OF_PROJECT, DESCRIPTION_OF_PROJECT, PHONE, FILE, RECIEVE = range(
    10)

SERVICE_LIST_photo = {'fa': '/content/fa.jpg',
                      'en': '/content/en.jpg'}
service_list = {'fa': 'تعرفه کلی خدمات',
                'en': 'Pricing'}
scientific = {'fa': 'خدمات پژوهشی',
              'en': 'Scientific Service'}
technology = {'fa': 'خدمات فناوری',
              'en': 'Technology Service'}
channel = {'fa': 'کانال تلگرامی راهین و ارتباط با ادمین',
           'en': 'Rahen Telegram Channel and admin ID'}

scientific_service_keyboard = {'fa': [['پایان نامه', 'پروپوزال', 'مقاله '],
                                      ['پیدا کردن ژورنال و سابمیت', 'چک کردن پلاجریسم', 'گرافیکال ابسترکت'],
                                      ['آنالیز آماری', 'پارافریزینگ', 'پکیج کامل دانشجویی، شامل تمامی موارد بالا']],
                               'en': [['Thesis', 'Proposal', 'Article'],
                                      ['Journal Finding and Submission', 'Plagiarism Check', 'Graphical Abstract'],
                                      ['Statistical Analysis', 'Paraphrasing', 'Full Package, All of the Above']]}

scientific_service_list = {
    'fa': ['پایان نامه', 'پروپوزال', 'آنالیز آماری', 'مقاله', 'پیدا کردن ژورنال و سابمیت', 'چک کردن پلاجریسم',
           'پارافریزینگ', 'پکیج کامل دانشجویی، شامل تمامی موارد بالا', 'گرافیکال ابسترکت'],
    'en': ['Thesis', 'Proposal', 'Statistical Analysis', 'Article',
           'Journal Finding and Submission', 'Plagiarism Check', 'Paraphrasing', 'Full Package, All of the Above',
           'Graphical Abstract']}

technology_service_list = {'fa': ['ثبت اختراع', 'پروپوزال فناوری'],
                           'en': ['Patent', 'Technology Proposal']}

article_list = {'fa': ['پایان نامه', 'پروپوزال', 'مقاله', 'پکیج کامل دانشجویی، شامل تمامی موارد بالا'],
                'en': ['Thesis', 'Proposal', 'Article', 'Full Package, All of the Above']}

no_article_list = {'fa': ['پیدا کردن ژورنال و سابمیت', 'چک کردن پلاجریسم', 'پارافریزینگ', 'آنالیز آماری', 'ثبت اختراع',
                          'پروپوزال فناوری', 'گرافیکال ابسترکت'],
                   'en': ['Journal Finding and Submission', 'Plagiarism Check', 'Paraphrasing', 'Statistical Analysis',
                          'Patent', 'Technology Proposal', 'Graphical abstract']}

article_type_list = {
    'fa': ['مورد / شاهدی', 'مقطعی', 'کارآزمایی بالینی', 'توصیفی', 'علوم پایه', 'کوهورت', 'بررسی بيماران', 'مروری'],
    'en': ['Case / Control', 'Cross-Sectional', 'Clinical Trial', 'Descriptive', 'Experimental', 'Cohort', 'Case Study',
           'Review']}

article_type_keboard = {'fa': [['مورد / شاهدی', 'مقطعی', 'کارآزمایی بالینی', 'توصیفی'],
                               ['علوم پایه', 'کوهورت', 'بررسی بيماران', 'مروری']],
                        'en': [['Case / Control', 'Cross-Sectional', 'Clinical Trial', 'Descriptive'],
                               ['Experimental', 'Cohort', 'Case Study', 'Review']]}

service_choose_txt = {'fa': '!سلام، لطفا یکی از گزینه ها را انتخاب کنید',
                      'en': 'Hi, please choose one of the options'}
scientific_service_txt = {'fa': 'یکی از خدمات پژوهشی زیر را انتخاب کنید: ',
                          'en': 'Choose one of the following scientific services:'}
technology_service_txt = {'fa': 'یکی از خدمات فناوری زیر را انتخاب کنید: ',
                          'en': 'Choose one of the following technology services:'}
article_txt = {'fa': 'لطفا نوع مطالعه خود را مشخص کنید:',
               'en': 'Please specify the type of your study:'}
no_article_txt = {'fa': 'لطفا جهت ادامه فرایند سابمیت دکمه no type را بزنید:',
                  'en': 'Please click the no type button to continue the submission process:'}
urgency_keyboard = {'fa': [['نیاز فوری', 'نیاز غیرفوری']],
                    'en': [['urgent', 'non-urgent']]}
stype_txt = {'fa': '.لطفا زمان تقریبی تحویل پروژه خود را مشخص کنید',
             'en': 'Please indicate the approximate time you want your project delivered:'}
timing_txt = {'fa': 'لطفا عنوان پروژه خود را مشخص کنید: ',
              'en': 'Please specify the title of your project: '}
title_txt = {'fa': 'لطفا در مورد پروژه خود توضیح دهید. توضیحات باید کامل باشند و تمام موارد درخواستی باید ذکر شوند: ',
             'en': 'Please describe your project. Descriptions should include all the requested items: '}
description_txt = {
    'fa': 'لطفا جهت ارتباط همکاران ما با شما در خصوص پروژه و هماهنگی های بعدی، شماره موبایل متصل به حساب تلگرامی خود را تایپ کنید: ',
    'en': 'For further arrangements regarding your project please provide us with the phone number connected to your Telegram account: '}
phone_num_txt = {
    'fa': ' لطفا فایل کلی مربوط به پروژه خود را آپلود کنید (ترجیحا فایل زیپ). در صورت عدم وجود فایل /skip :را بزنید',
    'en': 'Please upload the overall file of your project (preferably zip file). If there is no file, press /skip.'}
pfile_txt = {'fa': ' فایل دریافت شد. جهت تایید نهایی و ارسال به همکاران ما /send را بزنید',
             'en': 'File received. Press /send for final approval and your information will be sent to our colleagues.'}
skip_file_txt = {
    'fa': 'پروژه شما بدون فایل ارسالی با موفقیت ثبت شد.اطلاعات ثبت شده مورد بررسی قرار می گیرند و هزینه و توضیحات نهایی اجرای پروژه توسط همکاران برای شما ارسال می شود.',
    'en': "Your project has been successfully submitted without the file. The registered information will be checked and the final cost and description of the project implementation will be sent to you by our colleagues."}
recieved_info_txt = {
    'fa': 'پروژه شما همراه با فایل ارسالی با موفقیت ثبت شد.اطلاعات ثبت شده مورد بررسی قرار می گیرند و هزینه و توضیحات نهایی پروژه توسط همکاران برای شما ارسال می گردد',
    'en': 'Your project has been successfully submitted along with the file. The registered information will be checked and the final cost and description of the project implementation will be sent to you by our colleagues.'}
bye_txt = {'fa': 'خداحافظ دوست عزیز',
           'en': 'farewell dear friend'}
channel_txt = {'fa': '''
  آی دی کانال ما : t.me/RahenScience
  ارتباط با ما : @rahen_science''',
               'en': ''''
   Our Channel ID: t.me/RahenScience
   Contact us: @rahen_science'''}


# functions
# here ----------------------------------------------------------------------------------------------
def facts_2_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{k} - {v}' for k, v in user_data.items() if k != 'file_id']
    print('the shit was created')
    return "\n".join(facts).join(['\n', '\n'])


lang = ['en']


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user to choose a service."""
    reply_keyboard = [['en', 'fa']]
    update.message.reply_text('Please choose the bot language:',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return LANGUAGE


def language_choose(update: Update, context: CallbackContext) -> int:
    lang[0] = update.message.text

    reply_keyboard = [[scientific[lang[0]], technology[lang[0]]], [channel[lang[0]], service_list[lang[0]]]]
    update.message.reply_text(service_choose_txt[lang[0]],
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SERVICE_CHOOSE


def scientific_service(update: Update, context: CallbackContext) -> int:
    '''stores the service and asks the user to choose one of the scientific services'''
    reply_keyboard = scientific_service_keyboard[lang[0]]
    txt = update.message.text

    user_data = context.user_data
    user_name = update.message.chat.username
    try:
        user_data['username'] = '@' + user_name
    except:
        user_data['username'] = user_name
    user_data['choice'] = txt
    user_data['service'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user

    logger.info("the chosen service of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(scientific_service_txt[lang[0]],
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                               one_time_keyboard=True))
    return TYPE_OF_ARTICLE


def technology_service(update: Update, context: CallbackContext) -> int:
    '''stores the service and asks the user to choose one of the technology services'''
    reply_keyboard = [technology_service_list[lang[0]]]
    txt = update.message.text

    user_data = context.user_data
    user_data['username'] = update.message.chat.username
    user_data['choice'] = txt
    user_data['service'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user
    logger.info("the chosen service of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(technology_service_txt[lang[0]],
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TYPE_OF_ARTICLE


def article(update: Update, context: CallbackContext) -> int:
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['service type'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user

    reply_keyboard = article_type_keboard[lang[0]]
    update.message.reply_text(article_txt[lang[0]],
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TYPE_OF_SERVICE


def no_article(update: Update, context: CallbackContext) -> int:
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['service type'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user

    reply_keyboard = [['no type']]
    update.message.reply_text(no_article_txt[lang[0]],
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return TYPE_OF_SERVICE


def stype(update: Update, context: CallbackContext) -> int:
    """Stores the type of the chosen service and asks the user to pick a timing."""
    reply_keyboard = urgency_keyboard[lang[0]]
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['article type'] = user_data['choice']
    del user_data['choice']

    user = update.message.from_user
    logger.info("the project type of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(stype_txt[lang[0]],
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

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
    update.message.reply_text(timing_txt[lang[0]])

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
    update.message.reply_text(title_txt[lang[0]])

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
    update.message.reply_text(description_txt[lang[0]])

    return PHONE


def phone_num(update: Update, context: CallbackContext) -> int:
    txt = update.message.text

    user_data = context.user_data
    user_data['choice'] = txt
    user_data['phone'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user
    logger.info("phone number of %s: %s", user.first_name, update.message.text)

    update.message.reply_text(phone_num_txt[lang[0]])

    return FILE


def pfile(update: Update, context: CallbackContext) -> int:
    '''stores the project file and ends the conversation'''

    user = update.message.from_user
    logger.info("phone number of %s: %s", user.first_name, update.message.text)
    project_file = update.message.document.get_file()
    fid = update.message.document.file_id
    path = project_file.download()

    user_data = context.user_data
    user_data['choice'] = fid
    user_data['file_id'] = user_data['choice']
    del user_data['choice']

    update.message.reply_text(pfile_txt[lang[0]])

    return RECIEVE


def skip_file(update: Update, context: CallbackContext) -> int:
    '''skips the project file and ends the conversation'''
    user_data = context.user_data
    user_data['choice'] = 'NONE'
    user_data['file'] = user_data['choice']
    del user_data['choice']
    user = update.message.from_user
    logger.info("user %s did not send any file", user.first_name)
    update.message.reply_text(skip_file_txt[lang[0]])
    update.message.reply_text(f'{facts_2_str(user_data)}')
    context.bot.send_message(chat_id='@RahenScienceChannel', text=f'{facts_2_str(user_data)}')

    return ConversationHandler.END


def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    fid = user_data['file_id']
    update.message.reply_text(recieved_info_txt[lang[0]])
    update.message.reply_document(fid, caption=f'{facts_2_str(user_data)}')  # telegram.Bot.send_document
    context.bot.send_document(chat_id='@RahenScienceChannel', document=fid, caption=f'{facts_2_str(user_data)}')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(bye_txt[lang[0]], reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update: Update, context: CallbackContext) -> int:
    print(f'update {update} caused {context.error}')


def channel_func(update: Update, context: CallbackContext):
    update.message.reply_text(channel_txt[lang[0]])


def service_list_func(update: Update, context: CallbackContext):
    update.message.reply_photo(open(SERVICE_LIST_photo[lang[0]], 'rb'))


# main function
# here ----------------------------------------------------------------------------------------------

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN,
                      use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [MessageHandler(Filters.regex('^(en|fa)$'), language_choose)],

            SERVICE_CHOOSE: [
                MessageHandler(Filters.regex('^(' + '|'.join([scientific['en']] + [scientific['fa']]) + ')$'),
                               scientific_service),
                # basically it is like an if/else statement
                MessageHandler(Filters.regex('^(' + '|'.join([technology['en']] + [technology['fa']]) + ')$'),
                               technology_service),
                # you are determining which function to be run
                MessageHandler(Filters.regex('^(' + '|'.join([channel['en']] + [channel['fa']]) + ')$'), channel_func),
                # after getting a particular message and the state is the output message
                MessageHandler(Filters.regex('^(' + '|'.join([service_list['en']] + [service_list['fa']]) + ')$'),
                               service_list_func)],
            # comming from the functions (it is spitted out by its associated function)

            TYPE_OF_ARTICLE: [
                MessageHandler(Filters.regex('^(' + '|'.join(article_list['en'] + article_list['fa']) + ')$'), article),
                MessageHandler(Filters.regex('^(' + '|'.join(no_article_list['en'] + no_article_list['fa']) + ')$'),
                               no_article)],

            TYPE_OF_SERVICE: [MessageHandler(
                Filters.regex('^(no type|' + '|'.join(article_type_list['en'] + article_type_list['fa']) + ')$'),
                stype)],

            TIMINNG_OF_SERVICE: [MessageHandler(
                Filters.regex('^(no type|' + '|'.join(urgency_keyboard['en'][0] + urgency_keyboard['fa'][0]) + ')$'),
                timing)],

            TITLE_OF_PROJECT: [MessageHandler(Filters.text & ~Filters.command, title)],
            # when the user dont have to choose anything and simply
            # want to type some text or command you use this expresion
            DESCRIPTION_OF_PROJECT: [MessageHandler(Filters.text & ~Filters.command, description)],

            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone_num)],

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
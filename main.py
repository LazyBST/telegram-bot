from dotenv import load_dotenv
load_dotenv()

import logging
from operator import itemgetter
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackContext, Application
import os
from src.services.pdfGenerator import GenerateFromTemplate
from src.constants import MESSAGES, OUTPUT_FILE_NAME
from src.utils import isValidDate, isValidAge
import asyncio
from flask import Flask, request, jsonify

TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')

loop = asyncio.get_event_loop()

# Initialize the logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

INIT, NAME, AGE, DISEASE, ILLNESS_START_DATE, ILLNESS_END_DATE = range(6)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(MESSAGES['START'])
    return INIT
    
async def help_handler(update: Update, context):
    await update.message.reply_text(MESSAGES['HELP'])

async def initHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text != "I am sick":
        await update.message.reply_text(MESSAGES['START'])
        return INIT
    
    response = MESSAGES['NAME']
    await update.message.reply_text(response)
    return NAME

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'update {update} caused an error :: {context.error}')
    
async def nameHandler(update: Update, context: CallbackContext) -> int:
    name = update.message.text
    context.user_data['name'] = name
    await update.message.reply_text(MESSAGES['AGE'].format(name=name))
    return AGE
    
async def ageHandler(update: Update, context: CallbackContext) -> int:
    age = update.message.text
    
    if not isValidAge(age):
        await update.message.reply_text(MESSAGES['INVALID_AGE'])
        return AGE
    
    context.user_data['age'] = age
    await update.message.reply_text(MESSAGES['DISEASE'])
    return DISEASE

async def diseaseHandler(update: Update, context: CallbackContext) -> int:
    disease = update.message.text
    context.user_data['disease'] = disease
    await update.message.reply_text(MESSAGES['START_DATE'])
    return ILLNESS_START_DATE

async def illnessStartDateHandler(update: Update, context: CallbackContext) -> int:
    startDate = update.message.text
    if not isValidDate(startDate):
        await update.message.reply_text(MESSAGES['START_DATE'])
        return ILLNESS_START_DATE
    
    context.user_data['illnessStartDate'] = startDate
    await update.message.reply_text(MESSAGES['END_DATE'])
    return ILLNESS_END_DATE

async def illnessEndDateHandler(update: Update, context: CallbackContext) -> int:
    endDate = update.message.text
    if not isValidDate(endDate):
        await update.message.reply_text(MESSAGES['END_DATE'])
        return ILLNESS_END_DATE
    
    context.user_data['illnessEndDate'] = endDate
    name, age, disease, startDate, endDate = itemgetter('name', 'age', 'disease', 'illnessStartDate', 'illnessEndDate')(context.user_data)
    await update.message.reply_text(MESSAGES["END"])
    pdfStream = GenerateFromTemplate.buildMedical(name, age, disease, startDate, endDate)
    await update.message.reply_document(pdfStream, filename=OUTPUT_FILE_NAME)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(MESSAGES['CANCEL'], reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def bot_handler(event=None, context=None):
    try:
        bot = Application.builder().token(TOKEN).build()
        # await bot.initialize()
        
        # Commands
        bot.add_handler(CommandHandler('help', help_handler))
        
        # Errors
        bot.add_error_handler(error_handler)
        
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start_handler)],
            states={
                INIT: [MessageHandler(filters.TEXT & (~filters.COMMAND), initHandler)],
                NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), nameHandler)],
                AGE: [MessageHandler(filters.TEXT & (~filters.COMMAND), ageHandler)],
                DISEASE: [MessageHandler(filters.TEXT & (~filters.COMMAND), diseaseHandler)],
                ILLNESS_START_DATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), illnessStartDateHandler)],
                ILLNESS_END_DATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), illnessEndDateHandler)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )

        bot.add_handler(conv_handler)
        bot.run_polling()
        
    except Exception as e:
        logger.error("Error in bot_handler: %s", str(e))

# def lambda_handler(event=None, context=None):
#     global loop
#     if loop.is_closed():
#         loop = asyncio.new_event_loop()
#     return loop.run_until_complete(bot_handler(event, context))

if __name__ == '__main__':
    bot_handler()

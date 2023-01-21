from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from main import ShiftPlan
"""
Dieser Bot soll einen Schichtplan erstellen. Dazu Güßt der Bot den User und 
fragt nach den Daten die er benötigt um den Schichtplan zu erstellen.
Es wird ein Startdatum, Anzahl an tagen, Anzahl der Schichten pro Tag, die 
Namen und optional ein Zeitformat benötigt.
Danach Zeit der Bot den Schichtplan an und nimmt änderungen entgegen.
Die Änderungen werden durch die main.py bearbeitet und der Bot gibt den 
akuellen Schichtplan aus.
"""

async def create_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fragat alle daten ab um den Schichtplan zu erstellen"""
    await update.message.reply_text(f'Hello '
                                    f'{update.effective_user.first_name} \n'
                                    f'Hier kannst du deinen Schichtplan '
                                    f'erstellen.\n dazu benötige ich ein '
                                    f'paar Daten von dir.\n Wann soll der '
                                    f'Sicherplan starten? Bitte gib das '
                                    f'Datum im Format JJJJ-MM-TT ein.')
    # user Imput abfragen
    # Datum
    datum = await context.get_user_input()
    # Anzahl an Tagen
    await update.message.reply_text(f'Wie viele Tage soll der Schichtplan '
                                    f'haben?')
    tage = await context.get_user_input()
    # Anzahl an Schichten pro Tag
    await update.message.reply_text(f'Wie viele Schichten soll es pro Tag geben?')
    schichten = await context.get_user_input()
    # Namen
    names = update.CHAT_MEMBER
    # Zeitformat
    # await update.message.reply_text(f'In welchem Format soll die Zeit '
    #                                 f'angegeben?\n'
    #                                 f'Voreingestellt ist das iso Format. '
    #                                 f'"%Y-%m-%d"\n Du aber auch german('
    #                                 f'"%d.%m.%Y") oder us("%m/%d/%Y") wählen.\n'
    #                                 f'Darüber hinaus kannst du auch dein '
    #                                 f'eigenes format angeben.')
    # zeitformat = await context.get_user_input()
    # Schichtplan erstellen
    sichplan = ShiftPlan(datum, tage, schichten, names,)
    # Schichtplan ausgeben
    rendered_schedule = sichplan.render_schedule_table()
    await update.message.reply_text(f'Der Schichtplan sieht so aus:\n{rendered_schedule}')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Says hello to the user."""
    await update.message.reply_text(f'Hello '
                                    f'{update.effective_user.first_name} \n'
                                    f'Ich bin ein Bot der dir deinen Schichtplan '
                                    f'erstellt.\n'
                                    f'Wenn du einen Schichtplan erstellen '
                                    f'möchtest, dann gib /create_schedule ein.')


app = ApplicationBuilder().token(os.environ['TELEGRAM_API_KEY']).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("create_schedule", create_schedule))


app.run_polling()
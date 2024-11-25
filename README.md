from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Definir el token de tu bot
TOKEN = '7287004742:AAHiGlePqw_tus0iN2ZOK8_tBl8tnJ_ADgA'

# Definir los estados de la conversación
CAPITAL = 1
CUOTAS = 2

# Función de inicio
def start(update: Update, context: CallbackContext):
    update.message.reply_text('¡Hola! Soy tu bot de Surebets. ¿Cuánto es tu capital máximo para invertir?')
    return CAPITAL

# Función para recibir el capital máximo
def receive_capital(update: Update, context: CallbackContext):
    try:
        # Guardar el capital máximo proporcionado por el usuario
        capital_maximo = float(update.message.text)
        context.user_data['capital_maximo'] = capital_maximo

        update.message.reply_text(f"Capital máximo recibido: {capital_maximo}. Ahora, ¿cuál es el número de cuotas?")

        return CUOTAS  # Cambiar al siguiente paso

    except ValueError:
        update.message.reply_text("Por favor, ingresa un número válido para el capital máximo.")
        return CAPITAL  # Volver a pedir el capital

# Función para recibir las cuotas
def receive_cuotas(update: Update, context: CallbackContext):
    try:
        # Guardar las cuotas proporcionadas por el usuario
        cuotas = int(update.message.text)
        context.user_data['cuotas'] = cuotas

        update.message.reply_text(f"Cuotas recibidas: {cuotas}. ¡Gracias! Ahora puedes usar el bot.")

        return -1  # Fin de la conversación

    except ValueError:
        update.message.reply_text("Por favor, ingresa un número válido para las cuotas.")
        return CUOTAS  # Volver a pedir las cuotas

# Función para manejar las respuestas no reconocidas
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("No entiendo lo que dices. Por favor, responde con los datos solicitados.")

def main():
    # Crear el Updater y el Dispatcher
    updater = Updater(TOKEN)

    # Obtener el dispatcher
    dispatcher = updater.dispatcher

    # Añadir los manejadores de comandos y mensajes
    dispatcher.add_handler(CommandHandler('start', start))

    # Añadir los manejadores para las conversaciones
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_capital, pass_user_data=True))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_cuotas, pass_user_data=True))

    # Arrancar el bot
    updater.start_polling()

    # Esperar que el bot termine
    updater.idle()

if __name__ == '__main__':
    main()

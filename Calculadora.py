from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Función para dividir el texto en fragmentos más pequeños
def dividir_mensaje(texto, limite=4096):
    return [texto[i:i+limite] for i in range(0, len(texto), limite)]

# Comando /sure
def sure(update: Update, context: CallbackContext) -> None:
    try:
        # Extraer los argumentos
        args = context.args
        if len(args) != 3:
            update.message.reply_text("Uso incorrecto. Ejemplo: /sure 100 2.20 2.05")
            return

        # Convertir argumentos
        capital_maximo = float(args[0])
        cuota_1 = float(args[1])
        cuota_2 = float(args[2])

        # Determinar la cuota mayor y menor
        mayor = max(cuota_1, cuota_2)
        menor = min(cuota_1, cuota_2)

        # Calcular la división (mayor entre menor)
        division = mayor / menor

        # Realizar la iteración y filtrar resultados válidos
        numero = 1
        resultados_exactos = []  # Lista para resultados exactos
        resultados_inexactos = []  # Lista para resultados inexactos
        while True:
            multiplicacion = numero * division
            suma = numero + multiplicacion
            # Verificar si la suma es un número entero (tolerancia de 0.0001)
            if abs(suma - round(suma)) < 0.0001:
                resultados_exactos.append(f"{numero} × {division:.4f} = {multiplicacion:.4f}, Suma = {int(suma)}")
            else:
                # Clasificar inexactos por la diferencia al número entero más cercano
                diferencia = abs(suma - round(suma))
                resultados_inexactos.append((numero, division, multiplicacion, suma, diferencia))
            if suma > capital_maximo:
                break
            numero += 1

        # Guardar los resultados en el contexto del usuario
        context.user_data['resultados_exactos'] = resultados_exactos
        context.user_data['resultados_inexactos'] = resultados_inexactos
        context.user_data['capital_maximo'] = capital_maximo

        # Información adicional a mostrar
        info_detallada = (
            f"Cuota 1: {cuota_1}\n"
            f"Cuota 2: {cuota_2}\n"
            f"Capital máximo: {capital_maximo}\n"
            f"Cuota mayor: {mayor}\n"
            f"Cuota menor: {menor}\n"
            f"División (Mayor / Menor): {division:.4f}\n"
        )

        # Verificar si hubo resultados exactos
        if resultados_exactos:
            resultados_texto = "\n".join(resultados_exactos)
            mensaje = f"{info_detallada}\nResultados exactos (suma sin decimales):\n{resultados_texto}\n\nSe detuvo porque la suma superó el capital máximo: {capital_maximo}"
        else:
            mensaje = f"{info_detallada}\nNo se encontraron resultados exactos con suma sin decimales."

        # Dividir el mensaje largo en fragmentos más pequeños
        fragmentos = dividir_mensaje(mensaje)

        # Enviar cada fragmento por separado
        for fragmento in fragmentos:
            update.message.reply_text(fragmento)

    except ValueError:
        update.message.reply_text("Por favor, introduce números válidos.")

# Responder con resultados inexactos (cuando el usuario dice "otros")
def otros(update: Update, context: CallbackContext) -> None:
    try:
        # Obtener los montos inexactos previos
        montos_inexactos = context.user_data.get('resultados_inexactos', [])
        
        if not montos_inexactos:
            update.message.reply_text("No hay resultados inexactos previos. Usa el comando /sure para obtener resultados.")
            return

        # Ordenar los montos inexactos por la menor diferencia con el número entero más cercano
        montos_inexactos.sort(key=lambda x: x[4])  # Ordenar por la diferencia

        # Mostrar los montos inexactos clasificados sin la diferencia
        resultados_texto = ""
        for monto in montos_inexactos:
            numero, division, multiplicacion, suma, _ = monto  # Ignoramos la diferencia
            resultados_texto += f"{numero} × {division:.4f} = {multiplicacion:.4f}, Suma = {suma:.4f}\n"
            # Limitar la cantidad de resultados a enviar por mensaje
            if len(resultados_texto) > 3500:  # Si excede 3500 caracteres, enviamos lo acumulado y comenzamos otro
                fragmentos = dividir_mensaje(resultados_texto)
                for fragmento in fragmentos:
                    update.message.reply_text(f"Resultados inexactos (ordenados por la menor diferencia con el número entero más cercano):\n{fragmento}")
                resultados_texto = ""  # Limpiamos el contenido acumulado

        # Enviar el resto si no se excede el límite
        if resultados_texto:
            fragmentos = dividir_mensaje(resultados_texto)
            for fragmento in fragmentos:
                update.message.reply_text(f"Resultados inexactos (ordenados por la menor diferencia con el número entero más cercano):\n{fragmento}")

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Función principal para configurar el bot
def main():
    # Reemplaza este token con tu token real
    TOKEN = "7616517707:AAEPFEwac9DyZ6gddLj6xtory6egCWKG-2w"
    updater = Updater(TOKEN)

    # Añadir manejadores de comandos
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("sure", sure))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, otros))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

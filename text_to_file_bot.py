from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import os

# Define the file types
FILE_TYPES = ["TXT", "JSON", "CSV", "HTML", "CSS", "MD"]

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any text, and I'll ask you which file type you want!")

# Handle text messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    context.user_data["text"] = user_text  # Store the text for later use

    # Create inline buttons for file types
    keyboard = [
        [InlineKeyboardButton(file_type, callback_data=file_type)]
        for file_type in FILE_TYPES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Reply with the message and buttons
    await update.message.reply_text(
        f"Which type of file you need for this text?\n\nYour text: {user_text}",
        reply_markup=reply_markup
    )

# Handle button callbacks
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    file_type = query.data
    user_text = context.user_data.get("text", "")  # Retrieve the stored text

    await query.answer(f"You selected: {file_type}")

    # Create the file based on the selected format
    file_path = f"output.{file_type.lower()}"
    try:
        if file_type == "TXT":
            with open(file_path, "w") as file:
                file.write(user_text)
        elif file_type == "JSON":
            import json
            data = {"text": user_text}
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        elif file_type == "CSV":
            import csv
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([user_text])
        elif file_type == "HTML":
            with open(file_path, "w") as file:
                file.write(f"<html><body><p>{user_text}</p></body></html>")
        elif file_type == "CSS":
            with open(file_path, "w") as file:
                file.write(f"/* CSS File */\n\nbody {{\n\tcontent: '{user_text}';\n}}")
        elif file_type == "MD":
            with open(file_path, "w") as file:
                file.write(f"# Markdown File\n\n{user_text}")

        # Send the file to the user
        with open(file_path, "rb") as file:
            await query.message.reply_document(document=file, caption=f"Here is your {file_type} file!")

    except Exception as e:
        await query.message.reply_text(f"Failed to create the file: {e}")
    finally:
        # Clean up the file
        if os.path.exists(file_path):
            os.remove(file_path)

# Main function to run the bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token("8198647351:AAGJwoDwAZFHyqRBQTU03taT99ynF6HuPW0").build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CallbackQueryHandler(handle_button))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
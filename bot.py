import os
import json
import random
from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

with open ("vibe_db.json" , "r", encoding="utf-8") as f:
    VIBE_DB = json.load(f)

# Updated initialization based on your catch
client = genai.Client(api_key=GEMINI_API_KEY)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # 1. Immediate feedback so you know the bot received it
    await update.message.reply_text("Drafting...")

    # 2. The Vibe Engine: Grab 5 random past tweets to set the context
    # We use min() just in case your JSON has fewer than 5 tweets
    sample_vibes = random.sample(VIBE_DB, min(5, len(VIBE_DB)))
    vibe_text = "\n".join([f"- {v}" for v in sample_vibes])
    await update.message.reply_text(f"🔍 Context Used:\n{vibe_text}")

    # 3. The Instruction Set
    prompt = f"""
        You are a ghostwriter for a pragmatic developer. I am going to give you a raw thought.
        Your job is to translate it into a tweet that sounds exactly like me.

        Here is my actual personality based on my past tweets:
        {vibe_text}

        My raw thought/update:
        "{user_input}"

        Give me 3 distinct variations based on these exact personas:
        1. [The Builder]: Frustrated by the friction of building, but optimistically sarcastic because the thing is eventually getting built.
        2. [The Raw Wisdom Speaker]: Casual, street-smart developer wisdom. Everything is stated with a heavy layer of irony.
        3. [The Rational Doomer]: A pessimist who uses sensationalist, dramatic language to describe the situation, but the underlying logic and reasoning are completely sound and grounded in reality.

        CRITICAL RULES:
        - Sound like a guy in his 20s who builds things. 
        - NEVER use corporate, robotic, or academic words (no "facilitate," "metrics," "optimal," "utilize," etc.).
        - Keep it under 280 characters per variation.
        - Plain text only. NO hashtags. NO emojis unless they match the vibe examples.
        """

    try:
        # 4. Your updated 2.5-flash call
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        # Send the generated drafts back to your Telegram
        await update.message.reply_text(response.text)

    except Exception as e:
        # If the API fails or errors out, print the error to Telegram so you can debug
        await update.message.reply_text(f"Generation failed: {e}")


def main():
    print("Bot is live. Press Ctrl+C in terminal to stop.")

    # Build the Telegram app
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Tell the app to route all text messages to our handle_message function
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling (listening for messages)
    app.run_polling()


if __name__ == '__main__':
    main()
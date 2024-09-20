import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler
from scraper import parse_robota_ua_resume, parse_work_ua_resume
from utils import sort_resumes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


# Async function for the /start command
async def start(update: Update, context):
    await update.message.reply_text("Welcome to the Resume Finder bot! Use /search <job title> to find resumes.")


# Async function for the /search command
async def search(update: Update, context):
    target_job = " ".join(context.args) or "Data Scientist"

    # Scrape both job websites
    resumes = parse_robota_ua_resume() + parse_work_ua_resume()

    # Sort the resumes by relevance
    sorted_resumes = sort_resumes(resumes, target_job, min_experience=2, required_skills=["Python", "SQL"])

    # Show the top 5 resumes
    for resume in sorted_resumes[:5]:
        await update.message.reply_text(f"Name: {resume.name}, Job: {resume.job_position}, Salary: {resume.salary} грн")


# Main function to start the bot
def main():
    # Create the Application object with your bot token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the /start and /search handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))

    # Use application.run_polling() to start polling without closing the event loop
    application.run_polling()


if __name__ == "__main__":
    # Check if an event loop is already running
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If the event loop is already running, run the bot directly in the current loop
            main()
        else:
            # If no event loop is running, start the bot in a new loop
            asyncio.run(main())
    except RuntimeError:
        # Handle cases where no event loop is found and start one
        asyncio.run(main())

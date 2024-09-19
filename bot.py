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
async def main():
    # Create the Application object with your bot token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the /start and /search handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))

    # Start polling the bot
    await application.run_polling()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If event loop is already running, run the main function directly
            loop.create_task(main())
        else:
            # If no event loop is running, start a new one
            loop.run_until_complete(main())
    except RuntimeError:
        # In case of no event loop found, create a new one using asyncio.run()
        asyncio.run(main())

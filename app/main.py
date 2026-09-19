from fastapi import FastAPI, Request, Header, HTTPException
from dotenv import load_dotenv

import os
import httpx

from .database import engine, Base, SessionLocal
from .models import TelegramMessage
from .agent import ask_agent


load_dotenv()


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# ENVIRONMENT VARIABLES
# --------------------------------------------------

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)




if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN is missing in .env"
    )


# --------------------------------------------------
# FASTAPI
# --------------------------------------------------

app = FastAPI(
    title="Telegram AI Supply Chain Agent"
)


# --------------------------------------------------
# TELEGRAM API
# --------------------------------------------------

async def send_telegram_message(
    chat_id: int,
    text: str
):

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            url,
            json=payload
        )

        response.raise_for_status()


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "status": "running",
        "service": "Telegram AI Supply Chain Agent"
    }


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# TELEGRAM WEBHOOK
# --------------------------------------------------

@app.post("/telegram-webhook")
async def telegram_webhook(
    request: Request
):

    # ----------------------------------------------
    # VERIFY TELEGRAM SECRET
    # ----------------------------------------------

    


    # ----------------------------------------------
    # GET TELEGRAM UPDATE
    # ----------------------------------------------

    update = await request.json()

    message = update.get("message")

    if not message:

        return {
            "status": "ignored"
        }


    # ----------------------------------------------
    # GET USER DATA
    # ----------------------------------------------

    chat = message.get("chat", {})

    chat_id = chat.get("id")

    user = message.get("from", {})

    telegram_user_id = str(
        user.get("id")
    )

    username = user.get(
        "username"
    )

    text = message.get(
        "text"
    )


    if not text:

        return {
            "status": "ignored"
        }


    # ----------------------------------------------
    # DATABASE SESSION
    # ----------------------------------------------

    db = SessionLocal()


    try:

        # ------------------------------------------
        # SAVE USER MESSAGE
        # ------------------------------------------

        telegram_message = TelegramMessage(

            telegram_user_id=telegram_user_id,

            username=username,

            message=text
        )

        db.add(
            telegram_message
        )

        db.commit()

        db.refresh(
            telegram_message
        )


        # ------------------------------------------
        # ASK AGENT
        # ------------------------------------------

        response = ask_agent(text)


        # ------------------------------------------
        # SAVE AGENT RESPONSE
        # ------------------------------------------

        telegram_message.response = response

        db.commit()


        # ------------------------------------------
        # SEND TO TELEGRAM
        # ------------------------------------------

        await send_telegram_message(
            chat_id,
            response
        )


        return {
            "status": "success"
        }


    except Exception as e:

        db.rollback()

        print(
            "ERROR:",
            repr(e)
        )

        return {
            "status": "error",
            "message": str(e)
        }


    finally:

        db.close()
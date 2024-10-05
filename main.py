import logging
from telethon import TelegramClient, events
import json 
from datetime import datetime, timedelta 
import os 

# Giving config a variable to be used
config = json.load(open("assets/config.json", encoding="utf-8"))

# Your credentials
api_id = config['API_ID']  # Get it from https://my.telegram.org/
api_hash = config['API_HASH']  # Get it from https://my.telegram.org/

# Channels
source_channel = config['source_channel']  # Channel to copy messages from (username or ID)
destination_channel = config['destination']  # Channel to send messages to (username or ID)

# Logging setup
logging.basicConfig(
    level=logging.WARNING,  # Set level to WARNING to filter out INFO and DEBUG logs
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Create a Telethon client
client = TelegramClient('personal_forward_bot', api_id, api_hash)

def is_within_time_range():
    """
    Check if the current time (in UTC+1) (UK timezone)
    - Monday to Friday: 9AM - 5PM - Schedule
    - Saturday and Sunday: 10AM - 6PM - Schedule
    """
    # Get current time in UTC
    current_time = datetime.utcnow()

    # Adjust to UTC+1 by adding 1 hour
    utc_minus_1_time = current_time + timedelta(hours=1)

    # Get the current day of the week (0 = Monday, 6 = Sunday) - into simple array
    day_of_week = utc_minus_1_time.weekday()

    # Get current hour and minute
    current_hour = utc_minus_1_time.hour

    # Weekday (Monday to Friday)
    if 0 <= day_of_week <= 4:  # Monday to Friday
        if 9 <= current_hour < 17:  # Between 9AM and 5PM
            return True

    # Weekend (Saturday and Sunday)
    elif day_of_week == 5 or day_of_week == 6:  # Saturday or Sunday
        if 10 <= current_hour < 18:  # Between 10AM and 6PM
            return True

    return False

# Function to forward messages from one channel to another
@client.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    try:
        if is_within_time_range(): # If it's between the schedule posted by us!
            # Extract the message text
            message_text = event.message

            if 'NEW POOL' in message_text.message:
                # Forward the message to the destination channel
                await client.send_message(destination_channel, message_text)

                logger.info(f"Message forwarded to {destination_channel}")
            else:
                logger.info("signal was not a new pool")
        else:
            pass

    except Exception as e:
        logger.error(f"Error occurred: {e}")

# Start the client
if __name__ == '__main__':
    os.system("cls & title Telegram Forward Bot")

    logging.getLogger('telethon').setLevel(logging.WARNING)

    client.start()
    logger.info("Program has not initiated!")
    client.run_until_disconnected()

import time
import logging
import json
from crewai import Crew
from crew import OutlookAgentsCrew
from utils.outlook_connector import get_inboxes, get_unread_emails, create_draft_reply
import os
from utils.ollama_installer import start_ollama_model
from config.config import POLLING_INTERVAL, USER_IDENTITY
from utils.folder_utils import ensure_reviewed_folder
from bs4 import BeautifulSoup
import unicodedata

os.environ["LITELLM_SUPPRESS_PROVIDER_LIST"] = "true"

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger().addHandler(console_handler)

def extract_clean_body(email):
    # Step 1: Prefer HTMLBody, fallback to plain Body
    raw_body = getattr(email, "HTMLBody", "") or getattr(email, "Body", "")

    # Step 2: Remove HTML tags
    soup = BeautifulSoup(raw_body, "html.parser")
    clean_text = soup.get_text()

    # Step 3: Remove all invisible/formatting characters
    cleaned = ''.join(
        ch for ch in clean_text
        if not unicodedata.category(ch).startswith(('C', 'Zl', 'Zp'))  # C = control, Zl/Zp = line/paragraph separator
    )

    return cleaned.strip()

def process_email(email: object, crew: Crew) -> None:
    """
    results(CrewOutput) attr: 
        raw: A string containing the raw output of the crew (default format)
        pydantic: An optional Pydantic model object for structured output
        json_dict: An optional dictionary representing JSON output
        tasks_output: A list of TaskOutput objects for individual task results
        token_usage: A dictionary summarizing token usage during execution
    """
    try:
        logging.info(f"Processing email: {email.Subject}")

        email_input = {
            "subject": email.Subject,
            "sender": email.SenderEmailAddress,
            "body": extract_clean_body(email)
        }

        print("INPUT", email_input)

        results = crew.kickoff(inputs={"email": email_input, "identity": USER_IDENTITY})

        output_dict = {}
        for task_output in results.tasks_output:
            agent_name = task_output.name
            output_dict[agent_name] = task_output.raw

        # Convert to JSON
        json_string = json.dumps(output_dict, indent=4)
        json_output = json.loads(json_string)

        # Draft Response
        if json_output["generate_response"]:
            draft = create_draft_reply(email, json_output["generate_response"])
        logging.info(f"Draft created: {draft.Subject}")

        folder = ensure_reviewed_folder(email)
        email.Move(folder)
        
        logging.info("Moved email to Reviewed folder")
    except Exception as e:
        logging.exception(f"Error processing email {email.Subject}: {str(e)}")


def log_outlook_connection() -> None:
    try:
        inboxes = get_inboxes()
        inbox_names = [inbox.Name for inbox in inboxes] if inboxes else []
        logging.info(f"Connected to inboxes: {', '.join(inbox_names)}")
        logging.info(f"Found {len(get_unread_emails())} unread emails")
    except Exception as e:
        logging.exception(f"Outlook connection error: {str(e)}")


def main() -> None:
    logging.info("🔄 Initializing Outlook AI Agent System...")
    start_ollama_model()  # 🧠 Auto-start the Ollama model

    crew = OutlookAgentsCrew().crew()
    log_outlook_connection()

    while True:
        try:
            emails = get_unread_emails()
            if emails:
                for email in emails:
                    process_email(email, crew)
                    break # Remove after testing
            else:
                logging.info("📭 No new emails found.")
        except Exception as e:
            logging.exception("Main loop error occurred")

        time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    main()

import win32com.client
import pythoncom

def get_outlook_namespace():
    pythoncom.CoInitialize()
    outlook = win32com.client.Dispatch("Outlook.Application")
    return outlook.GetNamespace("MAPI")

# def get_outlook_namespace():
#     try:
#         pythoncom.CoInitialize()
#         outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
#         # Handle Outlook security prompt
#         # outlook.Session.Logon()
#         return outlook
#     except Exception as e:
#         raise e

def get_inboxes():
    """
    Returns a list of Inbox folders for each account in Outlook.
    """
    namespace = get_outlook_namespace()
    inboxes = []
    # Iterate over all accounts
    for account in namespace.Accounts:
        try:
            # Each account's root folder is identified by its display name.
            root_folder = namespace.Folders(account.DisplayName)
            # Get the Inbox folder under the root folder.
            inbox = root_folder.Folders("Inbox")
            inboxes.append(inbox)
        except Exception as e:
            print(f"Could not retrieve Inbox for account '{account.DisplayName}': {e}")
    return inboxes

def get_unread_emails():
    """
    Retrieves unread emails from all Inboxes, excluding those in 'Reviewed' folders.
    """
    unread = []
    inboxes = get_inboxes()
    for inbox in inboxes:
        try:
            messages = inbox.Items
            for msg in messages:
                try:
                    if msg.Unread and msg.Parent.Name != "Reviewed":
                        unread.append(msg)
                except Exception:
                    continue
        except Exception:
            continue
    return unread

def create_draft_reply(original_email, response_body):
    outlook = win32com.client.Dispatch("Outlook.Application")
    reply = original_email.ReplyAll()
    reply.Body = response_body
    reply.Save()  # Saves as draft instead of Send()
    return reply

def get_sent_emails(limit=50):
    namespace = get_outlook_namespace()
    sent_folder = namespace.GetDefaultFolder(5)  # 5 = Sent Items
    messages = sent_folder.Items
    messages.Sort("[SentOn]", True)

    sent_bodies = []
    count = 0
    for msg in messages:
        try:
            if msg.Class == 43 and msg.Body:  # MailItem
                sent_bodies.append(msg.Body)
                count += 1
                if count >= limit:
                    break
        except Exception:
            continue
    return sent_bodies

if __name__ == "__main__":
    # Quick test to verify connection and retrieve unread email count.
    inboxes = get_inboxes()
    print(f"Found {len(inboxes)} inboxes.")
    unread_emails = get_unread_emails()
    print(f"Found {len(unread_emails)} unread email(s).")

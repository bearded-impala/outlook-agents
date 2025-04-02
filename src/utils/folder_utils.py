import win32com.client as win32

def ensure_reviewed_folder(email):
    """
    Moves the given email to the 'Reviewed' folder at the root of the mailbox.
    Returns the folder to which the email should be moved.
    """
    # Get the root folder of the email's store
    store = email.Parent.Store
    root_folder = store.GetRootFolder()

    # Find or create 'Reviewed' folder under the root
    reviewed_folder = None
    for folder in root_folder.Folders:
        if folder.Name == "Reviewed":
            reviewed_folder = folder
            break

    if not reviewed_folder:
        reviewed_folder = root_folder.Folders.Add("Reviewed")

    return reviewed_folder
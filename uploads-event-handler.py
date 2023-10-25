import os
import win32file
import win32con

UPLOADS_FOLDER = "uploads path"  # Uploads folder path
SUPPLY_FOLDER = os.path.join(UPLOADS_FOLDER, "SUPPLY")
DEMAND_FOLDER = os.path.join(UPLOADS_FOLDER, "DEMAND")

def monitor_uploads_folder():
    """
    Sets up an event listener to monitor the uploads folder.
    When a new file is detected in this folder, it triggers further processing.
    """
    path_to_watch = os.path.abspath(UPLOADS_FOLDER)
    hDir = win32file.CreateFile(
        path_to_watch,
        1,  # FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        None,
    )
    while True:
        results = win32file.ReadDirectoryChangesW(
            hDir,
            1024,
            False,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME,
            None,
            None,
        )
        for action, filename in results:
            full_filename = os.path.join(path_to_watch, filename)
            if action == 1:  # File created
                handle_new_file(full_filename)


def handle_new_file(file_path):
    """
    Handles a new file by processing it and categorizing it.
    
    Args:
        file_path (str): The path to the newly created file.
    """
    sub_request_id = get_sub_request_id(os.path.basename(file_path))
    if sub_request_id is not None:
        categorize_and_move_file(file_path)



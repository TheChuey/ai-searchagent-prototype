import datetime
import os

# FUTURE AI: Add 'import sqlite3' here for database support.

def init_db():
    """
    HOOK: DATABASE INITIALIZATION
    An AI can replace this with code to create a 'research.db' file
    and a 'messages' table with columns (id, role, content, timestamp).
    """
    pass

def export_to_file(data, folder="exports", file_type="txt"):
    """
    HOOK: UNIVERSAL FILE EXPORTER
    
    FUTURE AI: 
    1. Check if the 'exports' folder exists using os.makedirs().
    2. Based on 'file_type', implement different saving logics:
       - If 'txt': Standard f.write().
       - If 'json': Use json.dump().
       - If 'md': Save as a Markdown file for better formatting.
    3. Return the string path of the newly created file.
    """
    # For now, we just return a placeholder message
    return f"Placeholder: Future AI will save this as {file_type} in {folder}/"

# BEGINNER TIP: Stubs like this help you design your UI 
# before you've even written the complex backend code.

def save_chat(messages):
    """Saves to TXT (Current) and provides a hook for SQL (Future)."""
    filename = "chat_history.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- TXT APPEND LOGIC ---
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n--- SESSION: {timestamp} ---\n")
        for msg in messages:
            f.write(f"{msg['role'].upper()}: {msg['content']}\n\n")

    # --- HOOK: SQL INSERT ---
    # FUTURE AI: Iterate through 'messages' and use 'INSERT INTO messages...' 
    # to store every interaction permanently in a relational format.
    
    return filename

def read_chat_history():
    """Reads from TXT (Current) and provides a hook for SQL (Future)."""
    # --- HOOK: SQL SELECT ---
    # FUTURE AI: Instead of reading a messy text file, use:
    # 'SELECT content FROM messages WHERE role="assistant" ORDER BY timestamp DESC LIMIT 10'
    
    filename = "chat_history.txt"
    if not os.path.exists(filename):
        return "ERROR: No history found."
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()[-5000:]
import logging
import os
import subprocess
import urllib.request
import tempfile
import shutil
import time
from config.config import MODEL_NAME

def is_ollama_installed() -> bool:
    """Checks if ollama is available either in PATH or default Windows install path"""
    if shutil.which("ollama"):
        return True

    # 🧠 Check known default path
    ollama_default_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
    if os.path.exists(ollama_default_path):
        # 👇 Add it to PATH at runtime so subprocess can use it
        os.environ["PATH"] += os.pathsep + os.path.dirname(ollama_default_path)
        return True

    return False

def add_ollama_to_path_if_installed():
    """If installed but not in PATH, add manually (optional)"""
    ollama_exe = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
    if os.path.exists(ollama_exe):
        os.environ["PATH"] += os.pathsep + os.path.dirname(ollama_exe)

def install_ollama_windows():
    """Download and install Ollama silently on Windows"""
    ollama_url = "https://ollama.com/download/OllamaSetup.exe"
    install_path = os.path.join(tempfile.gettempdir(), "OllamaSetup.exe")

    logging.info("🔽 Downloading Ollama installer...")
    urllib.request.urlretrieve(ollama_url, install_path)
    logging.info(f"✅ Ollama downloaded to: {install_path}")

    logging.info("💿 Running Ollama installer silently...")
    subprocess.run(
        [install_path, "/SILENT", "/VERYSILENT"],
        check=True
    )
    logging.info("✅ Ollama installed successfully.")
    add_ollama_to_path_if_installed()

def is_model_pulled(model_name: str = MODEL_NAME) -> bool:
    """Check if model is already pulled in Ollama"""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        return model_name.lower() in result.stdout.lower()
    except Exception as e:
        logging.warning(f"Could not check Ollama model list: {e}")
        return False


def start_ollama_model():
    from utils.ollama_installer import is_ollama_installed, install_ollama_windows

    if not is_ollama_installed():
        logging.warning("Ollama not found in PATH. Attempting installation...")
        try:
            install_ollama_windows()
        except Exception as e:
            logging.exception("Failed to install Ollama.")
            raise RuntimeError("Could not install Ollama automatically.") from e

    try:
        if not is_model_pulled(MODEL_NAME):
            logging.info(f"📦 Pulling {MODEL_NAME} model (not yet cached)...")
            subprocess.run(["ollama", "pull", MODEL_NAME], check=True)
            logging.info("✅ Model pulled successfully.")
        else:
            logging.info("✅ Model already pulled. Skipping.")
    except Exception as e:
        logging.exception("Failed to pull model.")
        raise RuntimeError("Model pull failed. Make sure you're connected to the internet.") from e

    try:
        logging.info(f"🚀 Starting {MODEL_NAME} model...")
        subprocess.Popen(
            ["ollama", "run", MODEL_NAME],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        time.sleep(5)
        logging.info(f"✅ {MODEL_NAME} launched successfully.")
    except Exception as e:
        logging.exception(f"Failed to start {MODEL_NAME}.")
        raise

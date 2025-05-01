import logging
from pathlib import Path

def setup_logger():
    # Create .wakeword directory in user's home if it doesn't exist
    log_dir = Path.home() / ".wakeword"
    log_dir.mkdir(exist_ok=True)
    
    # Set up logging configuration
    log_file = log_dir / "wakeword.log"
    
    # Create logger
    logger = logging.getLogger("wakeword")
    logger.setLevel(logging.INFO)
    
    # Create formatters
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create a global logger instance
logger = setup_logger() 
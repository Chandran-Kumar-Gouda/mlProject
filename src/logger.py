import logging                     
import os                          
from datetime import datetime     

# Generate a log filename with the current timestamp, e.g., '05_07_2025_18_30_45.log'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create a full path including the current working directory, 'logs' folder, and the log filename
#  Warning: This path includes the filename, so it's not just a folder
log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Create the directory tree at 'log_path'
#  But this line is trying to create a directory with the log file name (like 'logs/05_07_2025_18_30_45.log/'),
#  which is unintended — files shouldn't be used in os.makedirs().
# Still, exist_ok=True means it won't raise an error if the folder exists already
os.makedirs(log_path, exist_ok=True)

# Create another path by joining the (already full) log_path and the log filename again
# This results in something like: logs/05_07_2025_18_30_45.log/05_07_2025_18_30_45.log
#  which is not what you want — you're nesting a file inside a file-named folder
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# Configure the logger with:
# - LOG_FILE_PATH: Where to save the logs
# - format: How the log entries will be formatted
# - level: What level of logs will be captured (INFO and above)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


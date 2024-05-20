import os
import argparse
import logging
import json
import platform
from typing import Dict, Any
# Ensure the parent directory is in the sys.path
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)
# Import the module from the parent directory
from utils.load import load_json_config

def detect_os(m4b_config_path_or_dict: Any) -> Dict[str, str]:
    """
    Detect the operating system and return its type.

    Arguments:
    m4b_config_path_or_dict -- the path to the m4b config file or the config dictionary
    """
    try:
        m4b_config = load_json_config(m4b_config_path_or_dict)

        logging.debug("Detecting OS type")
        os_map = m4b_config.get("system").get("os_map")
        os_type = platform.system().lower()
        os_type = os_map.get(os_type, "unknown")
        logging.info(f"OS type detected: {os_type}")
        return {"os_type": os_type}
    except Exception as e:
        logging.error(f"An error occurred while detecting OS: {str(e)}")
        raise

def detect_architecture(m4b_config_path_or_dict: Any) -> Dict[str, str]:
    """
    Detect the system architecture and return its type.

    Arguments:
    m4b_config_path_or_dict -- the path to the m4b config file or the config dictionary
    """
    try:
        m4b_config = load_json_config(m4b_config_path_or_dict)

        logging.debug("Detecting system architecture")
        arch_map = m4b_config.get("system").get("arch_map")
        arch = platform.machine().lower()
        dkarch = arch_map.get(arch, "unknown")
        logging.info(f"System architecture detected: {arch}, Docker architecture has been set to {dkarch}")
        return {"arch": arch, "dkarch": dkarch}
    except Exception as e:
        logging.error(f"An error occurred while detecting architecture: {str(e)}")
        raise

def main(m4b_config_path_or_dict: Any) -> None:
    """
    Main function to run the detect module standalone.

    Arguments:
    m4b_config_path_or_dict -- the path to the m4b config file or the config dictionary
    """
    try:
        # Test the function
        msg = f"Testing detect module function"
        print(msg)
        logging.info(msg)

        print(detect_os(m4b_config_path_or_dict))
        print(detect_architecture(m4b_config_path_or_dict))
        
        msg = f"Detect module test complete"
        print(msg)
        logging.info(msg)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    # Get the script absolute path and name
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.basename(__file__)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=f"Run the {script_name} module standalone.")
    parser.add_argument('--m4b-config-path-or-dict', type=str, required=True, help='The m4b config file path or JSON string')
    parser.add_argument('--log-dir', default=os.path.join(script_dir, 'logs'), help='Set the logging directory')
    parser.add_argument('--log-file', default=f"{script_name}.log", help='Set the logging file name')
    args = parser.parse_args()

    # Start logging
    os.makedirs(args.log_dir, exist_ok=True)
    logging.basicConfig(filename=os.path.join(args.log_dir, args.log_file),
                        format='%(asctime)s - [%(levelname)s] - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    # Call the main function
    main(args.m4b_config_path_or_dict)

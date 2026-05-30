"""Utility functions shared across the masm2c project."""

import logging

def read_whole_file(file_name: str) -> str:
    """Read the entire file and return it as a string.
    
    Args:
        file_name: The name of the file to read
        
    Returns:
        The content of the file as a string
    """
    logging.info("Reading file %s...", file_name)
    try:
        with open(file_name, encoding="cp437") as file:
            return file.read()
    except Exception as e:
        logging.error("Error reading file %s: %s", file_name, e)
        raise
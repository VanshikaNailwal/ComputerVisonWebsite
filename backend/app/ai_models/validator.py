"""
============================================================
AI Model Validator
============================================================

Purpose
-------
Contains reusable validation utilities for AI model uploads.

Responsibilities
----------------
• Validate uploaded file extension
• Sanitize uploaded filenames
• Verify YOLO model integrity

Architecture
------------

Upload Request
      │
      ▼
Validator
      │
      ▼
Service
      │
      ▼
Database

NOTE
----
This module contains NO database operations and NO API routes.
Its only responsibility is validating uploaded models.

============================================================
"""

from pathlib import Path

from fastapi import HTTPException
from ultralytics import YOLO


# ============================================================
# Allowed Model Extensions
# ============================================================

ALLOWED_MODEL_EXTENSION = ".pt"


# ============================================================
# Sanitize Filename
# ============================================================
#
# Removes any directory information from the uploaded
# filename.
#
# Example
#
# Input:
# ../../truck.pt
#
# Output:
# truck.pt
#
# ============================================================

def sanitize_filename(filename: str) -> str:
    """
    Return a safe filename.

    Parameters
    ----------
    filename : str
        Uploaded filename.

    Returns
    -------
    str
        Sanitized filename.
    """

    return Path(filename).name


# ============================================================
# Validate Model Extension
# ============================================================
#
# Ensures only YOLO .pt models are accepted.
#
# ============================================================

def validate_model_extension(filename: str) -> None:
    """
    Validate uploaded model file extension.

    Raises
    ------
    HTTPException
        If the uploaded file is not a .pt model.
    """

    if Path(filename).suffix.lower() != ALLOWED_MODEL_EXTENSION:
        raise HTTPException(
            status_code=400,
            detail="Only .pt model files are allowed."
        )


# ============================================================
# Validate YOLO Model
# ============================================================
#
# Attempts to load the uploaded model using
# Ultralytics YOLO.
#
# If loading fails, the model is considered invalid.
#
# ============================================================

def validate_yolo_model(model_path: Path) -> None:
    """
    Validate that the uploaded file is a valid
    Ultralytics YOLO model.

    Parameters
    ----------
    model_path : Path
        Path to the uploaded model.

    Raises
    ------
    Exception
        Raised by Ultralytics if the model
        cannot be loaded.
    """

    YOLO(str(model_path))
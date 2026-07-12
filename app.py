# attendance_dashboard/app.py

"""
Application Entry Point

Purpose
-------
Official Streamlit launcher for the OYBS Attendance Dashboard.

Responsibilities
----------------
- Start the Presentation layer.
- Provide a stable application entry point.

Architecture
------------
Root launcher -> Presentation -> Application -> Domain
"""

from src.presentation.streamlit_app import main

if __name__ == "__main__":
    main()

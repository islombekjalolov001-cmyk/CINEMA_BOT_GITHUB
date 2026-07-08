"""Export users table to an .xlsx file using pandas + openpyxl."""
from __future__ import annotations

import datetime as dt
import os

import pandas as pd

from db import get_db


async def export_users_to_excel(output_dir: str = "data") -> str:
    """Write all users to `data/users.xlsx` and return the file path."""
    db = get_db()
    rows = await db.users_dataframe_rows()

    records = [
        {
            "user_id": r["user_id"],
            "username": r["username"],
            "full_name": r["full_name"],
            "language": r["language"],
            "is_blocked": bool(r["is_blocked"]),
            "created_at": dt.datetime.fromtimestamp(r["created_at"]).strftime("%Y-%m-%d %H:%M"),
        }
        for r in rows
    ]

    df = pd.DataFrame(records, columns=[
        "user_id", "username", "full_name", "language", "is_blocked", "created_at"
    ])

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "users.xlsx")
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="users")

        worksheet = writer.sheets["users"]
        for column_cells in worksheet.columns:
            max_len = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = max_len + 2

    return path

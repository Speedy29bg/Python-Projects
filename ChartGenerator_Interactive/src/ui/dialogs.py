import tkinter as tk
from tkinter import ttk
import pandas as pd

def show_data_preview_dialog(parent, data: pd.DataFrame, max_rows: int = 20):
    """Show a popup dialog with a preview of the DataFrame (first N rows)"""
    if data is None or data.empty:
        tk.messagebox.showinfo("Preview Data", "No data to preview.")
        return

    preview_win = tk.Toplevel(parent)
    preview_win.title("Data Preview")
    preview_win.geometry("800x400")

    frame = ttk.Frame(preview_win)
    frame.pack(fill='both', expand=True)

    cols = list(data.columns)
    tree = ttk.Treeview(frame, columns=cols, show='headings', height=min(max_rows, len(data)))
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    for _, row in data.head(max_rows).iterrows():
        tree.insert('', 'end', values=[str(row[col]) for col in cols])

    tree.pack(fill='both', expand=True)

    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    ttk.Label(preview_win, text=f"Showing first {min(max_rows, len(data))} of {len(data)} rows.").pack(pady=5)
    ttk.Button(preview_win, text="Close", command=preview_win.destroy).pack(pady=5)

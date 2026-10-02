"""
Personal Expense Tracker
A simple desktop expense manager built with Tkinter.

The application keeps all expense records in memory during the session and
provides basic add, delete, clear, total, keyboard-shortcut, validation,
tooltip, and status-feedback interactions.
"""

import tkinter as tk
from tkinter import ttk


# ---------------------------------------------------------------------------
# Application constants
# ---------------------------------------------------------------------------

APP_TITLE = "Personal Expense Tracker"
WINDOW_SIZE = "760x700"
CURRENCY = "₱"

COLORS = {
    "background": "#F5F7FB",
    "surface": "#FFFFFF",
    "surface_alt": "#EEF2F7",
    "header": "#172033",
    "header_text": "#FFFFFF",
    "text": "#1F2937",
    "muted_text": "#64748B",
    "border": "#D8DEE8",
    "accent": "#2563EB",
    "accent_hover": "#1D4ED8",
    "accent_pressed": "#1E40AF",
    "success": "#15803D",
    "success_bg": "#ECFDF3",
    "error": "#B91C1C",
    "error_bg": "#FEF2F2",
    "tooltip": "#FFFBEA",
}

FONT = "Segoe UI"
CATEGORIES = [
    "Food",
    "Transport",
    "Utilities",
    "Entertainment",
    "Health",
    "Shopping",
    "Others",
]


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class PersonalExpenseTracker:
    """Main application class for the Personal Expense Tracker GUI."""

    def __init__(self, root):
        """Initialize the main window, data storage, and build the interface."""
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["background"])

        self.expenses = []
        self.total_var = tk.StringVar(value=f"{CURRENCY} 0.00")
        self.status_var = tk.StringVar(value="Ready.")
        self.count_var = tk.StringVar(value="0 records")

        self.setup_styles()
        self.create_widgets()
        self.bind_shortcuts()

    # ------------------------------------------------------------------
    # Styling
    # ------------------------------------------------------------------

    def setup_styles(self):
        """Configure ttk styles for a consistent modern visual theme."""
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "App.TLabel",
            font=(FONT, 10),
            background=COLORS["surface"],
            foreground=COLORS["text"],
        )
        style.configure(
            "Muted.TLabel",
            font=(FONT, 9),
            background=COLORS["surface"],
            foreground=COLORS["muted_text"],
        )
        style.configure(
            "Title.TLabel",
            font=(FONT, 21, "bold"),
            background=COLORS["header"],
            foreground=COLORS["header_text"],
        )
        style.configure(
            "Subtitle.TLabel",
            font=(FONT, 10),
            background=COLORS["header"],
            foreground="#CBD5E1",
        )
        style.configure(
            "Section.TLabel",
            font=(FONT, 11, "bold"),
            background=COLORS["surface"],
            foreground=COLORS["text"],
        )
        style.configure(
            "TotalCaption.TLabel",
            font=(FONT, 9, "bold"),
            background=COLORS["header"],
            foreground="#CBD5E1",
        )
        style.configure(
            "Total.TLabel",
            font=(FONT, 22, "bold"),
            background=COLORS["header"],
            foreground=COLORS["header_text"],
        )
        style.configure(
            "Status.TLabel",
            font=(FONT, 9),
            background=COLORS["surface_alt"],
            foreground=COLORS["muted_text"],
        )

        style.configure(
            "TEntry",
            font=(FONT, 10),
            padding=(9, 8),
            fieldbackground=COLORS["surface"],
            foreground=COLORS["text"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
        )
        style.configure(
            "TCombobox",
            font=(FONT, 10),
            padding=(8, 7),
            fieldbackground=COLORS["surface"],
            foreground=COLORS["text"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
        )

        style.configure(
            "TButton",
            font=(FONT, 10, "bold"),
            padding=(13, 8),
            background=COLORS["surface"],
            foreground=COLORS["text"],
            borderwidth=1,
        )
        style.map(
            "TButton",
            background=[
                ("pressed", COLORS["surface_alt"]),
                ("active", COLORS["surface_alt"]),
            ],
        )

        style.configure(
            "Accent.TButton",
            font=(FONT, 10, "bold"),
            padding=(15, 9),
            background=COLORS["accent"],
            foreground="#FFFFFF",
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[
                ("disabled", "#A7B3C6"),
                ("pressed", COLORS["accent_pressed"]),
                ("active", COLORS["accent_hover"]),
            ],
            foreground=[("disabled", "#E8EDF5")],
        )

        style.configure(
            "Danger.TButton",
            font=(FONT, 10, "bold"),
            padding=(13, 8),
            background="#FFFFFF",
            foreground=COLORS["error"],
        )
        style.map(
            "Danger.TButton",
            background=[("active", COLORS["error_bg"])],
        )

        style.configure(
            "Treeview",
            font=(FONT, 10),
            rowheight=34,
            background=COLORS["surface"],
            fieldbackground=COLORS["surface"],
            foreground=COLORS["text"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
        )
        style.configure(
            "Treeview.Heading",
            font=(FONT, 9, "bold"),
            padding=(7, 8),
            background=COLORS["surface_alt"],
            foreground=COLORS["text"],
            bordercolor=COLORS["border"],
        )
        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", COLORS["text"])],
        )

        style.configure(
            "Vertical.TScrollbar",
            background=COLORS["surface_alt"],
            troughcolor=COLORS["surface_alt"],
            arrowcolor=COLORS["muted_text"],
            bordercolor=COLORS["surface_alt"],
        )

    # ------------------------------------------------------------------
    # GUI construction
    # ------------------------------------------------------------------

    def create_widgets(self):
        """Build all GUI widgets: input fields, buttons, table, total display, and status bar."""
        main_frame = tk.Frame(
            self.root,
            bg=COLORS["background"],
            padx=22,
            pady=18,
        )
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(
            main_frame,
            bg=COLORS["header"],
            padx=22,
            pady=18,
        )
        header.pack(fill=tk.X, pady=(0, 14))

        title_area = tk.Frame(header, bg=COLORS["header"])
        title_area.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            title_area,
            text=APP_TITLE,
            style="Title.TLabel",
        ).pack(anchor=tk.W)

        ttk.Label(
            title_area,
            text="Track your spending quickly and keep a clear view of your total.",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(3, 0))

        total_area = tk.Frame(header, bg=COLORS["header"])
        total_area.pack(side=tk.RIGHT, padx=(18, 0))

        ttk.Label(
            total_area,
            text="TOTAL EXPENSES",
            style="TotalCaption.TLabel",
        ).pack(anchor=tk.E)

        ttk.Label(
            total_area,
            textvariable=self.total_var,
            style="Total.TLabel",
        ).pack(anchor=tk.E, pady=(1, 0))

        # Expense input card
        input_card = tk.Frame(
            main_frame,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=16,
            pady=15,
        )
        input_card.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(
            input_card,
            text="Add Expense",
            style="Section.TLabel",
        ).grid(row=0, column=0, columnspan=6, sticky=tk.W)

        ttk.Label(
            input_card,
            text="Description",
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky=tk.W, pady=(13, 4))

        ttk.Label(
            input_card,
            text="Amount",
            style="Muted.TLabel",
        ).grid(row=1, column=2, sticky=tk.W, pady=(13, 4))

        ttk.Label(
            input_card,
            text="Category",
            style="Muted.TLabel",
        ).grid(row=1, column=4, sticky=tk.W, pady=(13, 4))

        self.desc_entry = ttk.Entry(input_card)
        self.desc_entry.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky=tk.EW,
            padx=(0, 14),
        )
        self.desc_entry.tooltip = "Enter a short description for the expense"
        self.add_tooltip(self.desc_entry, self.desc_entry.tooltip)

        self.amount_entry = ttk.Entry(input_card, width=17)
        self.amount_entry.grid(
            row=2,
            column=2,
            sticky=tk.EW,
            padx=(0, 14),
        )
        self.add_tooltip(
            self.amount_entry,
            "Enter a positive number (e.g. 150.00)",
        )

        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            input_card,
            textvariable=self.category_var,
            values=CATEGORIES,
            state="readonly",
            width=19,
        )
        self.category_combo.grid(
            row=2,
            column=4,
            sticky=tk.EW,
            padx=(0, 14),
        )
        self.category_combo.set("")
        self.add_tooltip(
            self.category_combo,
            "Select an expense category",
        )

        self.add_btn = ttk.Button(
            input_card,
            text="Add Expense",
            style="Accent.TButton",
            command=self.add_expense,
            state=tk.DISABLED,
        )
        self.add_btn.grid(
            row=2,
            column=5,
            sticky=tk.E,
        )
        self.add_tooltip(
            self.add_btn,
            "Add expense to the list (Enter)",
        )

        ttk.Button(
            input_card,
            text="Clear Form",
            command=self.clear_form,
        ).grid(
            row=3,
            column=0,
            sticky=tk.W,
            pady=(12, 0),
        )

        for column in (1, 3):
            input_card.grid_columnconfigure(column, weight=1)

        # Bindings remain the same as the original program.
        self.desc_entry.bind("<KeyRelease>", lambda e: self.check_fields())
        self.amount_entry.bind("<KeyRelease>", lambda e: self.check_fields())
        self.category_combo.bind(
            "<<ComboboxSelected>>",
            lambda e: self.check_fields(),
        )

        # Records table card
        table_card = tk.Frame(
            main_frame,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=12,
            pady=12,
        )
        table_card.pack(fill=tk.X, pady=(0, 12))

        table_header = tk.Frame(table_card, bg=COLORS["surface"])
        table_header.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(
            table_header,
            text="Expense Records",
            style="Section.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Label(
            table_header,
            textvariable=self.count_var,
            style="Muted.TLabel",
        ).pack(side=tk.RIGHT)

        table_frame = tk.Frame(table_card, bg=COLORS["surface"])
        table_frame.pack(fill=tk.X)

        columns = ("num", "desc", "category", "amount")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=5,
        )

        self.tree.heading("num", text="#")
        self.tree.heading("desc", text="Description")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")

        self.tree.column("num", width=48, anchor=tk.CENTER, stretch=False)
        self.tree.column("desc", width=280, anchor=tk.W)
        self.tree.column("category", width=145, anchor=tk.CENTER)
        self.tree.column("amount", width=130, anchor=tk.E)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview,
            style="Vertical.TScrollbar",
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottom actions and status
        footer = tk.Frame(
            main_frame,
            bg=COLORS["background"],
        )
        footer.pack(fill=tk.X)

        action_frame = tk.Frame(footer, bg=COLORS["background"])
        action_frame.pack(side=tk.LEFT)

        self.del_btn = ttk.Button(
            action_frame,
            text="Delete Selected",
            command=self.delete_expense,
        )
        self.del_btn.pack(side=tk.LEFT)
        self.add_tooltip(
            self.del_btn,
            "Delete the selected expense",
        )

        self.clear_btn = ttk.Button(
            action_frame,
            text="Clear All Records",
            style="Danger.TButton",
            command=self.clear_all,
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(8, 0))
        self.add_tooltip(
            self.clear_btn,
            "Remove all expenses and reset",
        )

        status_bar = tk.Frame(
            footer,
            bg=COLORS["surface_alt"],
            padx=10,
            pady=7,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        status_bar.pack(side=tk.RIGHT)

        self.status_label = ttk.Label(
            status_bar,
            textvariable=self.status_var,
            style="Status.TLabel",
        )
        self.status_label.pack()

    # ------------------------------------------------------------------
    # Keyboard shortcuts
    # ------------------------------------------------------------------

    def bind_shortcuts(self):
        """Bind keyboard shortcuts: Enter to add expense, Delete to remove selected."""
        self.root.bind("<Return>", lambda e: self.add_expense())
        self.root.bind("<Delete>", lambda e: self.delete_expense())

    # ------------------------------------------------------------------
    # Validation and tooltips
    # ------------------------------------------------------------------

    def check_fields(self):
        """Enable the Add button only when all required fields are filled."""
        desc = self.desc_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_var.get()

        if desc and amount and category:
            self.add_btn.configure(state=tk.NORMAL)
        else:
            self.add_btn.configure(state=tk.DISABLED)

    def add_tooltip(self, widget, text):
        """Attach a hover tooltip to a widget that displays helper text on mouse enter."""
        tip = tk.Toplevel(widget)
        tip.withdraw()
        tip.overrideredirect(True)

        label = tk.Label(
            tip,
            text=text,
            bg=COLORS["tooltip"],
            fg=COLORS["text"],
            relief=tk.SOLID,
            borderwidth=1,
            padx=7,
            pady=4,
            font=(FONT, 9),
        )
        label.pack()

        def show(event):
            x = widget.winfo_rootx() + widget.winfo_width() + 10
            y = widget.winfo_rooty() + 2
            tip.geometry(f"+{x}+{y}")
            tip.deiconify()

        def hide(event):
            tip.withdraw()

        widget.bind("<Enter>", show)
        widget.bind("<Leave>", hide)

    # ------------------------------------------------------------------
    # Expense operations
    # ------------------------------------------------------------------

    def add_expense(self):
        """Validate inputs and add a new expense entry to the list and table."""
        desc = self.desc_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        category = self.category_var.get()

        if not desc:
            self.display_feedback(
                "Please complete all required fields.",
                is_error=True,
            )
            self.desc_entry.focus_set()
            return

        if not category:
            self.display_feedback(
                "Please complete all required fields.",
                is_error=True,
            )
            self.category_combo.focus_set()
            return

        if not amount_str:
            self.display_feedback(
                "Please complete all required fields.",
                is_error=True,
            )
            self.amount_entry.focus_set()
            return

        try:
            amount = float(amount_str)
        except ValueError:
            self.display_feedback(
                "Amount must be a number.",
                is_error=True,
            )
            self.amount_entry.focus_set()
            return

        if amount <= 0:
            self.display_feedback(
                "Please enter a valid positive amount.",
                is_error=True,
            )
            self.amount_entry.focus_set()
            return

        self.expenses.append(
            {
                "desc": desc,
                "category": category,
                "amount": amount,
            }
        )

        num = len(self.expenses)
        self.tree.insert(
            "",
            tk.END,
            values=(num, desc, category, f"{CURRENCY} {amount:,.2f}"),
        )

        self.calculate_total()
        self.refresh_count()
        self.clear_form()
        self.display_feedback(
            "Expense added successfully.",
            is_error=False,
        )

    def delete_expense(self):
        """Delete the currently selected expense from the list and update the table."""
        selected = self.tree.selection()

        if not selected:
            self.display_feedback(
                "Please select an expense to delete.",
                is_error=True,
            )
            return

        item = self.tree.item(selected[0])
        idx = int(item["values"][0]) - 1

        self.expenses.pop(idx)
        self.tree.delete(selected[0])
        self.refresh_list()
        self.calculate_total()
        self.refresh_count()
        self.display_feedback(
            "Expense deleted.",
            is_error=False,
        )

    def clear_all(self):
        """Clear all expense records and reset the interface to its initial state."""
        if not self.expenses:
            self.display_feedback(
                "No records to clear.",
                is_error=True,
            )
            return

        self.expenses.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.total_var.set(f"{CURRENCY} 0.00")
        self.refresh_count()
        self.clear_form()
        self.display_feedback(
            "All expense records have been cleared.",
            is_error=False,
        )

    # ------------------------------------------------------------------
    # Form and calculations
    # ------------------------------------------------------------------

    def clear_form(self):
        """Reset the description, amount, and category input fields to empty."""
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set("")
        self.check_fields()

    def calculate_total(self):
        """Recalculate and update the total expenses display with two decimal places."""
        total = sum(expense["amount"] for expense in self.expenses)
        self.total_var.set(f"{CURRENCY} {total:,.2f}")

    def refresh_list(self):
        """Rebuild the treeview table from the current expenses list with correct numbering."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, expense in enumerate(self.expenses, 1):
            self.tree.insert(
                "",
                tk.END,
                values=(
                    i,
                    expense["desc"],
                    expense["category"],
                    f"{CURRENCY} {expense['amount']:,.2f}",
                ),
            )

    def refresh_count(self):
        """Update the number of currently stored expense records."""
        count = len(self.expenses)
        label = "record" if count == 1 else "records"
        self.count_var.set(f"{count} {label}")

    def display_feedback(self, message, is_error=False):
        """Show a status message to the user (green for success, red for errors)."""
        self.status_var.set(message)

        if is_error:
            self.status_label.configure(foreground=COLORS["error"])
        else:
            self.status_label.configure(foreground=COLORS["success"])

        self.root.after(
            4000,
            lambda: self.status_label.configure(
                foreground=COLORS["muted_text"]
            ),
        )


# ---------------------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------------------

def main():
    """Create the Tkinter root window and start the application."""
    root = tk.Tk()
    PersonalExpenseTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()

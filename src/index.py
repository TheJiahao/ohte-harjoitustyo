from tkinter import Tk

import sv_ttk

from ui.ui import UI


def main() -> None:
    window = Tk()
    window.title("Study-planner")

    ui_view = UI(window)
    ui_view.start()

    sv_ttk.set_theme("light")

    window.mainloop()


if __name__ == "__main__":
    main()

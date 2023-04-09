from tkinter import Tk

from ui.ui import UI


def main() -> None:
    window = Tk()
    window.title("Study-planner")

    ui_view = UI(window)
    ui_view.start()

    window.mainloop()


if __name__ == "__main__":
    main()

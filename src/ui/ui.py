from ui.create_course_view import CreateCourseView


class UI:
    def __init__(self, root) -> None:
        self.__root = root
        self.__current_view = None

    def start(self) -> None:
        self.__show_create_course_view()

    def __hide_current_view(self) -> None:
        if self.__current_view:
            self.__current_view.destroy()

        self.__current_view = None

    def __show_create_course_view(self) -> None:
        self.__hide_current_view()

        self.__current_view = CreateCourseView(self.__root)

        self.__current_view.pack()

import flet

# from utils.base64img import *

VERSION = "4.3"
MODES = ["Wild Encounter", "Stationary", "Fishing"]


class myHome(object):
    def __init__(self, page: flet.Page) -> None:
        self.page = page
        # Column1
        # self.version_block=Block("Version: ", flet.Dropdown(width=100,options=[flet.dropdown.Option(ver) for ver in ['RS', 'E', 'FrLg']],autofocus=True))
        # self.mode_block=Block("Mode: ", flet.Dropdown(width=160,options=[flet.dropdown.Option(mode) for mode in ['Wild Encounter', 'Stationary']]))
        self.version_dropdown = flet.Dropdown(
            label="Version",
            options=[flet.dropdown.Option(ver) for ver in ["RS", "E", "FrLg"]],
            expand=1,
        )
        self.mode_dropdown = flet.Dropdown(
            label="Mode",
            options=[flet.dropdown.Option(mode) for mode in MODES],
            expand=1,
        )
        self.start_button = flet.FilledTonalButton(text="Start!", expand=1)
        self.direction = DirectionButton()
        self.refresh = flet.IconButton(
            icon=flet.icons.REFRESH,
        )
        self.button_row = flet.Row(
            controls=[self.start_button, self.refresh, self.direction], expand=1
        )
        # self.Column1=flet.Column(controls=[self.version_block,self.mode_block,self.button_row],alignment=flet.alignment.center, expand=1)
        self.Column1 = flet.Column(
            controls=[self.version_dropdown, self.mode_dropdown, self.button_row],
            alignment=flet.alignment.center,
            expand=1,
        )

        # Column2
        self.jump_block = Block("Jump? ", flet.Checkbox(tristate=True, disabled=True))
        self.run_block = Block("Run? ", flet.Checkbox(tristate=True, disabled=True))
        self.checkbox_column = flet.Column(controls=[self.jump_block, self.run_block])
        # img_src_base64="iVBORw0KGgoAAAANSUhEUgAAAEQAAABECAMAAAAPzWOAAAAAnFBMVEUAAAD///8AAABBQEHe1py0pYNaSkEAAAi0pIMABAhMSjzm3qSZlHB7Y0qwo39OREFWTkHFlWrVg0FKRjzm2qR3bU4ADBi/lF3VhUF4bld4b1pHNSt+b1eDZUqDcVqOhmJHQzGck3CsnYMIBABKRzRKRzm0pYsIBAg8OjFSODE8OjTViVLVypTe0qRBQDne1qTm1px1clp1cl/2wnNjjoyyAAAAAnRSTlMAAHaTzTgAAAEhSURBVHhe7dbHcoUwDIZR55ds024v6b339v7vFsmQudki2MXfwsszIDGA2xuhf4NkJCMZyYjrAtzfLIgagxHQKAhhOMJP5QjI3WAEzB4jIIcjIBKUQcqCgNsA1YgI/RHwb16PujIg4M833uWbCEJfpDzFOfPHBldKeF0T+iJYLC5emDfX83lrWLaD52OWVvEGgpzAtuJtQl5XkLO7EMtgib74e/9gN5EJLCsmehSkM8LEgKjil8uiSAhCCAZEDUkQqGFFpOnZ0QNUnIUA02AFeZ/60iUEYlkQZeR20lQDnAlhRbhDYEHgOdUOdmZ6YnU1yVDEi2FC6Jbrhor1JXFTkQ1xiBwrovU9UR1hfsfCgSARBn532sOG5D+ljGQkIxn5AeTYGlTNxZ6xAAAAAElFTkSuQmCC"
        # img_src="https://github.com/willkyu/willkyu.github.io/blob/main/images/avatar_.png?raw=true"
        # self.image=flet.Image(src_base64=img_src,width=100,height=100,border_radius=flet.border_radius.all(10),expand=1)
        self.image = flet.Container(
            image_src="https://github.com/willkyu/AutoPoke/blob/main/fig.png?raw=true",
            width=100,
            height=100,
            border_radius=flet.border_radius.all(10),
            expand=1,
        )
        self.row_in_column2 = flet.Row(
            controls=[self.checkbox_column, self.image], expand=1
        )
        self.count_pannel = flet.Column(
            controls=[
                flet.Text(
                    value="Encounters Count: ",
                    theme_style=flet.TextThemeStyle.HEADLINE_SMALL,
                ),
                flet.TextField(
                    value="8192",
                    text_style=flet.TextStyle(size=32),
                    text_align=flet.TextAlign.CENTER,
                ),
            ]
        )
        self.Column2 = flet.Column(
            controls=[self.row_in_column2, self.count_pannel], expand=1
        )

        # Column3
        self.main_pannel = MainPanel()
        self.Column3 = flet.Column(
            controls=[self.main_pannel],
            alignment=flet.alignment.center,
            expand=1,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        )

        self.row = flet.Row(
            controls=[self.Column1, self.Column2, self.Column3], expand=1, spacing=50
        )

        # # 将元素添加进window
        self.page.add(self.row)
        # # 聚焦输入框
        # self.input_field.input_box.focus()
        # self.direction.update_state('no')

    def print_to_pannel(self, info):
        self.main_pannel.append(flet.Text(value=info))

    def onKeyboardEnter(self, e: flet.KeyboardEvent):
        pass

    def updateState(self, state: str):
        pass


class MainPanel(flet.ListView):
    """panel"""

    def __init__(
        self, maxlen=100, expand: int = 1, spacing: int = 10, auto_scroll: bool = True
    ):
        super().__init__(expand=1, spacing=10, auto_scroll=True)
        self.maxlen = maxlen
        self.controls.append(flet.Text(value="=== AutoPoke v{} ===".format(VERSION)))
        self.controls.append(
            (
                flet.Text(
                    value="*Text Speed of Game MUST be Fast AND NO Window Minimizing of Playback."
                )
            )
        )

    def append(self, text: flet.Text):
        self.controls.append(text)
        if len(self.controls) > 50:
            self.controls = self.controls[-50:]
        self.update()


class Block(flet.Row):
    """文本与自定义框"""

    def __init__(self, text: str, another: object, expand=0) -> None:
        super().__init__(expand=expand)
        self.text = flet.Text(value=text, weight=flet.FontWeight.BOLD)
        self.another = another
        # self.input_box = flet.TextField(expand=1, label="Ctrl or Cmpt?")
        # self.send_bottom = flet.IconButton(
        #     icon=flet.icons.ARROW_UPWARD_ROUNDED, icon_color=flet.colors.WHITE10, on_click=home.sendMessage)
        self.controls = [
            self.text,
            self.another,
        ]


class DirectionButton(flet.IconButton):
    """方向按钮"""

    def __init__(self):
        super().__init__(icon=flet.icons.DO_NOT_DISTURB, disabled=True)
        self.value = "lr"
        # print('init')

    def update_state(self, state):
        if state == "lr":
            self.icon = flet.icons.SWAP_HORIZ
            self.value = "lr"
        elif state == "ud":
            self.icon = flet.icons.SWAP_VERT
            self.value = "ud"
        else:
            self.icon = flet.icons.DO_NOT_DISTURB
            self.value = "no"
        self.update()

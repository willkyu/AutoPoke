import flet

# from utils.base64img import *

VERSION = "5.5.1.112824_beta"
MODES = ["Wild Encounter", "Stationary", "Fishing", "Test"]


class myHome(object):
    def __init__(self, page: flet.Page) -> None:
        self.page = page
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
        self.language_row = flet.RadioGroup(
            content=flet.Row(
                [
                    flet.Radio(value="Eng", label="Eng"),
                    flet.Radio(value="Jpn", label="Jpn"),
                ]
            )
        )
        self.Column1 = flet.Column(
            controls=[
                self.version_dropdown,
                self.mode_dropdown,
                self.language_row,
                self.button_row,
            ],
            alignment=flet.alignment.center,
            expand=1,
        )

        # Column2
        self.jump_block = Block("Jump? ", flet.Checkbox(tristate=True, disabled=True))
        self.run_block = Block("Run? ", flet.Checkbox(tristate=True, disabled=True))
        self.sweet_scent_block = Block(
            "Sweet Scent? ", flet.Checkbox(tristate=True, disabled=True)
        )
        self.repel_block = Block(
            "Auto Repel? ", flet.Checkbox(tristate=True, disabled=True)
        )
        self.checkbox_column = flet.Column(
            controls=[
                self.jump_block,
                self.run_block,
                self.sweet_scent_block,
                self.repel_block,
            ],
            # expand=1,
            spacing=1,
        )

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
                    # height=50,
                ),
            ],
            # expand=1,
            spacing=0,
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

        # 将元素添加进window
        self.page.add(self.row)
        # 聚焦输入框
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

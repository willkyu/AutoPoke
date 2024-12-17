import flet as ft


class ControlAndTips(ft.Container):
    def __init__(
        self,
        pannel: ft.Column,
        tips: str = "",
        text_size=16,
        alignment=ft.alignment.center,
        **kwargs
    ):
        super().__init__(alignment=alignment, **kwargs)
        self.pannel = pannel
        self.tips = tips
        self.border_radius = 10
        self.text_size = text_size
        # self.pannel.visible = len(self.tips) == 0
        self.text_view = ft.Container(
            content=ft.Text(
                value=self.tips,
                size=self.text_size,
                expand=True,
            ),
            padding=ft.padding.symmetric(vertical=10),
            bgcolor=ft.colors.GREY_900,
            visible=len(self.tips) > 0,
        )
        self.content = ft.Stack(
            [self.pannel, self.text_view],
            alignment=ft.alignment.center,
        )
        # self.on_hover = lambda e: print(id(e.control))

    def update_tips(self, tips: str):
        self.tips = tips
        # self.pannel.visible = len(self.tips) == 0
        self.text_view.visible = len(self.tips) > 0
        self.text_view.content.value = self.tips
        # print(self.tips)
        # self.content = ft.Stack(
        #     [self.pannel, self.text_view],
        #     alignment=ft.alignment.center,
        # )

        self.update()


class BoolSettingItem(ft.Container):
    def __init__(
        self,
        value: bool,
        title: str,
        on_click_buttom,
        pannel_and_tips: ControlAndTips,
        true_icon: ft.Icon,
        false_icon: ft.Icon = ft.icons.DO_NOT_DISTURB_ROUNDED,
        tips: str = "",
        expand=False,
        **kwargs
    ):
        super().__init__(
            expand=expand,
            height=50,
            # vertical_alignment=ft.CrossAxisAlignment.START,
            **kwargs
        )
        self.pannel_and_tips = pannel_and_tips
        self.tips = tips
        self.content = BoolItemButtom(
            value=value,
            text=title,
            true_icon=true_icon,
            false_icon=false_icon,
            on_click=on_click_buttom,
        )
        self.on_hover = self.on_hover_show_tip

    def on_hover_show_tip(self, e: ft.HoverEvent):
        self.pannel_and_tips.update_tips(self.tips if e.data == "true" else "")
        # print(e.data, self.tips)


class BoolItemButtom(ft.ElevatedButton):
    def __init__(self, value, true_icon: ft.Icon, false_icon: ft.Icon, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.true_icon = true_icon
        self.false_icon = false_icon
        self.icon = self.true_icon if self.value else self.false_icon

    def toggle(self):
        self.value = not self.value
        self.icon = self.true_icon if self.value else self.false_icon
        self.update()


class Block(ft.Column):
    """文本与自定义框"""

    def __init__(self, text: str, another: ft.Control, tips: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.text = ft.Text(value=text, weight=ft.FontWeight.BOLD)
        self.another = another

        self.controls = (
            [
                self.text,
                self.another,
                ft.Text(
                    value=tips,
                    size=13,
                    color=ft.colors.GREY,
                ),
            ]
            if isinstance(self.another, ft.TextField)
            else [
                ft.Row(
                    [
                        self.text,
                        self.another,
                    ]
                ),
                ft.Text(
                    value=tips,
                    size=13,
                    color=ft.colors.GREY,
                ),
            ]
        )

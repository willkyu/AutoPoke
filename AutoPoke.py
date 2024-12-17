import flet
from ui.AutoPokeUI import AutoPokeUI
from core.config import VERSION

# from utils.my_ui import VERSION


def main_page(page: flet.Page) -> None:
    page.title = f"AutoPoke {VERSION} by willkyu"
    page.window.width = 500
    page.window.height = 400
    page.window.resizable = False
    AutoPokeUI(page)


if __name__ == "__main__":
    flet.app(target=main_page)

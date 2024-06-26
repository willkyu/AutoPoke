import flet
from utils.home import Home
from utils.myUI import VERSION


def mainPage(page: flet.Page) -> None:
    page.title = "AutoPoke v{} by willkyu".format(VERSION)
    page.window_width = 720
    page.window_height = 300
    homePage = Home(page)


if __name__ == "__main__":
    flet.app(target=mainPage)

import flet
from utils.home import Home

def mainPage(page: flet.Page)->None:
    page.title="AutoPoke v4.2.1 by willkyu"
    page.window_width = 720
    page.window_height = 300
    homePage = Home(page)

if __name__ == '__main__':
    flet.app(target=mainPage)

import windows_toasts as wt

# import WindowsToaster, Toast, ToastDisplayImage, ToastImage


def send_toast(count: int):
    wintoaster = wt.WindowsToaster("AutoPoke")
    new_toaster = wt.Toast(
        [f"Got Shiny Pokemon in {count} SLs! Congratulations!"],
    )
    new_toaster.AddImage(
        wt.ToastDisplayImage.fromPath(
            "AutoPoke.shinyshoot.bmp", position=wt.ToastImagePosition.AppLogo
        )
    )
    wintoaster.show_toast(new_toaster)

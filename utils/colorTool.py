#对后台窗口截图
import win32gui, win32ui, win32con
from PIL import Image


def getColor(eo,x,y):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    #print('width:{}, height:{}.'.format(width,height))
    #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(eo)
    #创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    #创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    #创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
    ###保存bitmap到文件
    saveBitMap.SaveBitmapFile(saveDC,"tempIMG.bmp")
    
    im=Image.open('tempIMG.bmp')#文件的路径
    # print(im.mode)
    # print(im.getpixel((x,y)))#像素点的rgb

    #内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(eo,hWndDC)
    return im.getpixel((x,y))

def getSize():
    im=Image.open('tempIMG.bmp')
    return[im.width,im.height]



#如果要截图到打印设备：
###最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
#result = windll.user32.PrintWindow(hWnd,saveDC.GetSafeHdc(),0)
#print(result) #PrintWindow成功则输出1
 
#保存图像
##方法一：windows api保存

 

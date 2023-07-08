from email.header import Header
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from PIL import Image

# 邮件服务器地址,以下为网易邮箱
pop3_server = 'pop.163.com'

def sendMail(i=0, toMail='接收邮箱', subject='', picfilename='tempIMG.bmp'):
    mail = MIMEMultipart('related')
    mail_host = "smtp.163.com"
    mail_user = "发送邮箱"
    mail_pass = "授权码"
    receivers = toMail
    
    if subject=='':
      subject=u'Got Shiny Pokemon in {} SLs!'.format(i)

    # 图像压缩处理
    img = Image.open(picfilename)
    img_resize = img.resize((500,350))
    img_resize.save(picfilename)


    img_file = open(picfilename, 'rb')
    img_data = img_file.read()
    img_file.close()
    img = MIMEImage(img_data)
    img.add_header('Content-ID', '<pic>')  # 给一个content Id 供后面html内容引用
    mail.attach(img)
    myMessage = """
    <html>
      <body>
        <p>Got Shiny Pokemon in {} SLs!</p>
        <img src="cid:pic">
      </body>
    </html>
    """.format(i)
    mail.attach(MIMEText(myMessage, 'html', 'utf-8'))
    mail['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(mail_user,  receivers, mail.as_string())
        # print (f"{receivers} 邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
        pass

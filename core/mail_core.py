from email.header import Header
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def send_mail(i, to_mail, mail_host, mail_user, mail_pass, printf):
    mail = MIMEMultipart("related")

    receivers = to_mail

    picfilename = "AutoPoke.shinyshoot.bmp"
    subject = "AutoPoke: Got Shiny Pokemon in {} SLs!".format(i)

    # 图像压缩处理
    # img = Image.open(picfilename)
    # img_resize = img.resize((500,350))
    # img_resize.save(picfilename)

    img_file = open(picfilename, "rb")
    img_data = img_file.read()
    img_file.close()
    img = MIMEImage(img_data)
    img.add_header("Content-ID", "<pic>")  # 给一个content Id 供后面html内容引用
    mail.attach(img)
    myMessage = f"""
    <html>
      <body>
        <p>Got Shiny Pokemon in {i} SLs! Congratulations!</p>
        <img src="cid:pic">
      </body>
    </html>
    """
    mail.attach(MIMEText(myMessage, "html", "utf-8"))
    mail["Subject"] = Header(subject, "utf-8")
    # print(mail_host)
    # print(mail_user)
    # print(mail_pass)
    # print(receivers)

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        # print(123)
        smtpObj.sendmail(mail_user, receivers, mail.as_string())
        printf(f"{receivers} 邮件发送成功")
    except smtplib.SMTPException:
        printf("Error: 无法发送邮件")
        pass

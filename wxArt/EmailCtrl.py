
import wx
import smtplib

class EmailCtrl(wx.TextCtrl):

    server_name = "smtp.gmx.ch"
    port = 587
    user = "kevin.clever@gmx.ch"
    subject = "Neural artistic style."
    body = "Here comes some descriptive text."

    def __init__(self, *args, **kwargs):
        kwargs["style"] = wx.TE_PROCESS_ENTER               # Style allows the text field to intercept pressing <Enter>
        super(EmailCtrl, self).__init__(*args, **kwargs)
        
        # Set the password dynamically when the program starts. (TO DO)
        self.password = ""
        
        self.Bind(wx.EVT_TEXT_ENTER, self.send_mail, self)


    def send_mail(self, event):
        recipient = self.GetValue()

        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self.user, recipient, self.subject, self.body)

        print "Sending ", message

        try:
            server = smtplib.SMTP(server_name, port)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.user, recipient, message)
            server.close()
            wx.MessageBox('successfully sent the mail')

        except:
            wx.MessageBox("failed to send mail")

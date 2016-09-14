
import os
import wx
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text        import MIMEText
from email.mime.multipart   import MIMEMultipart

from .PasswordQuery import PasswordQuery



class EmailCtrl(wx.TextCtrl):

    server_name       = "smtp.gmx.ch"
    port              = 587
    sender            = "kevin.clever@gmx.ch"
    default_recipient = "jschwabedal@gmail.com"
    subject           = "Neural artistic style"
    body              = "Here comes some descriptive text."

    def __init__(self, *args, **kwargs):
        kwargs["style"] = wx.TE_PROCESS_ENTER               # Style allows the text field to intercept pressing <Enter>
        super(EmailCtrl, self).__init__(*args, **kwargs)
        
        # Set the password dynamically when the program starts. (TO DO)
        self.password = ""
        #self.query_password()


    def send_email(self, attachments=[], recipient=None): # attachments is a list of filenames.
        #read out the recipient email address
        if recipient == None:
            recipient = self.GetValue()

        # construct the email
        message = MIMEMultipart()
        message['From']    = self.sender
        message['To']      = recipient
        message['Subject'] = self.subject

        message.attach( MIMEText(self.body) )

        for f in attachments:

            assert os.path.exists(f), "File '%s' nonexistent." % (f)

            with open(f, 'rb') as File:
                attachment = MIMEApplication( File.read(),
                                              Name = os.path.basename(f) )

                attachment['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
                message.attach(attachment)

        # Send the email
        try:
            server = smtplib.SMTP(self.server_name, self.port)
            server.ehlo()
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, recipient, message.as_string())
            server.close()
            wx.MessageBox('Successfully sent the mail.')
            return True

        except:
            wx.MessageBox("Failed to send mail")
            return False


    def query_password(self):
        
        while False:
            dialog = PasswordQuery(None, size=wx.Size(200, 50))
            dialog.ShowModal()

            self.password = dialog.password
            
            if self.send_email(recipient=self.default_recipient):   # Returns true if email successfully sent.
                return

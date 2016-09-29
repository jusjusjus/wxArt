
# -*- coding: utf-8 -*- 

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
    
    _pwd_title        = "Password for %s" % (sender)

    def __init__(self, *args, **kwargs):
        kwargs["style"] = wx.TE_PROCESS_ENTER               # Style allows the text field to intercept pressing <Enter>
        super(EmailCtrl, self).__init__(*args, **kwargs)
        
        # Set the password dynamically when the program starts. (TO DO)
        self.password = ""  # XXX
        self.SetEditable(False)
        self.query_password()


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

        if self.IsEditable():
            return
        
        while True:    # XXX
            query_fields = [('server_name', self.server_name),
                            ('sender',      self.sender),
                            ('port',        self.port),
                            ('password',    '')               ]

            dialog = PasswordQuery(query_fields, None, size=wx.Size(400, 150), title=self._pwd_title)
            dialog.ShowModal()

            if dialog.OK == True:
                for key in dialog.input:
                    if key == 'port':   setattr(self, key, int(dialog.input[key]))      # this has to be an integer.
                    else:               setattr(self, key, dialog.input[key])           # these should be strings.
            
                if self.send_email(recipient=self.default_recipient):   # Returns true if email successfully sent.
                    self.SetEditable(True)
                    return

            else:   # dialog not ok:  Disable the ability to enter stuff into the text field.
                self.SetEditable(False)
                return



    subject           = "Kunst durch künstliche Intelligenz"

    body = """Hallo!

    Wir freuen uns, dass Sie sich am Tag der Deutschen Einheit die Zeit
    genommen haben unseren Stand im Wissenschaftszelt zu besuchen.

    Mehrschichtige neuronale Netze werden zunehmend Teil der Technologie, die
    uns in unserem täglichen Leben umgibt. Die zugrunde liegenden Mechanismen
    versuchen die Funktionsweise von Gehirnen lebender Wesen nachzuahmen und
    erreichen so faszinierende Ergebnisse. Die Vorstellung ein denkendes
    Wesen in unserem Computer zu simulieren ist natürlich sehr ungewohnt.
    Viele Menschen machen sich Sorgen, dass wir diese Technik nicht ausreichend
    beherrschen. Darum haben wir uns am Stand des Max-Planck-Instituts für die
    Physik Komplexer Systeme darum bemüht, diese Technik am Beispiel von
    'Sehen' etwas zu entzaubern.

    Wenn sich ein mehrschichtiges neuronales Netz ein Bild ansieht, dann sieht
    es nicht zuerst auf das große Ganze sondern sucht systematisch nach
    einfachen Details. Auf seiner ersten Prozessierungsebene entdeckt es zum
    Beispiel Kanten von Farbübergängen, die unterschiedlich auf dem Bild
    ausgerichtet sind. Dies passiert für jeden Farbkanal, Rot, Grün und Blau,
    einzeln. So werden aus den drei Farbkanälen, die zusammen das ursprüngliche
    Bild ergeben, Kanäle von Kanten unterschiedlicher Ausrichtung. In den
    folgenden Ebenen werden diese Kanten nun zu Umrissen und Umrisse zu Objekten.
    Die verarbeitete Information wird also immer abstrakter.

    An unserem Stand haben wir diese Technologie nun genutzt, um aus einem Foto
    und einem Gemälde ein neues Kunstwerk zu machen.
    Wie geht das wohl? Wie zuvor beschrieben zerlegen wir mit Hilfe eines
    Neuronalen Netzwerkes ein Bild auf unterschiedlichen
    Abstraktionsebenen in seine Informationsbestandteile. Im Foto wird der Inhalt erkannt,
    zum Beispiel ein Ohr oder eine Nase, im Kunstwerk hingegen, erkennt das
    Netzwerk die Art und Weise wie Inhalte aus verschiedenen Kanten
    und Farbenspielen konstruiert sind. Kombiniert man beides, erhält man ein
    neues Kunstwerk mit dem Inhalt des Fotos und dem Stil des Gemäldes.
    Und wenn bei uns alles geklappt hat, dann können Sie nun Ihr neues Kunstwerk im
    Anhang dieser E-Mail bewundern.

    Viele Grüße aus dem sonnigen Sachsen wünschen Ihnen unser Team.

    Justus Schwabedal
    Benedict Lünsmann
    Mehrdad Baghery
    Andre Scholich
    """


























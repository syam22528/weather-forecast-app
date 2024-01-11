import smtplib
import random


verificationCode = random.randint(100000, 1000000)
new_mail = ""
mail_sent_message = """A mail has been sent to your
 account with a verification code.
 Please enter the verification
 code in the box below:"""


def sendMail():
    Email_Username = "pythonmailbot123@gmail.com"
    Email_Password = "python12345"

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(Email_Username, Email_Password)

        subject = "The Weather Forecast App: Verification Code"
        body = "Here is your verification code:"
        msg = f"Subject: {subject}\n\n{body}\n{verificationCode}"
        smtp.sendmail(Email_Username, new_mail, msg)
        print("Mail has been sent.")
        print("\n\n")

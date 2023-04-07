import smtplib
import random

# function to generate random 6-digit code
def generate_code():
    return random.randint(100000, 999999)

# function to send verification email
def send_verification_email(recipient_email, verification_code):
    sender_email = 'email'  # replace with your own email address
    sender_password = 'pass'  # replace with your own email password

    message = f'Subject: Email Verification Code\n\nYour email verification code is {verification_code}'

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sender_email, sender_password)

        smtp.sendmail(sender_email, recipient_email, message)

# main program
recipient_email = input('Enter your email address: ')

# send verification code
verification_code = generate_code()
send_verification_email(recipient_email, verification_code)
print('Verification code sent to your email address.')

# verify email
verification_attempts = 3
while verification_attempts > 0:
    user_input = input('Enter the verification code you received: ')
    if user_input == str(verification_code):
        print('Email address verified successfully.')
        break
    else:
        verification_attempts -= 1
        if verification_attempts > 0:
            print(f'Incorrect verification code. {verification_attempts} attempts remaining.')
            resend_input = input('Do you want to resend the verification code? (y/n) : ')
            if resend_input.lower() == 'y':
                verification_code = generate_code()
                send_verification_email(recipient_email, verification_code)
                print('Verification code sent to your email address.')
            elif resend_input.lower() == 'n':
                print('Kindly do the verification soon.')
                break
        else:
            print('Verification failed. Please try again later.')
            break

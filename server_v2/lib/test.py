
from sendotp import sendotp

otpobj =  sendotp.sendotp('190375ALnQVrF2Z5a46383e','my message is {{otp}} keep otp with you.')

# 3245 is the otp to send
print(otpobj.send(919981534313,'msgind',3245))

#

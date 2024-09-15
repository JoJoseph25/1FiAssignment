import requests
from models.User import Users
from configs.config import Config
from configs.extensions import DBSession as db
from dependencies.security import get_hashed_password
from starlette.requests import Request as current_app

def check_username_exist(username: str):
    data = (db.query(Users)
            .filter_by(username=username)
            .one_or_none())
    return data

def check_user_exist(email: str, phone_number: str = None):
    data = None
    if email: # verify with email at max
        data = (db.query(Users)
                .filter_by(email=email)
                .one_or_none())
        return data
    if phone_number:
        data = (db.query(Users)
                .filter_by(phone_number=phone_number)
                .one_or_none()) 
    return data

def fetch_all_user(active=None):
    if active is not None:
        data = db.query(Users).filter_by(active=active).all()
    else:
        data = db.query(Users).all()
    return data

def add_user(data):
    user = Users(
            email=data.email,
            phone_number=data.phone_number,
            full_name=data.full_name,
            username=data.username,
            password=data.password,
        )
    db.add(user)
    db.flush()
    return user


class SMS_OTP:
    def __init__(self) -> None:
        self.SMS_Key = Config.SMS_KEY
        self.SMS_Email = Config.SMS_EMAIL
        self.CustomerID = Config.SMS_CUSTOMERID
        self.SMS_BaseURL = 'https://cpaas.messagecentral.com'
    
    def get_auth_token(self, app):
        SMS_AUTH_Headers = {'accept': '*/*'}
        SMS_AuthTokenURL = f'{self.SMS_BaseURL}/auth/v1/authentication/token' 
        SMS_AuthTokenURL+=f"?customerId={self.CustomerID}&key={self.SMS_Key}&scope=NEW&country=91&email={self.SMS_Email}"
        SMSAuthResponse = requests.get(SMS_AuthTokenURL, headers=SMS_AUTH_Headers)
        if SMSAuthResponse.status_code!=200:
            app.logger.error(f'Could not fetch SMS Auth Token: {SMSAuthResponse.json()}')
        SMS_AuthToken = SMSAuthResponse.json()['token']
        return SMS_AuthToken
    
    def send_sms(self, phone_number, app):
        SMS_AuthToken = self.get_auth_token(app)
        SMS_Send_Headers = {'authToken': SMS_AuthToken}
        SMS_SendOTP_URL = f'{self.SMS_BaseURL}/verification/v3/send' 
        SMS_SendOTP_URL+=f"?flowType=SMS&countryCode=91&otpLength=6&mobileNumber={phone_number}"
        SMS_SendOTP_Response = requests.post(SMS_SendOTP_URL, headers=SMS_Send_Headers)
        if SMS_SendOTP_Response.status_code!=200:
            app.logger.error(f'Could not send SMS OTP: {SMS_SendOTP_Response.json()}')

        SMS_OTP = SMS_SendOTP_Response.json()['data']['verificationId']    
        # set OTP in redis
        sms_otp_key = f"OTP:SMS:{phone_number}"
        app.redis.set(sms_otp_key, SMS_OTP, ex=60)
        return SMS_SendOTP_Response
    
    def verify_sms(self, verificartionID, app):
        SMS_AuthToken = self.get_auth_token(app)
        SMS_Verify_Headers = {'authToken': SMS_AuthToken}
        SMS_Verify_URL = f'{self.SMS_BaseURL}/verification/v3/validateOtp' 
        SMS_Verify_URL+=f"?verificationId={verificartionID}&code={otp}"
        SMS_Verify_Response = requests.get(SMS_Verify_URL, headers=SMS_Verify_Headers)
        if SMS_Verify_Response.status_code!=200:
            app.logger.error(f'Could not send SMS OTP: {SMS_Verify_Response.json()}')
        return SMS_Verify_Response

def send_email(name, email, otp, app):
    EMAIL_BaseURL = 'https://control.msg91.com/api/v5/email/send'
    EMAIL_Headers = {
        'Content-Type': 'application/json',
        'authkey': Config.OTP_AUTH_KEY
    }
    EMAIL_JSON = {
        "recipients": [
            {
            "to": [
                {
                "email": email,
                "name": name
                }
            ],
            "variables": {
                    "company_name": "1Fi",
                    "otp": otp
                }
            }
        ],
        "from": {
            "email": "no-reply-1Fi@6prfeq.mailer91.com"
        },
        "domain": "6prfeq.mailer91.com",
        "template_id": Config.EMAIL_TEMPLATE_ID
    }
    EMAIL_Response = requests.post(EMAIL_BaseURL, json=EMAIL_JSON, headers=EMAIL_Headers)
    if EMAIL_Response.status_code!=200:
        app.logger.error(f'Could not send Email OTP: {EMAIL_Response.json()}')
    else:
        # set OTP in redis
        email_otp_key = f"OTP:EMAIL:{email}"
        app.redis.set(email_otp_key, otp, ex=60)
    
    return EMAIL_Response


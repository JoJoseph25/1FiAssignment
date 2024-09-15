import random
from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from configs.extensions import DBSession as db
from descriptions.User import GET_user_responses, POST_user_signup 
from dependencies.security import get_hashed_password, verify_password
from utils.User import (check_user_exist, check_username_exist, add_user, 
                        fetch_all_user, send_sms, verify_sms, send_email)
from schemas.User import UserSingup, UserLogin, UserInfo, ResendOTP, VerifySingup

router = APIRouter()

@router.get(
    '/user',
    tags=["User"], status_code=200,
    summary="Get User Info",
    responses={**GET_user_responses},
    )
def user_info(request: Request,
            email: Optional[str] = None, 
            phone_number: Optional[str] = None,
            active: Optional[bool] = None,
        ):
    """
    Fetch user info using following parameters:
    * **email** : email of the user
    * **phone_number** : phone number of the user
    
    Note: if no query parameter given all users fetched (filter can be applied based on active).
    """
    try:
        if email:
            user = check_user_exist(email)
        elif phone_number:
            user = check_user_exist(None, phone_number)
        else:
            user = fetch_all_user(active)
        if user is None or len(user)==0:
            status_code = 404
            result = {
                'message': 'User does not exist',
                'status': False
            }            
        else:
            if isinstance(user, list):
                user_schema = [UserInfo.from_orm(u) for u in user]
            else:
                user_schema = [UserInfo.from_orm(user)]
            userJSON = jsonable_encoder(user_schema)
            status_code = 200
            result = {
                'message': 'User Record Fetched',
                'status': True, 'user': userJSON
            }
    except ValueError as e:
        request.app.logger.error(e)
        status_code = 406
        result = {
                'message': f'Error: {e}',
                'status': False
            }
    except Exception as e:
        request.app.logger.error(e)
        status_code = 500
        result = {
                'message': 'Unexpected Error',
                'status': False
            }
    finally:
        return JSONResponse(content=result, status_code=status_code)
 

@router.post(
    '/signup',
    tags=["SignUp"], status_code=201,
    summary="Add User Signup",
    responses={**POST_user_signup},
    )
def signup(request: Request, data: UserSingup):
    """
    User signup route by providing either of the following:
    * **email** : email of the user
    * **phone_number** : phone number of the user
    """
    try:
        user = check_user_exist(data.email)
        if user is None:
            user = add_user(data)
            db.commit()
            otp = random.randint(100000, 999999)
            request.app.logger.error(f"OPT: {otp}")
            # send verify SMS OTP
            if user.phone_number is not None:
                otp_send_response = send_sms(user.phone_number, request.app)
                request.app.logger.error(f"Status Code: {otp_send_response.status_code}")
                request.app.logger.error(f"Status JSON: {otp_send_response.json()}")
            
            # send verify EMAIL OTP
            if user.email is not None:
                otp = random.randint(100000, 999999)
                otp_send_response = send_email(user.full_name, user.email, otp, request.app)
            
            user_schema = UserInfo.from_orm(user)
            userJSON = jsonable_encoder(user_schema)
            result = {
                'message': 'User Created',
                'user': userJSON
            }
            status_code = 201
        else:
            status_code = 400
            result = {
                'message': 'User already exists for provided email/phone number.',
                'status': False
            }
    except ValueError as e:
        request.app.logger.error(e)
        status_code = 406
        result = {
                'message': f'Error: {e}',
                'status': False
            }
    except Exception as e:
        request.app.logger.error(e)
        status_code = 500
        result = {
                'message': 'Unexpected Error',
                'status': False
            }
    finally:
        return JSONResponse(content=result, status_code=status_code)


@router.post(
    '/login',
    tags=["Login"], status_code=201,
    summary="User Login",
    # responses={**POST_user_signup},
    )
def login(request: Request, data: UserLogin):
    """
    User login route by providing either of the following:
    * **email** : email of the user
    * **phone_number** : phone number of the user
    * **password** : password of user
    """
    try:
        if data.email:
            user = check_user_exist(data.email)
        elif data.phone_number:
            user = check_user_exist(None, data.phone_number)
        elif data.username:
            user = check_username_exist(data.username)
        else:
            user = None
            
        if user is None:
            status_code = 404
            result = {
                'message': 'User does not exist',
                'status': False
            }
        elif user.active!=True:
            status_code = 409
            result = {
                'message': 'User not verified',
                'status': False
            }
        else:
            hashed_password = get_hashed_password(data.password)
            request.app.logger.error(f"Password: {hashed_password}")
            request.app.logger.error(f"DB Password: {user.password}")
            request.app.logger.error(f"PassCheck: {verify_password(data.password, user.password)}")
            if verify_password(hashed_password, user.password):
                status_code = 200
                result = {
                    'message': 'User Login Succesfull.',
                    'status': False
                }
            else:
                status_code = 400
                result = {
                    'message': 'Incorrect Password',
                    'status': False
                }
            
    except ValueError as e:
        request.app.logger.error(e)
        status_code = 406
        result = {
                'message': f'Error: {e}',
                'status': False
            }
    except Exception as e:
        request.app.logger.error(e)
        status_code = 500
        result = {
                'message': 'Unexpected Error',
                'status': False
            }
    finally:
        return JSONResponse(content=result, status_code=status_code)


@router.post(
    '/resendOTP',
    tags=["OTP"], status_code=201,
    summary="Send User OTP",
    # responses={**POST_user_signup},
    )
def resendOTP(request: Request, data: ResendOTP):
    """
    User signup resebd OTP based on:
    * **email** : email of the user
    * **phone_number** : phone number of the user
    """
    try:
        user = check_user_exist(data.email, data.phone_number)
        if user is None:
            status_code = 404
            result = {
                'message': 'User does not exist for given email/phone number.',
                'status': False
            }
        else:
            # send mobile OTP
            if data.phone_number:
                otp_send_response = send_sms(data.phone_number, request.app)
                if otp_send_response.json()['responseCode']==506:
                    status_code = 409
                    result = {
                        'message': 'OTP sent already, try again after a minute.',
                        'status': False
                    }
                else:
                    status_code = 201
                    result = {
                        'message': 'OTP Sent succesfully.',
                        'status': True
                    }
            
            # send email OTP
            elif data.email:
                email_otp_key = f"OTP:EMAIL:{data.email}"
                email_otp = request.app.redis.get(email_otp_key)
                if email_otp is not None:
                    email_otp = email_otp.decode('utf-8')
                    status_code = 409
                    result = {
                        'message': 'OTP sent already, try again after a minute.',
                        'status': False
                    }
                else:
                    otp = random.randint(100000, 999999)
                    otp_send_response = send_email(user.full_name, data.email, otp, request.app)
                    status_code = 201
                    result = {
                        'message': 'OTP Sent succesfully.',
                        'status': True
                    }

            else:
                status_code = 400
                result = {
                    'message': 'Either phone number or email must be provided',
                    'status': False
                }              
            
    except ValueError as e:
        request.app.logger.error(e)
        status_code = 406
        result = {
                'message': f'Error: {e}',
                'status': False
            }
    except Exception as e:
        request.app.logger.error(e)
        status_code = 500
        result = {
                'message': 'Unexpected Error',
                'status': False
            }
    finally:
        return JSONResponse(content=result, status_code=status_code)
    

@router.post(
    '/verifyOTP',
    tags=["OTP"], status_code=201,
    summary="Verify User OTP",
    # responses={**POST_user_signup},
    )
def verifyOTP(request: Request, data: VerifySingup):
    """
    User signup verify using OTP based on:
    * **email** : email of the user
    * **phone_number** : phone number of the user
    """
    try:
        user = check_user_exist(data.email, data.phone_number)
        if user is None:
            status_code = 404
            result = {
                'message': 'User does not exist for given email/phone number.',
                'status': False
            }
        else:
            # verify mobile OTP
            if data.phone_number:
                sms_otp_key = f"OTP:SMS:{data.phone_number}"
                verificationID = request.app.redis.get(sms_otp_key)
                if verificationID is None:
                    status_code = 409
                    result = {
                        'message': 'OTP expired please resend.',
                        'status': False
                    }
                else:
                    verificationID = verificationID.decode('utf-8')
                    otp_send_response = verify_sms(data.otp, verificationID, request.app)
                    if otp_send_response.json()['responseCode']==200:
                        status_code = 200
                        result = {
                            'message': 'User Verified Successfully.',
                            'status': True
                        }
                        user.number_verified = True
                        if (user.number_verified==True) and (user.email_verified==True):
                            user.active=True
                        db.commit()
                    else:
                        status_code = 400
                        result = {
                            'message': 'Invalid OTP.',
                            'status': False
                        }
            
            # verify email OTP
            elif data.email:
                email_otp_key = f"OTP:EMAIL:{data.email}"
                email_otp = request.app.redis.get(email_otp_key)
                if email_otp is None:
                    status_code = 409
                    result = {
                        'message': 'OTP expired please resend.',
                        'status': False
                    }
                else:
                    email_otp = email_otp.decode('utf-8')
                    request.app.logger.debug(f'Email OTP: {email_otp}')
                    request.app.logger.debug(f'Request OTP: {data.otp}')
                    if data.otp==email_otp:
                        status_code = 200
                        result = {
                            'message': 'User Verified Successfully.',
                            'status': True
                        }
                        user.email_verified = True
                        if (user.number_verified==True) and (user.email_verified==True):
                            user.active=True
                        db.commit()
                    else:
                        status_code = 400
                        result = {
                            'message': 'Invalid OTP.',
                            'status': False
                        }

            else:
                status_code = 400
                result = {
                    'message': 'Either phone number or email must be provided',
                    'status': False
                }              
            
    except ValueError as e:
        request.app.logger.error(e)
        status_code = 406
        result = {
                'message': f'Error: {e}',
                'status': False
            }
    except Exception as e:
        request.app.logger.error(e)
        status_code = 500
        result = {
                'message': 'Unexpected Error',
                'status': False
            }
    finally:
        return JSONResponse(content=result, status_code=status_code)
    
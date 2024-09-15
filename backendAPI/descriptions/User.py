from schemas.User import UserInfo
from schemas.Common import Message

GET_user_responses = {
    200: {
        "model": UserInfo,
        "description": "Successfully registered User",
        "content": {
            "application/json": {
                "example": {
                    "message": "User Record Fetched",
                    "status": True,
                    "user": [
                        {
                            "id": "a1a1a1a1-1234-5678-9999-bbbbbbbbbbbb",
                            "username": "johndoe",
                            "full_name": "John Doe",
                            "email": "johndoe@gmail.com",
                            "phone_number": "987654321",
                            "email_verified": True,
                            "number_verified": True,
                            "active": True
                        }
                    ]
                }
            }
        },
    },
    404: {
        "model": Message,
        "description": "User Not Found",
        "content": {
            "application/json": {
                "example": {
                    "message": "User does not exist",
                    "status": False
                }
            }
        }
    },
    422: {
        "description": "Invalid payload",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "type": "value_error",
                            "loc": [
                                "body"
                            ],
                            "msg": "Value error, Either email or phone number must be provided.",
                            "input": {
                                "full_name": "John Doe",
                                "password": "password",
                                "username": "demo_user"
                            },
                            "ctx": {
                                "error": {}
                            }
                        }
                    ]
                }
            }
        }
    },
    500: {
        "model": Message,
        "description": "Server Error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Unexpected Error",
                    "status": False
                }
            }
        }
    },
}

POST_user_signup = {
    201: {
        "model": UserInfo,
        "description": "Successfully registered User",
        "content": {
            "application/json": {
                "example": {
                    "message": "User Created",
                    "user": {
                        "id": "a1a1a1a1-1234-5678-9999-bbbbbbbbbbbb",
                        "username": "johndoe",
                        "full_name": "John Doe",
                        "email": "johndoe@gmail.com",
                        "phone_number": "987654321",
                        "email_verified": True,
                        "number_verified": True,
                        "active": True
                    }
                }
            }
        },
    },
    400: {
        "model": Message,
        "description": "User Already Exists",
        "content": {
            "application/json": {
                "example": {
                    "message": "User already exists for provided email/phone number.",
                    "status": False
                }
            }
        }
    },
    422: {
        "description": "Invalid payload",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "type": "value_error",
                            "loc": [
                                "body"
                            ],
                            "msg": "Value error, Either email or phone number must be provided.",
                            "input": {
                                "full_name": "John Doe",
                                "password": "password",
                                "username": "demo_user"
                            },
                            "ctx": {
                                "error": {}
                            }
                        }
                    ]
                }
            }
        }
    },
    500: {
        "model": Message,
        "description": "Server Error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Unexpected Error",
                    "status": False
                }
            }
        }
    },
}

POST_user_login = {
    200: {
        "model": Message,
        "description": "User Succesfully Login",
        "content": {
            "application/json": {
                "example": {
                    "message": "User Login Successfull.",
                    "status": True
                }
            }
        },
    },
    400: {
        "model": Message,
        "description": "Incorrect Credentials",
        "content": {
            "application/json": {
                "example": {
                    "message": "Incorrect Password.",
                    "status": False
                }
            }
        }
    },
    404: {
        "model": Message,
        "description": "User Not Found",
        "content": {
            "application/json": {
                "example": {
                    "message": "User does not exist.",
                    "status": False
                }
            }
        }
    },
    409: {
        "model": Message,
        "description": "User Not Verified/Active",
        "content": {
            "application/json": {
                "example": {
                    "message": "User not verified.",
                    "status": False
                }
            }
        }
    },
    422: {
        "description": "Invalid payload",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "type": "value_error",
                            "loc": [
                                "body"
                            ],
                            "msg": "Value error, Either email or phone number must be provided.",
                            "input": {
                                "full_name": "John Doe",
                                "password": "password",
                                "username": "demo_user"
                            },
                            "ctx": {
                                "error": {}
                            }
                        }
                    ]
                }
            }
        }
    },
    500: {
        "model": Message,
        "description": "Server Error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Unexpected Error",
                    "status": False
                }
            }
        }
    },
}

POST_resendOTP = {
    201: {
        "model": Message,
        "description": "OTP sent successfully",
        "content": {
            "application/json": {
                "example": {
                    "message": "OTP Sent successfully.",
                    "status": True
                }
            }
        },
    },
    400: {
        "model": Message,
        "description": "Incorrect Request",
        "content": {
            "application/json": {
                "example": {
                    "message": "Either phone number or email must be provided.",
                    "status": False
                }
            }
        }
    },
    404: {
        "model": Message,
        "description": "User Not Found",
        "content": {
            "application/json": {
                "example": {
                    "message": "User does not exist for given email/phone number.",
                    "status": False
                }
            }
        }
    },
    409: {
        "model": Message,
        "description": "Retry after a while",
        "content": {
            "application/json": {
                "example": {
                    "message": "OTP sent already, try again after a minute.",
                    "status": False
                }
            }
        }
    },
    422: {
        "description": "Invalid payload",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "type": "value_error",
                            "loc": [
                                "body"
                            ],
                            "msg": "Value error, Either email or phone number must be provided.",
                            "input": {
                                "full_name": "John Doe",
                                "password": "password",
                                "username": "demo_user"
                            },
                            "ctx": {
                                "error": {}
                            }
                        }
                    ]
                }
            }
        }
    },
    500: {
        "model": Message,
        "description": "Server Error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Unexpected Error",
                    "status": False
                }
            }
        }
    },
}

POST_verifyOTP = {
    200: {
        "model": Message,
        "description": "OTP Verified",
        "content": {
            "application/json": {
                "example": {
                    "message": "User Verified Successfully.",
                    "status": True
                }
            }
        },
    },
    400: {
        "model": Message,
        "description": "Incorrect OTP",
        "content": {
            "application/json": {
                "example": {
                    "message": "Invalid OTP.",
                    "status": False
                }
            }
        }
    },
    409: {
        "model": Message,
        "description": "OTP expired",
        "content": {
            "application/json": {
                "example": {
                    "message": "OTP expired please resend.",
                    "status": False
                }
            }
        }
    },
    422: {
        "description": "Invalid payload",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "type": "value_error",
                            "loc": [
                                "body"
                            ],
                            "msg": "Value error, Either email or phone number must be provided.",
                            "input": {
                                "full_name": "John Doe",
                                "password": "password",
                                "username": "demo_user"
                            },
                            "ctx": {
                                "error": {}
                            }
                        }
                    ]
                }
            }
        }
    },
    500: {
        "model": Message,
        "description": "Server Error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Unexpected Error",
                    "status": False
                }
            }
        }
    },
}














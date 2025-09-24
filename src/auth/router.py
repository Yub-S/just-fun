from fastapi import APIRouter, Depends,status
from fastapi.exceptions import HTTPException
from src.auth.service import UserService
from datetime import timedelta, datetime
from src.auth.scheme import createuserdata,logindata, user, UserBookModel, EmailModel, Passwordreset, NewPassword
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.utils import verify_password_hash,create_access_token,decode_token
from fastapi.responses import JSONResponse
from src.auth.dependency import tokenbearer,accesstokenbearer,refreshtokenbearer, get_current_user
from src.db.redis import add_jti_to_blocklist
from src.auth.dependency import RoleChecker
from src.mail import create_message, mail
from src.auth.utils import create_url_safe_token , decode_url_safe_token, generate_password_hash
from src.config import Config
from fastapi import BackgroundTasks
from src.celery import send_email


auth_router = APIRouter()
userservice = UserService()

role_checker = RoleChecker(["admin", "user"])

# signup
@auth_router.post("/signup", status_code = status.HTTP_201_CREATED)
async def create_new_user(userdata:createuserdata,bg_task: BackgroundTasks, session:AsyncSession = Depends(get_session)):
    email = userdata.email
    user_exist = await userservice.user_exits(email,session)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user already exits")
    user_data =  await userservice.create_user(userdata,session)

    token = create_url_safe_token({"email":email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"
    html_message = f"""
    <h1>Verify your email</h1>
    <p>Please click this <a href = "{link}">link</a> to verify your email</p>"""

    message = create_message(recipients=[email],subject="verify your email",body =html_message)

    #await mail.send_message(message)
    # using background tasks to do this operation
    #bg_task.add_task(mail.send_message,message)
    # using celery to do this operation
    send_email.delay(recipients=[email],subject="verify your email",body =html_message)

    return {
        "message":"Account created! Check email for verification",
        "user":user_data
    }

@auth_router.get("/verify/{token}")
async def verify_user(token:str,session:AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data
    if user_email:
        user = await userservice.get_user_by_email(user_email,session)

        if not user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)

        return JSONResponse(
            content = {
                "message":"Account verified successfully ",
            },
            status_code = status.HTTP_200_OK
        )
    return JSONResponse(
        content = {
            "message":"cannot verify your account"
        },
        status_code = status.HTTP_200_OK
    )
    

# login 
@auth_router.post("/login")
async def login_users(login_data:logindata,session:AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await userservice.get_user_by_email(email,session)
    if user is not None:
        is_password_valid= verify_password_hash(password,user.password_hash)

        if is_password_valid:
            access_token = create_access_token(userdata = {
                "email":email,
                "user_uid":str(user.uid)
            })

            refresh_token = create_access_token(userdata = {
                "email":email,
                "user_uid":str(user.uid)
            },
            refresh=True,
            expiry=timedelta(days =1))


            return JSONResponse(
                content = {
                    "message":"login_successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{"email":user.email,"uid":str(user.uid)}
                }
            )
        
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "invalid email or password"
    )
        
@auth_router.get("/refresh_token")
async def get_new_access_token(token_details:dict=Depends(refreshtokenbearer())):
    expiry_date = token_details["exp"]

    if datetime.fromtimestamp(expiry_date) > datetime.now():
        new_access_token = create_access_token(token_details["user"])
        return JSONResponse (content = {"access_token" : new_access_token})
    
    raise HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST, details = "invalid or expired token"
    )


@auth_router.get("/logout")
async def revoke_token(token_details:dict=Depends(accesstokenbearer())):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(content={"message":"logout succesfully"}, status_code=status.HTTP_200_OK)

@auth_router.get("/me", response_model=UserBookModel)
async def get_current_user(user=Depends(get_current_user), _:bool=Depends(role_checker)):
    return user


@auth_router.post("/send_mail")
async def send_mail(email:EmailModel):
    email_address = email.address

    html = "<h1>welcome to the app</h1>"
    subject = "welcome to bookly"

    message = create_message(recipients=email_address,
                             subject=subject,
                             body=html)
    
    await mail.send_message(message)
    return {"message":"email sent successfully "}



@auth_router.post("/reset-request")
async def password_reset(email_data:Passwordreset):
    user_email = email_data.email

    token = create_url_safe_token(user_email)

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset/{token}"

    html_request = f""""
    <h1>Reset Your Password</h1>
    <p>Please click the link <a href = "{link}">link</a> to change password </p>
    """

    subject = "Reset Your Password"

    message = create_message(
        recipients=[user_email],
        subject=subject,
        body=html_request

    )

    await mail.send_message(message)
    return JSONResponse(
        content = {
            "message":"Please check your email for instruction to reset your password"
        },
        status_code = status.HTTP_200_OK
    )

@auth_router.post("/password-reset/{token}")
async def set_new_password(token:str,
                           passwords: NewPassword,
                           session:AsyncSession=Depends(get_session)):
    new_password = passwords.new_password
    confirmed_password = passwords.confirm_new_password

    if new_password!=confirmed_password:
        raise HTTPException(
            detail="Passwords do not match",
            status_code = status.HTTP_404_BAD_REQUEST
        )
    
    token_data = decode_url_safe_token(token)
    user_email = token_data

    if user_email:
        user = await userservice.get_user_by_email(user_email,session)
        if not user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
        
        password_hash = generate_password_hash(new_password)

        return JSONResponse(
            content = {
                "message":f"Your new password hash is {password_hash}",
            },
            status_code = status.HTTP_200_OK
        )
    return JSONResponse(
        content = {
            "message":"cannot change password"
        },
        status_code = status.HTTP_200_OK
    )


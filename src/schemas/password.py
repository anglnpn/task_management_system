import re

from pydantic import BaseModel, field_validator, Field

from constants.password import MIN_PASSWORD_LENGTH


class PasswordBase(BaseModel):
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def password_validation(cls, password: str) -> str:
        if len(password) < MIN_PASSWORD_LENGTH and not re.match(
            r"^[ -~]+$", password
        ):
            msg = "Password does not meet the requirements."
            raise ValueError(msg)
        return password

from pydantic import BaseModel, Field, PastDate


class DateOfBirth(BaseModel):
    dateOfBirth: PastDate = Field(
        title="The birthday of the user",
        description="The birthday of the user. Required format YYYY-MM-DD, Cannot be today or any future date.",
    )


class Username(BaseModel):
    username: str = Field(
        title="Username of the user",
        description="The username choosed by the user. Must contain only letters and be unique.",
        pattern="^[a-zA-Z]+$",
    )

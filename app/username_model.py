from pydantic import BaseModel, Field


class Username(BaseModel):
    username: str = Field(
        title="Username of the user",
        description="The username choosed by the user. Must contain only letters and be unique.",
        pattern="^[a-zA-Z]+$",
    )

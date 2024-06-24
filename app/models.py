"""Models for check data used by application endpoints."""

from pydantic import BaseModel, Field, PastDate


class DateOfBirth(BaseModel):
    dateOfBirth: PastDate = Field(
        title="The birthday of the user",
        description="The birthday of the user. Required format YYYY-MM-DD, Cannot be today or any future date.",
    )

from beanie import Document
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class Member(BaseModel):
    """Represents a team member with technical skills and preferences."""

    tech_field: List[str] = Field(default_factory=list)
    gender: Optional[str] = None
    major: Optional[str] = None
    planguage: List[str] = Field(default_factory=list)
    already_know: Optional[bool] = None


class TeamRequest(Document):
    """Represents a team formation request document in MongoDB."""

    id: Optional[str] = None
    user_personal_phone: Optional[str] = None
    user_name: str
    user_gender: Optional[str] = None
    user_abstract: Optional[str] = None
    members: List[Member] = Field(default_factory=list)
    owner_fingerprint: str = Field(..., alias="ownerFingerprint")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        """Beanie configuration settings for the TeamRequest model."""

        name = "teamrequests"  # Collection name in MongoDB
        use_state_management = True

    async def save(self, *args, **kwargs):
        """Update the updated_at timestamp before saving."""

        self.updated_at = datetime.now()
        return await super().save(*args, **kwargs)

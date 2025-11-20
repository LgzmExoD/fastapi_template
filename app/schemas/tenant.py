from typing import Optional

from pydantic import BaseModel, ConfigDict


class TenantBase(BaseModel):
    name: str
    schema_name: Optional[str] = None
    is_active: Optional[bool] = True


class TenantCreate(TenantBase):
    pass


class TenantUpdate(TenantBase):
    pass


class TenantInDBBase(TenantBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Tenant(TenantInDBBase):
    pass

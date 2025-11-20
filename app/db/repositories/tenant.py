from app.db.repository import BaseRepository
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


class TenantRepository(BaseRepository[Tenant, TenantCreate, TenantUpdate]):
    pass


tenant = TenantRepository(Tenant)

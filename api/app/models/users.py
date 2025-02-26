from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, UUID, Boolean

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(255))
    address_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    identity_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f'<{self.full_name} {self.email}>'
    
    def check_activation(self):
        if (self.identity_verified and self.email_verified and self.address_verified):
            self.is_active = True
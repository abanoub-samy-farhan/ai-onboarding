from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, CHAR, Boolean

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id: Mapped[CHAR] = mapped_column(CHAR(36), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    national_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True)
    identity_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    documents = db.relationship('Document', back_populates='user', cascade='all, delete-orphan')
    user_sessions = db.relationship('UserSession', back_populates='user', cascade='all, delete-orphan')
    tokens = db.relationship('Token', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<{self.full_name} {self.email}>'
    
    def check_activation(self):
        if (self.identity_verified and self.email_verified and self.address_verified):
            self.is_active = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'national_id': self.national_id,
            'address': self.address,
            'phone_number': self.phone_number,
            'identity_verified': self.identity_verified,
            'email_verified': self.email_verified,
            'is_active': self.is_active
        }
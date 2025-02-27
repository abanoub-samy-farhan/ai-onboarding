from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, CHAR, Boolean, DateTime, ForeignKey

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    __table_args__ = {'extend_existing': True}

    user_id: Mapped[CHAR] = mapped_column(CHAR(36), ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User', back_populates='user_sessions')
    access_token: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)



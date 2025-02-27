from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Column, ForeignKey, DateTime, Boolean, CHAR


class Document(db.Model):
    __tablename__ = 'documents'
    __table_args__ = {'extend_existing': True}


    id: Mapped[CHAR] = mapped_column(CHAR(36), primary_key=True)
    user_id: Mapped[CHAR] = mapped_column(CHAR(36), ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='documents')
    photo_uri: Mapped[str] = mapped_column(String(255), nullable=True)
    national_id_uri: Mapped[str] = mapped_column(String(255), nullable=True)
    live_video_uri: Mapped[str] = mapped_column(String(255), nullable=True)
    proof_of_income_uri: Mapped[str] = mapped_column(String(255), nullable=True)
    proof_of_address_uri: Mapped[str] = mapped_column(String(255), nullable=True)

    
    def __repr__(self):
        return f'<{self.name}> '
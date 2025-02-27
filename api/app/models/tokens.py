from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, CHAR, ForeignKey

class Token(db.Model):
    __tablename__ = 'tokens'
    __table_args__ = {'extend_existing': True}


    token: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[CHAR] = mapped_column(CHAR(36), ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='tokens')


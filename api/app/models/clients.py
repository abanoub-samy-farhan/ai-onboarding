from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, CHAR, ForeignKey

class Client(db.Model):
    __tablename__ = 'clients'
    __table_args__ = {'extend_existing': True}


    client_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_secret: Mapped[CHAR] = mapped_column(CHAR(36), nullable=False)

    def to_dict(self):
        return {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
    
class ClientAccessTokens(db.Model):
    __tablename__ = 'clients_access_tokens'
    __table_args__ = {'extend_existing': True}

    token: Mapped[CHAR] = mapped_column(CHAR(36))
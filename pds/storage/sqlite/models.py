from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class DataBlock(Base):
    __tablename__ = "datablock"

    cid: Mapped[bytes] = mapped_column(primary_key=True)
    content: Mapped[bytes]
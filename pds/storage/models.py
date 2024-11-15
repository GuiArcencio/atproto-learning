from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class RepoBase(DeclarativeBase):
    pass

class DataBlock(RepoBase):
    __tablename__ = "datablock"

    cid: Mapped[bytes] = mapped_column(primary_key=True)
    content: Mapped[bytes]

from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, joinedload

engine = create_engine("sqlite:///./sql_app.db", future=True,
                       echo=True, connect_args={"check_same_thread": False})
# engine = create_engine("sqlite+pysqlite:///:memory:", future=True,
#                        echo=True, connect_args={"check_same_thread": False})
# ===================================================
# Make the DeclarativeMeta
Base = declarative_base()

class RoleUser(Base):
    __tablename__ = 'role_users'
    role_id = Column(ForeignKey('roles.id'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    blurb = Column(String, nullable=False)
    role = relationship("Role", back_populates="users")
    user = relationship("User", back_populates="roles")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # users = relationship("User", secondary="role_users", back_populates="roles")
    users = relationship("RoleUser", back_populates="role")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    # roles = relationship("Role", secondary="role_users", back_populates="users")
    roles = relationship("RoleUser", back_populates="user")





# Create the tables in the database
Base.metadata.create_all(engine)
# ===================================================


class UserBase(BaseModel):
    id: int
    username: str
    blurb: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    id: int
    name: str
    blurb: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserBase):
    roles: List[RoleBase]


class RoleSchema(RoleBase):
    users: List[UserBase]


# ===================================================
# Insert data
with Session(bind=engine) as session:
    role1 = Role(name="user")
    role2 = Role(name="moderator")
    role3 = Role(name="admin")

    user1 = User(username="normal")
    user2 = User(username="superadmin")

#     user1.roles = [role1, role3]
#     user2.roles = [role2, role3]

    session.add_all([role1, role2, role3, user1, user2])
    session.commit()
    print("=========== Role, User")

    role_user1 = RoleUser(role_id=role1.id, user_id=user1.id, blurb="Blue wrote chapter 1")
    role_user2 = RoleUser(role_id=role2.id, user_id=user1.id, blurb="Chip wrote chapter 2")
    role_user3 = RoleUser(role_id=role2.id, user_id=user2.id, blurb="Blue wrote chapters 1-3")
    role_user4 = RoleUser(role_id=role3.id, user_id=user2.id, blurb="Alyssa wrote chapter 4")

    session.add_all([role_user1, role_user2, role_user3, role_user4])
    session.commit()
    print("=========== Blurb")

# ===================================================
with Session(bind=engine) as session:
    db_role = session.query(Role).first()
    print("=========== ", db_role.users[0].blurb)
    print("=========== ", db_role.users[0].user.username)


# ===================================================
# with Session(bind=engine) as session:
#     # b1 = session.query(Role).where(Role.id == 2).one()
#     b1 = session.query(Role).options(
#         joinedload(Role.users)).where(Role.id == 2).one()
#     print("------------- Role: ", b1.name)
#     for a in b1.users:
#         print("------------- User: ", a.username)

# ===================================================
# app = FastAPI(title="Bookipedia")


# def get_db():
#     db = Session(bind=engine)
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get("/roles/{id}", response_model=RoleSchema)
# async def get_role(id: int, db: Session = Depends(get_db)):
#     db_role = db.query(Role).options(
#         joinedload(Role.users)).where(Role.id == id).one()
#     return db_role


# @app.get("/roles", response_model=List[RoleSchema])
# async def get_roles(db: Session = Depends(get_db)):
#     db_roles = db.query(Role).options(joinedload(Role.users)).all()
#     return db_roles


# @app.get("/users", response_model=List[UserSchema])
# async def get_users(db: Session = Depends(get_db)):
#     db_users = db.query(User).options(joinedload(User.roles)).all()
#     return db_users


# @app.get("/user/{id}", response_model=UserSchema)
# async def get_user(id: int, db: Session = Depends(get_db)):
#     db_user = db.query(User).options(
#         joinedload(User.roles)).where(User.id == id).one()
#     return db_user

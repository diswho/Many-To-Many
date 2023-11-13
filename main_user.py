from sqlalchemy.ext.associationproxy import association_proxy
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, joinedload

# engine = create_engine("sqlite:///./sql_user.db", future=True,
#                        echo=True, connect_args={"check_same_thread": False})
engine = create_engine("sqlite+pysqlite:///:memory:", future=True,
                       echo=True, connect_args={"check_same_thread": False})
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
    # proxies
    role_name = association_proxy(target_collection='role', attr="name")
    user_name = association_proxy(target_collection='user', attr="name")


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    users = relationship("RoleUser", back_populates="role")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    roles = relationship("RoleUser", back_populates="user")


# Create the tables in the database
Base.metadata.create_all(engine)
# ===================================================


class UserBase(BaseModel):
    id: int = Field(alias='user_id')
    name: str = Field(alias='user_name')
    blurb: Optional[str] = None

    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    model_config = ConfigDict(from_attributes=True)
    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True, extra='allow')


class RoleBase(BaseModel):
    id: int = Field(alias='role_id')
    name: str = Field(alias='role_name')
    blurb: Optional[str] = None

    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    # model_config = ConfigDict(from_attributes=True)
    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True, extra='allow')


class UserSchema(UserBase):
    roles: List[RoleBase]


class RoleSchema(RoleBase):
    users: List[UserBase]


# ===================================================# Insert data
with Session(bind=engine) as session:
    role1 = Role(name="user")
    role2 = Role(name="moderator")
    role3 = Role(name="admin")

    user1 = User(name="normal")
    user2 = User(name="superadmin")

#     user1.roles = [role1, role3]
#     user2.roles = [role2, role3]

    session.add_all([role1, role2, role3, user1, user2])
    session.commit()
    print("=========== Role, User")

    role_user1 = RoleUser(role_id=role1.id, user_id=user1.id,
                          blurb="Blue wrote chapter 1")
    role_user2 = RoleUser(role_id=role2.id, user_id=user1.id,
                          blurb="Chip wrote chapter 2")
    role_user3 = RoleUser(role_id=role2.id, user_id=user2.id,
                          blurb="Blue wrote chapters 1-3")
    role_user4 = RoleUser(role_id=role3.id, user_id=user2.id,
                          blurb="Alyssa wrote chapter 4")

    session.add_all([role_user1, role_user2, role_user3, role_user4])
    session.commit()
    print("=========== Blurb")

# ===================================================
# with Session(bind=engine) as session:
#     # db_role = session.query(Role).options(joinedload(Role.users).options(joinedload(RoleUser.user))).first()
#     db_role = session.query(Role).options(
#         joinedload(Role.users)).where(Role.id == 1).one()
#     schema_role = RoleSchema.model_validate(db_role)
#     print("========= db_book: ", schema_role.model_dump_json())
# ===================================================
app = FastAPI(title="Bookipedia")


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/roles/{id}", response_model=RoleSchema)
async def get_role(id: int, db: Session = Depends(get_db)):
    db_role = db.query(Role).options(joinedload(Role.users)).where(Role.id == id).one()
    return db_role


@app.get("/roles", response_model=List[RoleSchema])
async def get_roles(db: Session = Depends(get_db)):
    db_roles = db.query(Role).options(joinedload(Role.users)).all()
    return db_roles


@app.get("/users", response_model=List[UserSchema])
async def get_users(db: Session = Depends(get_db)):
    db_users = db.query(User).options(joinedload(User.roles)).all()
    return db_users


@app.get("/user/{id}", response_model=UserSchema)
async def get_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).options(
        joinedload(User.roles)).where(User.id == id).one()
    return db_user

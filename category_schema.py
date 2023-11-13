from __future__ import annotations
from typing import List
from pydantic import BaseModel
from datetime import datetime


class CategoryBase(BaseModel):
    label: str

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    suppliers: List[Supplier]


from .supplier_schema import Supplier  # nopep8
Category.update_forward_refs()


class CategorySkeleton(CategoryBase):
    pass


class CategoryPatch(CategoryBase):
    pass

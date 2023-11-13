from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
# import schemas


class SupplierBase(BaseModel):
    company_email: Optional[str] = None
    logo: Optional[str] = None
    state_province: str = None
    city_area: Optional[str] = None
    location: Optional[str] = None
    company_phone: str = None
    fax: Optional[str] = None
    tagline: Optional[str] = None
    company_bio: Optional[str] = None
    postal_code: Optional[str] = None
    year_established: str = None
    employees_count: Optional[str] = None
    certificates: Optional[List[dict]] = []
    cover_image: Optional[str] = None
    gallery: Optional[List[dict]] = None
    license: Optional[str] = None
    website: Optional[str] = None
    whatsapp_number: Optional[str] = None
    facebook_url: Optional[str] = None
    twitter_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    pinterest_url: Optional[str] = None
    instagram_url: Optional[str] = None
    youtube_url: Optional[str] = None
    annual_revenue: Optional[str] = None
    payment_methods: Optional[List[dict]] = None
    challenges: Optional[List[str]] = []
    status: str = None
    user_id: int

    class Config:
        orm_mode = True


class SupplierCreate(SupplierBase):
    pass


class Supplier(SupplierBase):
    id: int
    categories: Optional[List[Category]] = []
    created_at: datetime
    updated_at: datetime


from .category_schema import Category  # nopep8
Category.update_forward_refs()

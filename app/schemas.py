from pydantic import BaseModel, PositiveInt, constr


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True


class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)

    class Config:
        orm_mode = True

class Category(BaseModel):
    CategoryID: PositiveInt
    CategoryName: constr(max_length=15) = None

    class Config:
        orm_mode = True

class ProductsRelated(BaseModel):
    ProductID: PositiveInt
    ProductName: constr(max_length=40)
    Category: Category
    Discontinued: bool = None

    class Config:
        orm_mode = True
    
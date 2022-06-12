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

class AddSupplier(BaseModel):
    CompanyName: constr(max_length=40) | None = ""
    ContactName: constr(max_length=40) | None = None
    ContactTitle: constr(max_length=40) | None = None
    Address: constr(max_length=40) | None = None
    City: constr(max_length=40) | None = None
    PostalCode: constr(max_length=40) | None = None
    Country: constr(max_length=40) | None = None
    Phone: constr(max_length=40) | None = None
    Fax: constr(max_length=40) | None = None
    HomePage: constr(max_length=40) | None = None


    class Config:
        orm_mode = True
 
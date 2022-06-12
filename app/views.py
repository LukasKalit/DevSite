from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models

from . import crud, schemas
from .database import get_db


router = APIRouter()


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)



@router.get("/suppliers/{supplier_id}")
async def read_user(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    print(type(db))
    print(type(supplier_id))
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_supplier


@router.get("/suppliers", response_model=List[schemas.Supplier])
async def read_users(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)





@router.get("/suppliers/{supplier_id}/products", response_model=List[schemas.ProductsRelated] )
def read_product(supplier_id: PositiveInt, db: Session = Depends(get_db)):

    if crud.get_supplier(db, supplier_id) is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    result = crud.get_products_related(db, supplier_id)
    
    for item in result:
        db_category = crud.get_categories_related(db, item.CategoryID)
        schemas.Category(CategoryID=db_category.CategoryID, CategoryName=db_category.CategoryName)
        item.Category = schemas.Category(CategoryID=db_category.CategoryID, CategoryName=db_category.CategoryName)

    return result

@router.post("/suppliers", status_code=201)
def create_supplier(response: Response, supplier: schemas.AddSupplier, db: Session = Depends(get_db)):
    # print(supplier)
    data = supplier.dict()
    # print(data)
    all_suppliers = crud.get_suppliers(db)
    lastID = -1
    for i in all_suppliers:
        if i.SupplierID > lastID:
            lastID = i.SupplierID
    lastID += 1

    for i in all_suppliers:
        if i.CompanyName == data["CompanyName"]:
            raise HTTPException(status_code=400, detail="Duplicated supplier")

    if supplier.CompanyName == "":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response
    return crud.add_suppliers(db, item=supplier, SupplierID=lastID)
    
@router.put("/suppliers/{id}")
def update_supplier(response:Response, supplier: schemas.AddSupplier, id: int, db: Session = Depends(get_db)):
    flag = True
    all_suppliers = crud.get_suppliers(db)
    for i in all_suppliers:
        if i.SupplierID == id:
            flag = False
    if flag:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    
    return crud.update_supplier(db, id, supplier)


@router.delete("/suppliers/{id}", status_code=204)
def update_supplier(response:Response, id: int, db: Session = Depends(get_db)):
    flag = True
    all_suppliers = crud.get_suppliers(db)
    for i in all_suppliers:
        if i.SupplierID == id:
            flag = False
    if flag:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    
    return crud.delete_supplier(db, id)

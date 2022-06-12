from sqlalchemy.orm import Session, Bundle
from sqlalchemy import select

from . import models



def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )

def get_suppliers(db: Session):
    return db.query(models.Supplier).all()

def get_supplier(db: Session, supplier_id: int):
    return (db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first())




def get_products_related(db: Session, supplier_id: int):
    return db.query(models.Product).filter(models.Product.SupplierID == supplier_id).order_by(models.Product.ProductID.desc()) .all()

def get_categories_related(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.CategoryID == category_id).first()


def add_suppliers(db: Session, item, SupplierID: int):
    db_user = models.Supplier(**item.dict(), SupplierID = SupplierID)
    print(type(item))
    print(type(db_user))
    print(item)
    print(db_user)
    
    # print(db_user.SupplierID,db_user.CompanyName )
    # db_user_json = db_user.json()
    # intiger_some = db_user_json.get("SupplierID")
    # print(intiger_some)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_supplier(db: Session, id: int, supplier_data):
    data = db.query(models.Supplier).filter(models.Supplier.SupplierID == id).first()
    supplier_data = supplier_data.dict()
    if supplier_data["CompanyName"] != "":
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).update({"CompanyName": supplier_data["CompanyName"]})
    if supplier_data["ContactName"] != "":
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).update({"ContactName": supplier_data["ContactName"]})
    if supplier_data["ContactTitle"] != "":
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).update({"ContactTitle": supplier_data["ContactTitle"]})
    db.commit()
    db.refresh(data)
    # print(data.CompanyName)
    # print(supplier_data)
    return data

def delete_supplier(db: Session, id: int):
    # data = db.query(models.Supplier).filter(models.Supplier.SupplierID == id).first()
    db.query(models.Supplier).filter(models.Supplier.SupplierID == id).delete()
    db.commit()
    return "Record deleted"


    

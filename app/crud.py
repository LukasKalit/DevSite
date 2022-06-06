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

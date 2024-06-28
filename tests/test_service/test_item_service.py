# test_item_model.py
import pytest
from datetime import datetime
from src.model.models import Item, PrecioHistorico, TipoItem
from sqlalchemy.exc import IntegrityError

def test_create_item(session):
    """Test the creation of an item."""
    tipo_item = TipoItem(nombre="Producto")
    session.add(tipo_item)
    session.commit()

    item = Item(nombre="Item Test", descripcion="Descripción del item de prueba", tipo_id=tipo_item.id)
    session.add(item)
    session.commit()

    # Act
    retrieved = session.query(Item).first()
    
    # Assert
    assert item.nombre == "Item Test"
    assert item.descripcion == "Descripción del item de prueba"
    assert item.tipo_id == tipo_item.id

def test_update_existing_item(session):
    tipo_item = TipoItem(nombre="Producto")
    session.add(tipo_item)
    session.commit()

    item = Item(nombre="Initial Item", descripcion="Descripción inicial", tipo_id=tipo_item.id)
    session.add(item)
    session.commit()

    # Act
    item.nombre = "Updated Item"
    session.commit()

    # Assert
    updated_item = session.query(Item).filter_by(nombre="Updated Item").first()
    assert updated_item.nombre == "Updated Item"

def test_create_precio_historico(session):
    tipo_item = TipoItem(nombre="Producto")
    session.add(tipo_item)
    session.commit()

    item = Item(nombre="Item Test", descripcion="Descripción del item de prueba", tipo_id=tipo_item.id)
    session.add(item)
    session.commit()

    fecha_vigencia_inicio = datetime.strptime("2023-01-01", "%Y-%m-%d").date()
    precio_historico = PrecioHistorico(item_id=item.id, precio=100.00, fecha_vigencia_inicio=fecha_vigencia_inicio)
    session.add(precio_historico)
    session.commit()

    # Act
    retrieved_precio = session.query(PrecioHistorico).first()

    # Assert
    assert retrieved_precio.item_id == item.id
    assert retrieved_precio.precio == 100.00
    assert retrieved_precio.fecha_vigencia_inicio == fecha_vigencia_inicio
    assert retrieved_precio.fecha_vigencia_fin == datetime(3000, 12, 31).date()

def test_update_precio_historico(session):
    tipo_item = TipoItem(nombre="Producto")
    session.add(tipo_item)
    session.commit()

    item = Item(nombre="Item Test", descripcion="Descripción del item de prueba", tipo_id=tipo_item.id)
    session.add(item)
    session.commit()

    precio_historico = PrecioHistorico(item_id=item.id, precio=100.00, fecha_vigencia_inicio=datetime.now().date())
    session.add(precio_historico)
    session.commit()

    # Act
    precio_historico.precio = 150.00
    session.commit()

    # Assert
    updated_precio = session.query(PrecioHistorico).filter_by(item_id=item.id).first()
    assert updated_precio.precio == 150.00

def test_duplicate_item_insertion(session):
    tipo_item = TipoItem(nombre="Producto")
    session.add(tipo_item)
    session.commit()

    item1 = Item(nombre="Item Duplicado", descripcion="Primera descripción", tipo_id=tipo_item.id)
    session.add(item1)
    session.commit()

    item2 = Item(nombre="Item Duplicado", descripcion="Segunda descripción", tipo_id=tipo_item.id)

    with pytest.raises(IntegrityError):
        session.add(item2)
        session.commit()

def test_delete_item(session):
    tipo_item = TipoItem(nombre="Producto")
    session.add(tipo_item)
    session.commit()

    item = Item(nombre="Item a Eliminar", descripcion="Descripción del item", tipo_id=tipo_item.id)
    session.add(item)
    session.commit()

    session.delete(item)
    session.commit()

    deleted_item = session.query(Item).filter_by(nombre="Item a Eliminar").first()
    assert deleted_item is None

def test_insert_item_without_required_fields(session):
    item = Item()  # no fields set

    with pytest.raises(IntegrityError):
        session.add(item)
        session.commit()

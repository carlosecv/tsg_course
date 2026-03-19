import xmlrpc.client

# Configuración de conexión
url = "http://localhost:8069"
db = "odoodemo18"
username = "admin"
password = "admin"

# Conexión al endpoint de autenticación
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")

# Autenticación
uid = common.authenticate(db, username, password, {})
if not uid:
    raise Exception("No fue posible autenticarse en Odoo. Revisa base, usuario o contraseña.")

print(f"Conectado correctamente. UID: {uid}")

# Conexión al endpoint de objetos
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Buscar todos los registros de estate.property
property_ids = models.execute_kw(
    db,
    uid,
    password,
    "estate.property",
    "search",
    [[]]   # dominio vacío = todos los registros
)

print("IDs encontrados:", property_ids)

# Leer algunos campos de esos registros
properties = models.execute_kw(
    db,
    uid,
    password,
    "estate.property",
    "read",
    [property_ids],
    {
        "fields": ["id", "name", "expected_price", "selling_price", "state"]
    }
)

print("\nPropiedades encontradas:\n")
for prop in properties:
    print(f"ID: {prop['id']}")
    print(f"Nombre: {prop.get('name')}")
    print(f"Precio esperado: {prop.get('expected_price')}")
    print(f"Precio venta: {prop.get('selling_price')}")
    print(f"Estado: {prop.get('state')}")
    print("-" * 40)

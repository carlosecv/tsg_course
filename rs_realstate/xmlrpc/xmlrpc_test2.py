import xmlrpc.client

url = "http://localhost:8069"
db = "odoodemo18"
username = "admin"
password = "admin"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if not uid:
    raise Exception("Error de autenticación")

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

properties = models.execute_kw(
    db,
    uid,
    password,
    "estate.property",
    "search_read",
    [[]],
    {
        "fields": ["id", "name", "expected_price", "selling_price", "state"],
        "order": "id asc"
    }
)
print("\nListado de estate.property:\n")
for prop in properties:
    print(
        f"ID: {prop['id']} | "
        f"Nombre: {prop.get('name')} | "
        f"Esperado: {prop.get('expected_price')} | "
        f"Venta: {prop.get('selling_price')} | "
        f"Estado: {prop.get('state')}"
    )

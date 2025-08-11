from fastapi import APIRouter
router = APIRouter()
PRESETS = [
    {"group":"Identidad","items":[
        {"name":"DNI","label":"DNI","type":"text","required":True,"mask":{"regex":"^\\d{8}$","hint":"8 dígitos"}},
        {"name":"RUC","label":"RUC","type":"text","required":True,"mask":{"regex":"^\\d{11}$","hint":"11 dígitos"}},
        {"name":"EMAIL","label":"Correo","type":"email","required":True,"mask":{"regex":"^[^@\s]+@[^@\s]+\.[^@\s]+$","hint":"correo válido"}},
        {"name":"NOMBRES","label":"Nombres","type":"text","required":True,"transform":"uppercase"},
        {"name":"APELLIDOS","label":"Apellidos","type":"text","required":True,"transform":"uppercase"}
    ]},
    {"group":"Ubicación","items":[
        {"name":"DEPARTAMENTO","label":"Departamento","type":"select","required":True,"options":["LIMA","AREQUIPA","CUSCO","LA LIBERTAD","PIURA","ANCASH"]},
        {"name":"PROVINCIA","label":"Provincia","type":"text","required":True,"transform":"uppercase"},
        {"name":"DISTRITO","label":"Distrito","type":"text","required":True,"transform":"uppercase"},
        {"name":"DIRECCION","label":"Dirección","type":"textarea","required":True,"transform":"uppercase"}
    ]},
    {"group":"Estado civil","items":[
        {"name":"ESTADO_CIVIL","label":"Estado Civil","type":"select","required":True,"options":["SOLTERO(A)","CASADO(A)","DIVORCIADO(A)","VIUDO(A)","CONVIVIENTE"]}
    ]},
    {"group":"Poderes","items":[
        {"name":"PODER_TIPO","label":"Tipo de Poder","type":"select","required":True,"options":["AMPLIO","ESPECIAL","BANCARIO","VEHICULAR"]},
        {"name":"APODERADO_NOMBRE","label":"Nombre Apoderado","type":"text","required":True,"transform":"uppercase"},
        {"name":"APODERADO_DNI","label":"DNI Apoderado","type":"text","required":True,"mask":{"regex":"^\\d{8}$","hint":"8 dígitos"}},
        {"name":"ALCANCE","label":"Alcance","type":"textarea","required":False,"placeholder":"Facultades específicas..."}
    ]}
]
@router.get("")
async def list_presets(): return {"presets": PRESETS}

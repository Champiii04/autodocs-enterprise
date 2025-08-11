from pydantic import BaseModel, Field, EmailStr, ValidationError, constr
def model_from_schema(schema: dict) -> type[BaseModel]:
    fields = {}
    for f in schema.get("fields", []):
        t = (str(f.get("type","text"))).lower()
        ann = str
        if t == "email": ann = EmailStr
        elif t == "number": ann = float
        elif t == "date": ann = str
        if f.get("mask") and f["mask"].get("regex"):
            ann = constr(pattern=f["mask"]["regex"])
        default = ... if f.get("required") else None
        fields[f["name"]] = (ann, Field(default=default))
    return type("DynamicForm", (BaseModel,), fields)

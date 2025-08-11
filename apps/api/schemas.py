from pydantic import BaseModel, Field
from typing import Any, Literal
class GenerateRequest(BaseModel): data: dict[str, Any]; options: dict[str, Any] = Field(default_factory=dict)
class JobOut(BaseModel):
    id: int; status: str
    output_docx_url: str | None = None; output_pdf_url: str | None = None
    output_odt_url: str | None = None; output_html_url: str | None = None
class FieldDef(BaseModel): name: str; label: str; type: Literal['text','number','date','select','textarea','email'] = 'text'; required: bool = False; options: list[str] = []; mask: dict | None = None; transform: str | None = None; show_if: dict | None = None
class FormCreate(BaseModel): template_key: str; name: str; fields: list[FieldDef]

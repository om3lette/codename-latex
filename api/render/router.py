from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from api.render.services import render_latex
from api.render.schemas import RenderResult, RenderStatus

from api.render.schemas import LatexRenderRequest

latex_router: APIRouter = APIRouter()

@latex_router.post("/render")
def render_document(data: LatexRenderRequest):
    if data.document == "":
        return HTTPException(status_code=400, detail="Document was not provided")
    response: RenderResult = render_latex(data.document)
    if response.status == RenderStatus.RENDER_ERROR:
        return HTTPException(status_code=400, detail=response.latex_error)
    if response.status == RenderStatus.UNKNOWN_ERROR:
        return HTTPException(status_code=500, detail="Unable to render document. Please try later")
    return FileResponse(response.output_path)
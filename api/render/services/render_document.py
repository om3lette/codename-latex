import subprocess
from pathlib import Path
from uuid import uuid4
from typing import Self

from api.render.constants import BASE_DOCUMENT, DOCUMENTS_SAVE_PATH, LATEX_DOCUMENT_NAME, PDF_DOCUMENT_NAME, CROPPED_PDF_DOCUMENT_NAME, GENERATED_IMAGE_PREFIX, FINAL_IMAGE_NAME
from api.render.schemas import RenderResult, RenderStatus

class LatexDocument:
    def __init__(self, working_dir: Path):
        self.working_dir: Path = working_dir

    def render(self, output_format: str) -> Self:
        subprocess.run(
            ["latexmk", f"-{output_format}", "-interaction=nonstopmode", LATEX_DOCUMENT_NAME],
            check=True,
            cwd=self.working_dir
        )
        return self

    def crop(self, margins: tuple[int, int, int, int]) -> Self:
        subprocess.run(
            ["pdfcrop", "--margins", " ".join(map(str, margins)), PDF_DOCUMENT_NAME, CROPPED_PDF_DOCUMENT_NAME],
            check=True,
            cwd=self.working_dir
        )
        return self

    def to_png(self, dpi: int, start_from_page: int = 1) -> Self:
        subprocess.run(
            ["pdftoppm", "-png", "-f", str(start_from_page), "-r", str(dpi), CROPPED_PDF_DOCUMENT_NAME, GENERATED_IMAGE_PREFIX],
            check=True,
            cwd=self.working_dir
        )
        return self

    def combine(self) -> Self:
        subprocess.run(
            ["convert", f"{GENERATED_IMAGE_PREFIX}-*.png", "-append", FINAL_IMAGE_NAME],
            check=True,
            cwd=self.working_dir
        )
        return self

def render_latex(tex_source: str, output_format: str = "pdf") -> RenderResult:
    request_id: str = uuid4().hex
    output_dir: Path = DOCUMENTS_SAVE_PATH.joinpath(request_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    latex_document: LatexDocument = LatexDocument(output_dir)

    tex_file: Path = output_dir.joinpath(LATEX_DOCUMENT_NAME)
    output_file: Path = output_dir.joinpath(FINAL_IMAGE_NAME)

    with tex_file.open("w") as f:
        f.write(BASE_DOCUMENT.replace("_body_", tex_source))

    try:
        latex_document.render(output_format).crop((30, 30, 30, 30)).to_png(600, 1).combine()
    except subprocess.CalledProcessError as e:
        return RenderResult(status=RenderStatus.RENDER_ERROR, latex_error=str(e))

    if output_file.exists():
        return RenderResult(status=RenderStatus.OK, output_path=output_file)
    return RenderResult(status=RenderStatus.UNKNOWN_ERROR)


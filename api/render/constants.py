from pathlib import Path

PROJECT_ROOT_PATH: Path = Path(__file__).resolve().parents[2]
DOCUMENTS_SAVE_PATH: Path = PROJECT_ROOT_PATH.joinpath("renders")

LATEX_DOCUMENT_NAME: str = "document.tex"
PDF_DOCUMENT_NAME: str = "document.pdf"
CROPPED_PDF_DOCUMENT_NAME: str = "cropped.pdf"
GENERATED_IMAGE_PREFIX: str = "cropped-image"
FINAL_IMAGE_NAME: str = "result.png"

BASE_DOCUMENT: str = r"""
    \documentclass[20pt]{extarticle}
    \usepackage[english, russian]{babel}
    \usepackage{amssymb}
    \usepackage{mathtools}
    \pagestyle{empty}
    \title{Document by InlineTexBot}
    \begin{document}
        _body_
    \end{document}
"""

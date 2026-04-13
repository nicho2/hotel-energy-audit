from __future__ import annotations

from html.parser import HTMLParser
from textwrap import wrap
from typing import Any


PDF_RENDERER_VERSION = "html_text_pdf_v1"


class HtmlReportPdfRenderer:
    def render(
        self,
        *,
        html: str,
        title: str,
        branding: dict[str, Any],
        report_type: str,
    ) -> bytes:
        lines = _HtmlTextExtractor().extract(html)
        if not lines:
            lines = [title]
        accent = _hex_to_rgb(str(branding.get("accent_color") or "#0f766e"))
        pages = _paginate(lines)
        return _build_pdf(
            pages=pages,
            title=title,
            logo_text=str(branding.get("logo_text") or "HEA"),
            company_name=str(branding.get("company_name") or "Hotel Energy Audit"),
            report_type=report_type,
            accent_rgb=accent,
        )


class _HtmlTextExtractor(HTMLParser):
    BLOCK_TAGS = {"h1", "h2", "h3", "p", "li", "tr", "div", "section", "article"}
    SKIP_TAGS = {"style", "script", "head"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._lines: list[str] = []
        self._current: list[str] = []
        self._skip_depth = 0
        self._prefix_stack: list[str] = []

    def extract(self, html: str) -> list[str]:
        self.feed(html)
        self.close()
        self._flush()
        return [line for line in self._lines if line.strip()]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
            return
        if tag in self.BLOCK_TAGS:
            self._flush()
        if tag == "li":
            self._prefix_stack.append("- ")
        if tag in {"td", "th"}:
            self._append("  ")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
            return
        if tag == "li" and self._prefix_stack:
            self._prefix_stack.pop()
        if tag in self.BLOCK_TAGS or tag in {"td", "th"}:
            self._flush()

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = " ".join(data.split())
        if text:
            self._append(text)

    def _append(self, text: str) -> None:
        if not self._current and self._prefix_stack:
            self._current.append(self._prefix_stack[-1])
        self._current.append(text)

    def _flush(self) -> None:
        text = " ".join(part.strip() for part in self._current if part.strip()).strip()
        if text and (not self._lines or self._lines[-1] != text):
            self._lines.append(text)
        self._current = []


def _paginate(lines: list[str], *, max_lines_per_page: int = 38, width: int = 92) -> list[list[str]]:
    pages: list[list[str]] = []
    page: list[str] = []
    for line in lines:
        wrapped = wrap(line, width=width, break_long_words=False, replace_whitespace=False) or [""]
        for wrapped_line in wrapped:
            if len(page) >= max_lines_per_page:
                pages.append(page)
                page = []
            page.append(wrapped_line)
    if page:
        pages.append(page)
    return pages or [[lines[0] if lines else "Report"]]


def _build_pdf(
    *,
    pages: list[list[str]],
    title: str,
    logo_text: str,
    company_name: str,
    report_type: str,
    accent_rgb: tuple[float, float, float],
) -> bytes:
    objects: list[bytes] = []
    catalog_id = 1
    pages_id = 2
    font_regular_id = 3
    font_bold_id = 4
    next_id = 5
    page_ids: list[int] = []
    content_ids: list[int] = []

    for _page in pages:
        page_ids.append(next_id)
        content_ids.append(next_id + 1)
        next_id += 2

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("latin-1"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    for index, (page_id, content_id, lines) in enumerate(zip(page_ids, content_ids, pages, strict=True), start=1):
        stream = _page_stream(
            lines=lines,
            page_number=index,
            page_count=len(pages),
            title=title,
            logo_text=logo_text,
            company_name=company_name,
            report_type=report_type,
            accent_rgb=accent_rgb,
        )
        objects.append(
            (
                f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 595 842] "
                f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >> >> "
                f"/Contents {content_id} 0 R >>"
            ).encode("latin-1")
        )
        objects.append(f"<< /Length {len(stream)} >> stream\n".encode("latin-1") + stream + b"\nendstream")

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for object_id, body in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{object_id} 0 obj\n".encode("latin-1"))
        pdf.extend(body)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        (
            "trailer\n"
            f"<< /Size {len(offsets)} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_offset}\n"
            "%%EOF\n"
        ).encode("latin-1")
    )
    return bytes(pdf)


def _page_stream(
    *,
    lines: list[str],
    page_number: int,
    page_count: int,
    title: str,
    logo_text: str,
    company_name: str,
    report_type: str,
    accent_rgb: tuple[float, float, float],
) -> bytes:
    r, g, b = accent_rgb
    commands = [
        "q",
        f"{r:.3f} {g:.3f} {b:.3f} rg",
        "0 802 595 40 re f",
        "Q",
        "BT",
        "/F2 14 Tf",
        "36 816 Td",
        f"({_escape_pdf_text(logo_text[:16])}) Tj",
        "/F2 10 Tf",
        "430 0 Td",
        f"({_escape_pdf_text(report_type.title())}) Tj",
        "ET",
        "BT",
        "/F2 16 Tf",
        "36 776 Td",
        f"({_escape_pdf_text(title)}) Tj",
        "/F1 9 Tf",
        "0 -16 Td",
        f"({_escape_pdf_text(company_name)}) Tj",
        "ET",
        "BT",
        "/F1 10 Tf",
        "36 724 Td",
        "13 TL",
    ]
    for line in lines:
        commands.append(f"({_escape_pdf_text(line)}) Tj")
        commands.append("T*")
    commands.extend(
        [
            "ET",
            "BT",
            "/F1 8 Tf",
            "36 28 Td",
            f"({_escape_pdf_text(f'Page {page_number}/{page_count} - Generated from report HTML')}) Tj",
            "ET",
        ]
    )
    return "\n".join(commands).encode("latin-1", errors="replace")


def _escape_pdf_text(value: str) -> str:
    safe = value.encode("latin-1", errors="replace").decode("latin-1")
    return safe.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _hex_to_rgb(value: str) -> tuple[float, float, float]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        return (0.06, 0.46, 0.43)
    try:
        return (int(value[0:2], 16) / 255, int(value[2:4], 16) / 255, int(value[4:6], 16) / 255)
    except ValueError:
        return (0.06, 0.46, 0.43)

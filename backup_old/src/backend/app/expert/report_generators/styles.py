from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus.tables import TableStyle


class Styles:
    """
    Static class containing styles used in the report generator.
    """

    WARNING_STYLE = ParagraphStyle("warningstyle", backColor=colors.orange)
    ERROR_STYLE = ParagraphStyle("warningstyle", backColor=colors.orangered)
    LEGEND_HEADER_STYLE = ParagraphStyle(
        "legendtitle",
        fontName="Helvetica-Bold",
        leftIndent=-12 * mm,
        rightIndent=0,
        firstLineIndent=0,
        fontSize=12,
        parent=getSampleStyleSheet()["Heading2"],
        alignment=0,
        spaceAfter=14,
    )
    LEGEND_TEXT_STYLE = ParagraphStyle(
        "legendtext", parent=getSampleStyleSheet()["Normal"], fontSize=8
    )
    TABLE_HEADER_STYLE = ParagraphStyle(
        "tableheadertitle",
        fontName="Helvetica-Bold",
        leftIndent=-12 * mm,
        rightIndent=0,
        firstLineIndent=0,
        fontSize=16,
        parent=getSampleStyleSheet()["Heading2"],
        alignment=0,
        spaceAfter=14,
    )
    TABLE_STYLE = TableStyle(
        [
            ("BOX", (0, 1), (-1, -1), 0.25, colors.black),
            ("LINEABOVE", (0, 1), (-1, -1), 0.25, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    )
    HEADING_ONE = ParagraphStyle(
        "headingone",
        fontName="Helvetica-Bold",
        leftIndent=-12 * mm,
        rightIndent=0,
        firstLineIndent=0,
        parent=getSampleStyleSheet()["Heading1"],
        alignment=0,
        spaceAfter=25,
    )
    HEADING_TWO = ParagraphStyle(
        "headingtwo",
        fontName="Helvetica-Bold",
        leftIndent=-12 * mm,
        rightIndent=0,
        firstLineIndent=0,
        parent=getSampleStyleSheet()["Heading2"],
        alignment=0,
        spaceAfter=15,
        spaceBefore=30,
    )
    HEADING_THREE = ParagraphStyle(
        "headingthree",
        fontName="Helvetica-Bold",
        leftIndent=-12 * mm,
        rightIndent=0,
        firstLineIndent=0,
        parent=getSampleStyleSheet()["Heading3"],
        alignment=0,
        spaceAfter=12,
        spaceBefore=20,
    )
    TEXTBLOCK = ParagraphStyle(
        "textblock",
        leftIndent=-12 * mm,
        rightIndent=0,
        firstLineIndent=0,
        parent=ParagraphStyle(name="paragraphImplicitDefaultStyle"),
        alignment=0,
        spaceAfter=14,
    )
    TOELICHTING = ParagraphStyle(
        "toelichting",
        leftIndent=-12 * mm,
        rightIndent=0,
        firstLineIndent=0,
        parent=ParagraphStyle(name="paragraphImplicitDefaultStyle"),
        alignment=0,
        spaceAfter=1,
    )

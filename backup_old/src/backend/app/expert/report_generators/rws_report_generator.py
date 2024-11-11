import os
from copy import deepcopy
from functools import reduce

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Image, PageBreak

from app.enums import Importance
from app.expert.report_generators.batch_report_base import BatchReporterBase
from app.expert.report_generators.styles import Styles


class RwsReportGenerator(BatchReporterBase):
    dirname = os.path.dirname(__file__)
    headers = ["", "Code", "Bevinding"]
    title = "Kwaliteitsrapport"

    # Constant styles
    warning_style = Styles.WARNING_STYLE
    error_style = Styles.ERROR_STYLE
    legend_header_style = Styles.LEGEND_HEADER_STYLE
    legend_text_style = Styles.LEGEND_TEXT_STYLE
    table_style = deepcopy(Styles.TABLE_STYLE)
    introduction = "Rapportage van kwaliteitsbevindingen uit een automatisch uitgevoerde controle, aan de hand van kwaliteitsregels van Rijkswaterstaat, toegepast op een levering met brondocumenten die is aangeleverd bij het Bronhouderportaal voor de BRO."
    title_style = Styles.HEADING_ONE
    heading_two = Styles.HEADING_TWO
    heading_three = Styles.HEADING_THREE
    text_block = Styles.TEXTBLOCK

    def __init__(self, batch_id, data):
        self.batch_id = batch_id
        self.data = data
        self.rules = self.__discover_applied_rules()
        super().__init__(batch_id, data)

    def __determine_followup_action(self, warnings: int, errors: int):
        """
        Based on the amount of warnings and errors, generate the followup action for in the report.

        Returns: String with corresponding followup action.
        """
        if errors > 0:
            return "Afkeuren"
        elif warnings > 0:
            return "Bespreken"
        return "Accorderen"

    def __translate_weight_to_dutch(self, weight):
        """
        Translates the weight values as defined in the Enum from the expert into a dutch human readable string.

        Returns: translated string.
        """
        if weight == "INFO":
            return "Info"
        elif weight == "WARNING":
            return "Waarschuwing"
        elif weight == "ERROR":
            return "Fout"
        return "Onbekend"

    def __discover_applied_rules(self):
        """
        Crawls the findings available in the data object and creates a set of applied rules on this batch.
        Adds the found rules to the rules property.

        Returns: None
        """
        rules = {}
        if len(self.data) > 0:
            for row in reversed(self.data):
                for finding in row["findings"]:
                    if finding.Rule.importance < 2 or not finding.Rule.enabled:
                        continue
                    if f"{finding.Rule.object_type}-{finding.Rule.id}" not in rules:
                        rules[f"{finding.Rule.object_type}-{finding.Rule.id}"] = {
                            "gewicht": self.__translate_weight_to_dutch(
                                Importance(finding.Rule.importance).name
                            ),
                            "uitleg": finding.Rule.explanation,
                            "occurences": 0,
                            "violated_files": [],
                        }
                    rules[f"{finding.Rule.object_type}-{finding.Rule.id}"][
                        "occurences"
                    ] += 1
                    if not finding.Finding.result:
                        rules[f"{finding.Rule.object_type}-{finding.Rule.id}"][
                            "violated_files"
                        ].append(finding.Finding.filename)
        return rules

    def __count_documents(self):
        """
        Crawls the data and returns the amount of documents checked in this batch.

        Returns: Document count
        """
        document_count = 1
        cur_file = self.data[0]["filename"]
        for document in self.data:
            if not cur_file == document["filename"]:
                cur_file = document["filename"]
                document_count += 1
        return document_count

    def __create_summary_table(self, contentBuilder):
        """
        Based on the discovered rules and results, create a table summarizing the reports amount of applied rules and violations.

        Returns: None
        """
        document_count = self.__count_documents()
        warnings = len(
            set(
                reduce(
                    lambda xs, ys: xs + ys,
                    [
                        rule["violated_files"]
                        for rule in self.rules.values()
                        if rule["gewicht"] == "Waarschuwing"
                    ],
                    [],
                )
            )
        )
        errors = len(
            set(
                reduce(
                    lambda xs, ys: xs + ys,
                    [
                        rule["violated_files"]
                        for rule in self.rules.values()
                        if rule["gewicht"] == "Fout"
                    ],
                    [],
                )
            )
        )
        table_style = TableStyle(
            [
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("FONTSIZE", (2, 0), (2, -1), 6),
                ("LEFTPADDING", (2, 0), (2, -1), 0),
                ("TOPPADDING", (2, 0), (2, -1), 1),
                ("BOTTOMPADDING", (2, 0), (2, -1), 0),
            ]
        )
        tabledata = [
            ["Leveringsnummer", self.batch_id, ""],
            ["Projectnummer", self.data[0]["project_nr"], ""],
            ["Rapportagedatum", self.data[0]["timestamp"].strftime("%Y.%m.%d"), ""],
            ["Aantal toegepaste kwaliteitsregels", len(self.rules), ""],
            ["Aantal gecontroleerde brondocumenten", document_count, ""],
            [
                "Aantal brondocumenten met waarschuwingen",
                f"{warnings}",
                f"({int(warnings/document_count*100)}%)",
            ],
            [
                "Aantal brondocumenten met foutmeldingen",
                f"{errors}",
                f"({int(errors/document_count*100)}%)",
            ],
            [
                "Geadviseerde vervolgactie",
                self.__determine_followup_action(warnings, errors),
                "",
            ],
        ]
        table = Table(tabledata, colWidths=[90 * mm, 50 * mm, 39 * mm])
        table.setStyle(table_style)
        contentBuilder(table)
        contentBuilder(Spacer(10, 10))
        contentBuilder(
            Paragraph(
                "<b>Toelichting</b>",
                style=Styles.TOELICHTING,
            )
        )
        contentBuilder(
            Paragraph(
                "Het leveringsnummer is het nummer voor deze levering dat is toegekend door het Bronhouderportaal. De geadviseerde vervolgactie is het advies voor de Technisch Manager van Rijkswaterstaat.",
                style=self.text_block,
            )
        )

    def __create_management_summary(self, contentBuilder):
        """
        Based on the discovered rules and results, create a table summarizing the report by showing each rule and their passing percentage.

        Returns: None
        """
        table_style = TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (3, 0), (4, -1), "RIGHT"),
                ("BOX", (0, 1), (-1, -1), 0.25, colors.black),
                ("LINEABOVE", (0, 1), (-1, -1), 0.25, colors.black),
                ("RIGHTPADDING", (3, 0), (3, 0), -22),
                ("FONTSIZE", (4, 1), (4, -1), 6),
                ("LEFTPADDING", (4, 1), (4, -1), -5),
                ("TOPPADDING", (4, 1), (4, -1), 5),
                ("BOTTOMPADDING", (4, 1), (4, -1), 0),
            ]
        )
        tabledata = [
            [
                "",
                "Code",
                "Omschrijving kwaliteitsregel",
                "Aantal brondocumenten met bevindingen",
            ]
        ]
        data = []
        row = 1
        for key, rule in self.rules.items():
            if len(rule["violated_files"]) <= 0:
                continue
            data.append(
                [
                    Image(
                        filename=os.path.join(
                            self.dirname,
                            "images",
                            (
                                "warning-white.png"
                                if rule["gewicht"] == "Waarschuwing"
                                else "error-white.png"
                            ),
                        ),
                        width=10 * mm,
                        height=10 * mm,
                    ),
                    key,
                    Paragraph(rule["uitleg"]),
                    str(len(rule["violated_files"])),
                    "("
                    + str(int(len(rule["violated_files"]) / rule["occurences"] * 100))
                    + "%)",
                ]
            )
            self.colour_row(table_style, rule["gewicht"], row)
            row += 1
        tabledata.extend(data)
        table = Table(
            tabledata, colWidths=[14 * mm, 20 * mm, 115 * mm, 22 * mm, 8 * mm]
        )
        table.setStyle(table_style)
        contentBuilder(
            Paragraph(
                "Kwaliteitsbevindingen",
                style=self.heading_three,
            )
        )
        self.build_legend(contentBuilder)
        contentBuilder(table)

    def build_legend(self, contentBuilder):
        """
        Writes the legend to the document.
        """
        table_style = TableStyle(
            [
                ("BOX", (0, 0), (1, 1), 0.25, colors.black),
                ("LINEABOVE", (0, 0), (1, 1), 0.25, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
        table_style.add("BACKGROUND", (0, 0), (0, 0), colors.orange)
        table_style.add("BACKGROUND", (0, 1), (0, 1), colors.orangered)
        legend_data = [
            [
                Image(
                    filename=os.path.join(self.dirname, "images", "warning-white.png"),
                    width=5 * mm,
                    height=5 * mm,
                ),
                Paragraph("Waarschuwing", style=self.legend_text_style),
                Paragraph(""),
            ],
            [
                Image(
                    filename=os.path.join(self.dirname, "images", "error-white.png"),
                    width=5 * mm,
                    height=5 * mm,
                ),
                Paragraph("Fout", style=self.legend_text_style),
                Paragraph(""),
            ],
        ]
        contentBuilder(Paragraph("<b>Legenda</b>", style=Styles.TOELICHTING))
        table = Table(legend_data, colWidths=[9 * mm, 30 * mm, 140 * mm])
        table.setStyle(table_style)
        contentBuilder(table)
        contentBuilder(Spacer(10, 10))

    def add_row(self, tabledata, filename, finding):
        """
        Adds a row to the current table for the given finding.

        Returns: None
        """
        tabledata.append(
            [
                Image(
                    filename=os.path.join(
                        self.dirname,
                        "images",
                        (
                            "warning-white.png"
                            if finding.Rule.importance == 2
                            else "error-white.png"
                        ),
                    ),
                    width=10 * mm,
                    height=10 * mm,
                ),
                Paragraph(f"{finding.Rule.object_type}-{finding.Rule.id}"),
                Paragraph(
                    finding.Finding.feedbackMessage,
                    getSampleStyleSheet()["Normal"],
                ),
            ]
        )

    def colour_row(self, table_style, importance, row_index):
        """
        Colours a row based on the importance level of the finding.
        Warning = Orange
        Error = Red

        Returns: None
        """
        table_style.add("BOX", (0, row_index), (0, row_index), 0.25, colors.black)
        if importance == "Waarschuwing":
            table_style.add("BACKGROUND", (0, row_index), (0, row_index), colors.orange)
        elif importance == "Fout":
            table_style.add(
                "BACKGROUND", (0, row_index), (0, row_index), colors.orangered
            )

    def build_table_from_data(
        self, contentBuilder, tabledata, table_style, file_name
    ) -> None:
        """
        Builds a table for the final report pdf based on given tabledata and table_style.

        Returns: None.
        """
        if len(tabledata) > 0:
            contentBuilder(
                Paragraph(f"Brondocument {file_name}", style=self.heading_three)
            )
            table = Table(tabledata, colWidths=[14 * mm, 20 * mm, 145 * mm])
            table.setStyle(table_style)
            contentBuilder(table)
            contentBuilder(Spacer(10, 10))

    def getContent(self, contentBuilder):
        """
        Builds a full report using the data defined in the Report Generator object.

        Returns: None.
        """
        contentBuilder(Paragraph(self.title, style=self.title_style))
        contentBuilder(Paragraph(self.introduction, style=self.text_block))
        contentBuilder(Paragraph("Managementsamenvatting", style=self.heading_two))
        self.__create_summary_table(contentBuilder)
        self.__create_management_summary(contentBuilder)
        contentBuilder(PageBreak())
        contentBuilder(
            Paragraph("Bevindingen per brondocument", style=self.heading_two)
        )
        self.build_legend(contentBuilder)
        tabledata = [self.headers]
        rowIndex = 1
        table_style = deepcopy(Styles.TABLE_STYLE)
        cur_file = self.data[0]["filename"]
        for document in self.data:
            if not cur_file == document["filename"]:
                self.build_table_from_data(
                    contentBuilder, tabledata, table_style, cur_file
                )
                cur_file = document["filename"]
                rowIndex = 1
                tabledata = [self.headers]
            for finding in [
                f
                for f in document["findings"]
                if not f.Finding.result and f.Rule.importance > 1
            ]:
                self.add_row(tabledata, document["filename"], finding)
                self.colour_row(
                    table_style,
                    self.__translate_weight_to_dutch(
                        Importance(finding.Rule.importance).name
                    ),
                    rowIndex,
                )
                rowIndex += 1
        self.build_table_from_data(contentBuilder, tabledata, table_style, cur_file)

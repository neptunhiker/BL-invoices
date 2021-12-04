from abc import ABC, abstractmethod
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image, Paragraph, Table

import helpers

class PDFReport(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_header(cls):
        pass

    @abstractmethod
    def create_body(cls):
        pass

    @abstractmethod
    def create_footer(cls):
        pass


class PDFInvoice(PDFReport):

    def __init__(self, participant_name, participant_title, participant_id, avgs_coupon_nr,
                 invoice_nr, time_period_start, time_period_end, nr_of_training_lessons, cost_per_training_lesson,
                 training_name, creation_date=datetime.date.today()):
        self.creation_date = creation_date
        self.date_for_title = creation_date.strftime('%Y-%m-%d')
        self.date_for_invoice = helpers.format_to_german_date(self.creation_date)
        self.payment_horizon
        self.latest_payment_date = self.creation_date + datetime.timedelta(days=self.payment_horizon)
        name = f"{self.date_for_title} BeginnerLuft Rechnung {participant_name}"
        super().__init__()
        self.participant_name = participant_name
        self.participant_title = participant_title
        self.participant_id = participant_id
        self.avgs_coupon_nr = avgs_coupon_nr
        self.invoice_nr = invoice_nr
        self.time_period_start = time_period_start
        self.time_period_end = time_period_end
        self.training_name = training_name
        self.nr_of_training_lessons = nr_of_training_lessons
        self.cost_per_training_lesson = cost_per_training_lesson
        self.total_cost = round(self.nr_of_training_lessons * self.cost_per_training_lesson, 2)


        self.iban = "DE28 4306 0967 1014 6919"
        self.bic = "GENODEM1GLS"

        self.width = A4[0]
        self.height = A4[1]

        # Create the pdf
        pdf = canvas.Canvas(f"{name}.pdf", pagesize=A4)
        pdf.setTitle(name)

        # Defining the size-structure of the report
        self.col_widths = [0.1 * self.width, 0.8 * self.width, 0.1 * self.width]
        self.row_heights = [0.1 * self.height, 0.8 * self.height, 0.1 * self.height]

        # Creating the main table of the report
        main_table = Table([
            ["", self.create_header(), ""],
            ["", self.create_body(), ""],
            ["", self.create_footer(), ""]
            ],
            colWidths=self.col_widths,
            rowHeights=self.row_heights
        )

        # Style of main table
        main_table.setStyle([
            ('GRID', (0, 0), (-1, -1), 1, "red"),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ("LINEBELOW", (1, 1), (1, 1), 1, "grey"),
        ])

        main_table.wrapOn(pdf, 0, 0)
        main_table.drawOn(pdf, 0, 0)

        pdf.showPage()
        pdf.save()

    def create_header(self):
        """Create a header for the report"""

        img_path = "resources/beginnerluft.png"
        img_width = self.col_widths[1] * 0.3
        img_height = self.row_heights[0] * 0.5
        img = Image(filename=img_path, width=img_width, height=img_height, kind="proportional")

        res = Table([
            [img],
            ["BeginnerLuft gGmbH - Bandelstr. 1 - 10559 Berlin"]
        ],
            colWidths=self.col_widths[1],
            rowHeights=self.row_heights[0] / 2
        )

        res.setStyle([
            # ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (0, 0), -20),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("TEXTCOLOR", (0, 0), (-1, -1), "grey"),
        ])

        return res

    def create_body(self):

        height_list = [0.15, 0.1, 0.15, 0.2, 0.15, 0.25]
        height_list = [height * self.row_heights[1] for height in height_list]

        res = Table([
            [self.date_for_invoice],
            [self._body_create_intro_text()],
            [self._body_create_invoice_details()],
            [],
            [],
            [],
            ],
            rowHeights=height_list
        )

        res.setStyle([
            ("GRID", (0, 0), (-1, -1), 1, "red"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0)
        ])

        return res

    def _body_create_intro_text(self):
        """Create the introductory text for the invoice"""
        if self.participant_title == "Herr":
            title = "Herrn"
        elif self.participant_title == "Frau":
            title = "Frau"
        else:
            title = ""

        para_list = []

        para_01 = Paragraph(f"""
        Sehr geehrte Damen und Herren,<br/><br/>
        
        hiermit stellen wir Ihnen unsere Leistungen im Rahmen der Maßname "{self.training_name}"
        für {title} {self.participant_name} (Kundennummer {self.participant_id}) in Rechnung:
        """)

        para_list.append(para_01)
        return para_list

    def _body_create_invoice_details(self):
        """Create the details for the invoice"""

        if self.time_period_start.year == self.time_period_end.year:
            start_date = self.time_period_start.strftime("%d.%m.")
        else:
            start_date = self.time_period_start.strftime("%d.%m.%Y")
        end_date = self.time_period_end.strftime("%d.%m.%Y")

        # Format into German number formatting
        total_costs_formatted = str('{:0,.2f}'.format(self.total_cost)).\
            replace(".", "X").replace(",", ".").replace("X", ",")
        costs_per_training_formatted = str('{:0,.2f}'.format(self.cost_per_training_lesson).replace(".", ","))

        res_table = Table([
            [f"Rechnungsnummer: {self.invoice_nr}"],
            [f"Zeitraum: {start_date} bis {end_date}"],
            [f"{self.nr_of_training_lessons} Unterrichtseinheiten á 45 Minuten"],
            [f"Kosten pro Unterrichtseinheit: {costs_per_training_formatted} €"],
            [f"Rechnungsbetrag: {total_costs_formatted} €"],
            ],
        )

        return res_table

    def _body_create_wire_instructions(self):
        """Create the wire instructions for transferring the money to BeginnerLuft"""

        para_list = []

        para_01 = Paragraph(f"""
            Bitte überweisen Sie den Rechnungsbetrag innerhalb der nächsten 14 Tage, spätestens bis zum 19.11.2021auf folgendes Konto:
            BeginnerLuft gGmbH

                """)

        para_list.append(para_01)
        return para_list

    def create_footer(self):
        """Create a footer for the report"""

        width_list = [
            0.22 * self.col_widths[1],
            0.22 * self.col_widths[1],
            0.22 * self.col_widths[1],
            0.34 * self.col_widths[1],
        ]

        res = Table([
            ["BeginnerLuft gGmbH", "030 / 398 768 02", "Amtsgericht", "Bankinstitut: GLS Bank"],
            ["Bandelstr. 1", "www.beginnerluft.de", "Berlin Charlottenburg", f"IBAN: {self.iban}"],
            ["10559 Berlin", "info@beginnerluft.de", "HR209894 B", f"BIC: {self.bic}"]
        ],
            # rowHeights=self.row_heights[2] / 3,
            colWidths=width_list
        )

        color = "#FFFF00"
        # color = colors.darkgrey
        res.setStyle([
            # ("GRID", (0, 0), (-1, -1), 1, "red"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, -1), (-1, -1), 20),
            # ("BACKGROUND", (0, 0), (-1, -1), color),
            # ("TEXTCOLOR", (0, 0), (-1, -1), "black"),
            # ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # horizontal
            # ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ])
        return res



if __name__ == '__main__':
    pdf = PDFInvoice(participant_name="Samer Kassem",
                     participant_title="Herr",
                     participant_id="955D551295",
                     invoice_nr="202110-74",
                     time_period_start=datetime.date(year=2021, month=8, day=9),
                     time_period_end=datetime.date(year=2021, month=10, day=31),
                     nr_of_training_lessons=48,
                     cost_per_training_lesson=64.81,
                     training_name="Individuelles Berufscoaching",
                     avgs_coupon_nr="sdlfjas-34")
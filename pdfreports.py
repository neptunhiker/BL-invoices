from abc import ABC, abstractmethod
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image, Paragraph, Table

from jobcenter import Jobcenter
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
                 training_name, signer, jobcenter, payment_horizon=14, creation_date=datetime.date.today()):
        self.creation_date = creation_date
        self.date_for_title = creation_date.strftime('%Y-%m-%d')
        self.date_for_invoice = helpers.format_to_german_date(self.creation_date)
        self.payment_horizon = payment_horizon
        self.latest_payment_date = helpers.format_to_german_date(self.creation_date +
                                                                 datetime.timedelta(days=self.payment_horizon))
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
        self.signer = signer
        self.jobcenter = jobcenter
        self.iban = "DE28 4306 0967 1014 6919"
        self.bic = "GENODEM1GLS"
        self.bl_name = "BeginnerLuft gGmbH"
        self.bl_street = "Bandelstr. 1"
        self.bl_zip_city = "10559 Berlin"

        self.width = A4[0]
        self.height = A4[1]

        # Create the pdf
        pdf = canvas.Canvas(f"{name}.pdf", pagesize=A4)
        pdf.setTitle(name)

        # Defining the size-structure of the report
        self.col_widths = [0.1 * self.width, 0.8 * self.width, 0.1 * self.width]
        self.row_heights = [0.15 * self.height, 0.75 * self.height, 0.1 * self.height]

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
            # ('GRID', (0, 0), (-1, -1), 1, "red"),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ("LINEBELOW", (1, 0), (1, 0), 1, "grey"),
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
            [f"{self.bl_name} - {self.bl_street} - {self.bl_zip_city}"]
        ],
            colWidths=self.col_widths[1],
            rowHeights=self.row_heights[0] / 2
        )

        res.setStyle([
            # ("VALIGN", (0, -1), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (0, 0), -40),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("TEXTCOLOR", (0, 0), (-1, -1), "grey"),
        ])

        return res

    def create_body(self):

        height_list = [0.15, 0.1, 0.05, 0.05, 0.45, 0.2]
        height_list = [height * self.row_heights[1] for height in height_list]

        res = Table([
            [self._body_create_address_for_recipient()],
            [self._body_create_address_bl()],
            [self._body_create_date_and_invoice_nr()],
            ["RECHNUNG"],
            [self._body_create_intro_text()],
            [self._body_create_greetings()],
            ],
            rowHeights=height_list
        )

        res.setStyle([
            # ("GRID", (0, 0), (-1, -1), 1, "red"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("FONTSIZE", (0, 3), (-1, 3), 12),
            ("BOTTOMPADDING", (0, 3), (-1, 3), 12),
        ])

        return res

    def _body_create_address_for_recipient(self):
        """Create the adress field for the job center"""

        para_list = []
        para_01 = Paragraph(f"""
                An das <br/>
                <b>{self.jobcenter.name}</b><br/>
                <b>{self.jobcenter.street} {self.jobcenter.street_nr}</b><br/>
                <b>{self.jobcenter.zip_code} {self.jobcenter.city}</b>
                """)
        para_list.append(para_01)
        return para_list

    def _body_create_address_bl(self):
        """Create the address field for BeginnerLuft"""

        para_list = []
        para_01_style = ParagraphStyle("para_01_style")
        para_01_style.alignment = 0  # 2 = alignment RIGHT
        para_01 = Paragraph(f"""
                {self.bl_name}<br/>
                {self.bl_street}<br/>
                {self.bl_zip_city}
                """, para_01_style)
        para_list.append(para_01)
        return para_list


    def _body_create_date_and_invoice_nr(self):
        """Create date and invoice nr"""

        para_list = []
        para_01_style = ParagraphStyle("para_01_style")
        para_01_style.alignment = 2  # 2 = alignment RIGHT
        para_01 = Paragraph(f"""
                {self.date_for_invoice}<br/>
                """, para_01_style)
        para_list.append(para_01)
        return para_list

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
        für {title} {self.participant_name} (Kundennummer {self.participant_id}) in Rechnung:<br/><br/><br/>
        """)

        if self.time_period_start.year == self.time_period_end.year:
            start_date = self.time_period_start.strftime("%d.%m.")
        else:
            start_date = self.time_period_start.strftime("%d.%m.%Y")
        end_date = self.time_period_end.strftime("%d.%m.%Y")

        # Format into German number formatting
        total_costs_formatted = str('{:0,.2f}'.format(self.total_cost)).\
            replace(".", "X").replace(",", ".").replace("X", ",")
        costs_per_training_formatted = str('{:0,.2f}'.format(self.cost_per_training_lesson).replace(".", ","))

        para_02 = Paragraph(f"""
            Rechnungsnummer: {self.invoice_nr}<br/>
            Zeitraum: {start_date} bis {end_date}<br/>
            {self.nr_of_training_lessons} Unterrichtseinheiten á 45 Minuten<br/>
            Kosten pro Unterrichtseinheit: {costs_per_training_formatted} €<br/>
            <b>Rechnungsbetrag: {total_costs_formatted} €</b><br/><br/><br/>
            """)

        para_03 = Paragraph(f"""
            Bitte überweisen Sie den Rechnungsbetrag innerhalb der nächsten {self.payment_horizon} Tage, spätestens bis 
            zum {self.latest_payment_date} auf folgendes Konto:<br/><br/>

            BeginnerLuft gGmbH<br/>
            IBAN: {self.iban}<br/>
            BIC: {self.bic}<br/>
            Verwendungszweck: {self.invoice_nr}
            """)

        para_list.append(para_01)
        para_list.append(para_02)
        para_list.append(para_03)

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

        res_table.setStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0)
        ])

        return res_table

    def _body_create_wire_instructions(self):
        """Create the wire instructions for transferring the money to BeginnerLuft"""

        para_list = []

        para_01 = Paragraph(f"""
            Bitte überweisen Sie den Rechnungsbetrag innerhalb der nächsten {self.payment_horizon} Tage, spätestens bis 
            zum {self.latest_payment_date} auf folgendes Konto:<br/><br/>
            
            BeginnerLuft gGmbH<br/>
            IBAN: {self.iban}<br/>
            BIC: {self.bic}<br/>
            Verwendungszweck: {self.invoice_nr}
                """)

        para_list.append(para_01)
        return para_list

    def _body_create_greetings(self):
        """Create the greetings at the end of the invoice document"""

        para_list = []
        para_01 = Paragraph(f"""
                    Mit freundlichen Grüßen<br/><br/><br/><br/><br/><br/>

                    {self.signer}
                        """)
        para_list.append(para_01)
        return para_list

    def create_footer(self):
        """Create a footer for the report"""

        width_list = [
            0.24 * self.col_widths[1],
            0.24 * self.col_widths[1],
            0.24 * self.col_widths[1],
            0.28 * self.col_widths[1],
        ]

        res = Table([
            ["BeginnerLuft gGmbH", "030 / 398 768 02", "Amtsgericht", "Bankinstitut: GLS Bank"],
            ["Bandelstr. 1", "www.beginnerluft.de", "Berlin Charlottenburg", f"IBAN: {self.iban}"],
            ["10559 Berlin", "info@beginnerluft.de", "HR209894 B", f"BIC: {self.bic}"]
        ],
            rowHeights=self.row_heights[2] / 7,  # use more rows to get lines closer together (hack)
            colWidths=width_list
        )


        res.setStyle([
            # ("GRID", (0, 0), (-1, -1), 1, "red"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 40),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            # ("BACKGROUND", (0, 0), (-1, -1), color),
            ("TEXTCOLOR", (0, 0), (-1, -1), "grey"),
            # ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # horizontal
            # ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ])
        return res



if __name__ == '__main__':

    jc = Jobcenter(name="Jobcenter Berlin Mitte", street="Seydelstr.", street_nr="2-5", zip_code="10117", city="Berlin")

    pdf = PDFInvoice(participant_name="Max Mustermann",
                     participant_title="Herr",
                     participant_id="1234567-AB",
                     invoice_nr="202110-99",
                     time_period_start=datetime.date(year=2021, month=8, day=9),
                     time_period_end=datetime.date(year=2021, month=10, day=31),
                     nr_of_training_lessons=40,
                     cost_per_training_lesson=12.34,
                     training_name="Individuelles Berufscoaching",
                     avgs_coupon_nr="9876-asdf",
                     signer="Peter Doe",
                     jobcenter=jc)
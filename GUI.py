import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk

from helpers import parse_date_from_string
from jobcenter import Jobcenter
from pdfreports import PDFInvoice



class BeginnerLuftGUI(tk.Tk):

    def __init__(self):
        super(BeginnerLuftGUI, self).__init__()
        self.title("BeginnerLuft")

        pd.set_option('display.expand_frame_repr', False)

        self.header_fontsize = 32
        self.font = "Times New Roman"
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Header.TLabel", font=(self.font, self.header_fontsize), background="white")
        self.style.configure("DataEntryHeader.TLabel", font=(self.font, 16, "bold"), background="white")
        self.style.configure("Normal.TLabel", background="white")
        self.style.configure("Data.TButton", width=30, background="white")
        self.style.configure("Annotation.TLabel", background="white", fontsize=6, foreground="grey")
        self.style.configure("TFrame", background="white")
        self.style.configure("DataEntry.TEntry")
        self.style.configure("TestBackground.TFrame")

        self.geometry("900x400")

        self.frm_header = ttk.Frame(self)
        self.frm_buttons = ttk.Frame(self)
        self.frm_header.grid(row=0, column=0)
        self.frm_buttons.grid(row=1, column=0)
        for i in range(2):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frm_header.grid_rowconfigure(0, weight=1)
        self.frm_header.grid_columnconfigure(0, weight=1)

        self.lbl_header = ttk.Label(self.frm_header, text="Rechnungserstellung", style="Header.TLabel")
        self.lbl_header.grid(row=0, column=0, columnspan=2)

        self.frm_buttons.grid_rowconfigure(0, weight=1)
        for i in range(2):
            self.frm_buttons.grid_columnconfigure(i, weight=1)

        self.btn_manual = ttk.Button(self.frm_buttons, text="Über manuelle Dateneingabe", style="Data.TButton",
                                     command=self.open_new_window)
        self.btn_manual.grid(row=1, column=0, padx=10)
        self.btn_database = ttk.Button(self.frm_buttons, text="Über Datenbank", style="Data.TButton")
        self.btn_database.grid(row=1, column=1, padx=10)
        self.lbl_not_implemented = ttk.Label(self.frm_buttons, text="Noch nicht implementiert", style="Annotation.TLabel")
        self.lbl_not_implemented.grid(row=2, column=1)

    def open_new_window(self):
        InvoiceDataEntry()


class InvoiceDataEntry(tk.Toplevel):

    def __init__(self):
        super(InvoiceDataEntry, self).__init__()
        self.frm_invoice = ttk.Frame(self, style="TestBackground.TFrame")
        self.frm_jobcenter = ttk.Frame(self, style="TestBackground.TFrame")
        self.frm_coaching = ttk.Frame(self, style="TestBackground.TFrame")
        self.frm_participant = ttk.Frame(self, style="TestBackground.TFrame")
        self.frm_go = ttk.Frame(self, style="TestBackground.TFrame")
        self.geometry("1000x500")
        self.participant_name = None
        self.participant_title = None
        self.participant_id = None
        self.avgs_coupon_nr = None
        self.invoice_nr = None
        self.time_period_start = None
        self.time_period_end = None
        self.nr_of_training_lessons = None
        self.cost_per_training_lesson = None
        self.training_name = "Individuelles Berufscoaching"
        self.signer = None
        self.jobcenter_name = None
        self.jobcenter_street_and_nr = None
        self.jobcenter_zip_and_city = None
        self.payment_horizon = 14
        self.creation_date = datetime.date.today()

        self.ent_participant_title = None
        self.ent_participant_name = None
        self.ent_participant_id = None
        self.ent_coaching_training_name = None
        self.ent_coaching_training_nr_lessons = None
        self.ent_coaching_training_start = None
        self.ent_coaching_training_end = None
        self.ent_coaching_cost_per_training_lesson = None
        self.ent_jc_name = None
        self.ent_jc_street_and_nr = None
        self.ent_jc_zip_city = None
        self.ent_invoice_date = None
        self.ent_invoice_payment_horizon = None
        self.ent_invoice_nr = None
        self.ent_invoice_signer = None  # to be changed to dropdown
        self.btn_go = None

        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        self.create_frame_layout()
        self.create_labels()
        self.create_entry_fields()
        self.set_default_values()
        self.create_go_button()

    def create_frame_layout(self):
        self.frm_participant.grid(row=1, column=0, sticky="new", padx=10)
        self.frm_coaching.grid(row=2, column=0, sticky="new", padx=10)
        self.frm_jobcenter.grid(row=1, column=1, sticky="new", padx=10)
        self.frm_invoice.grid(row=2, column=1, sticky="new", padx=10)
        self.frm_go.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10)

        for i in range(2):
            self.frm_go.grid_columnconfigure(i, weight=1)

    def create_labels(self):

        # PARTICIPANTS
        lbl_participant_header = ttk.Label(self.frm_participant, text="Teilnehmerdaten", style="DataEntryHeader.TLabel")
        lbl_participant_title = ttk.Label(self.frm_participant, text="Anrede des Teilnehmers", style="Normal.TLabel")
        lbl_participant_name = ttk.Label(self.frm_participant, text="Names des Teilnehmers", style="Normal.TLabel")
        lbl_participant_id = ttk.Label(self.frm_participant, text="Kundennummer des Teilnehmers", style="Normal.TLabel")

        for i, label in enumerate([lbl_participant_header, lbl_participant_title, lbl_participant_name, lbl_participant_id]):
            label.grid(row=i, column=0, sticky="nw")

        # COACHING DATA
        lbl_coaching_header = ttk.Label(self.frm_coaching, text="Coaching-Daten", style="DataEntryHeader.TLabel")
        lbl_training_name = ttk.Label(self.frm_coaching, text="Maßnahmenbezeichnung", style="Normal.TLabel")
        lbl_nr_training_lessons = ttk.Label(self.frm_coaching, text="Anzahl der Unterrichtseinheiten", style="Normal.TLabel")
        lbl_training_start = ttk.Label(self.frm_coaching, text="Beginn des Bewilligungszeitraums", style="Normal.TLabel")
        lbl_training_end = ttk.Label(self.frm_coaching, text="Ende des Bewilligungszeitraums", style="Normal.TLabel")
        lbl_training_cost = ttk.Label(self.frm_coaching, text="Kosten pro Unterrichtseinheit", style="Normal.TLabel")

        for i, label in enumerate([lbl_coaching_header, lbl_training_name, lbl_nr_training_lessons, lbl_training_start,
                                   lbl_training_end, lbl_training_cost]):
            label.grid(row=i, column=0, sticky="nw")

        # JOBCENTER
        lbl_jc_header = ttk.Label(self.frm_jobcenter, text="Jobcenter", style="DataEntryHeader.TLabel")
        lbl_jc_name = ttk.Label(self.frm_jobcenter, text="Name des Jobcenters", style="Normal.TLabel")
        lbl_jc_street_and_nr = ttk.Label(self.frm_jobcenter, text="Straße und Nr", style="Normal.TLabel")
        lbl_jc_zip_city = ttk.Label(self.frm_jobcenter, text="PLZ und Stadt", style="Normal.TLabel")

        for i, label in enumerate([lbl_jc_header, lbl_jc_name, lbl_jc_street_and_nr, lbl_jc_zip_city]):
            label.grid(row=i, column=0, sticky="nw")

        # INVOICE DATA
        lbl_invoice_header = ttk.Label(self.frm_invoice, text="Rechnungsdaten", style="DataEntryHeader.TLabel")
        lbl_invoice_date = ttk.Label(self.frm_invoice, text="Rechnungsdatum", style="Normal.TLabel")
        lbl_invoice_payment_horizon = ttk.Label(self.frm_invoice, text="Zahlungsziel in Tagen", style="Normal.TLabel")
        lbl_invoice_nr = ttk.Label(self.frm_invoice, text="Rechnungsnummer", style="Normal.TLabel")
        lbl_invoice_signer = ttk.Label(self.frm_invoice, text="Rechnung erstellt von", style="Normal.TLabel")

        for i, label in enumerate([lbl_invoice_header, lbl_invoice_date, lbl_invoice_payment_horizon, lbl_invoice_nr,
                                   lbl_invoice_signer]):
            label.grid(row=i, column=0, sticky="nw")

    def create_entry_fields(self):

        # PARTICIPANTS
        self.ent_participant_title = ttk.Entry(self.frm_participant, style="DataEntry.TEntry")
        self.ent_participant_name = ttk.Entry(self.frm_participant, style="DataEntry.TEntry")
        self.ent_participant_id = ttk.Entry(self.frm_participant, style="DataEntry.TEntry")

        for i, widget in enumerate([self.ent_participant_title, self.ent_participant_name, self.ent_participant_id]):
            widget.grid(row=i + 1, column=1, sticky="nw", padx=(5, 0))

        # COACHING
        self.ent_coaching_training_name = ttk.Entry(self.frm_coaching, style="DataEntry.TEntry")
        self.ent_coaching_training_nr_lessons = ttk.Entry(self.frm_coaching, style="DataEntry.TEntry")
        self.ent_coaching_training_start = ttk.Entry(self.frm_coaching, style="DataEntry.TEntry")
        self.ent_coaching_training_end = ttk.Entry(self.frm_coaching, style="DataEntry.TEntry")
        self.ent_coaching_cost_per_training_lesson = ttk.Entry(self.frm_coaching, style="DataEntry.TEntry")

        for i, widget in enumerate([self.ent_coaching_training_name, self.ent_coaching_training_nr_lessons,
                                    self.ent_coaching_training_start, self.ent_coaching_training_end,
                                    self.ent_coaching_cost_per_training_lesson]):
            widget.grid(row=i + 1, column=1, sticky="nw", padx=(5, 0))

        # JOBCENTER
        self.ent_jc_name = ttk.Entry(self.frm_jobcenter, style="DataEntry.TEntry")
        self.ent_jc_street_and_nr = ttk.Entry(self.frm_jobcenter, style="DataEntry.TEntry")
        self.ent_jc_zip_city = ttk.Entry(self.frm_jobcenter, style="DataEntry.TEntry")

        for i, widget in enumerate([self.ent_jc_name, self.ent_jc_street_and_nr, self.ent_jc_zip_city]):
            widget.grid(row=i + 1, column=1, sticky="nw", padx=(5, 0))

        # INVOICE DATA
        self.ent_invoice_date = ttk.Entry(self.frm_invoice, style="DataEntry.TEntry")
        self.ent_invoice_payment_horizon = ttk.Entry(self.frm_invoice, style="DataEntry.TEntry")
        self.ent_invoice_nr = ttk.Entry(self.frm_invoice, style="DataEntry.TEntry")
        self.ent_invoice_signer = ttk.Entry(self.frm_invoice, style="DataEntry.TEntry")

        for i, widget in enumerate([self.ent_invoice_date, self.ent_invoice_payment_horizon, self.ent_invoice_nr,
                                    self.ent_invoice_signer]):
            widget.grid(row=i + 1, column=1, sticky="nw", padx=(5, 0))

    def set_default_values(self):

        self.ent_coaching_training_name.insert(0, self.training_name)
        self.ent_invoice_date.insert(0, datetime.date.today())
        self.ent_invoice_payment_horizon.insert(0, 14)
        self.ent_invoice_signer.insert(0, "Jimmy Doe")

        # delete later
        self.ent_participant_title.insert(0, "Herr")
        self.ent_participant_name.insert(0, "Ahmed Muhadi")
        self.ent_participant_id.insert(0, "123456-abc")
        self.ent_coaching_training_nr_lessons.insert(0, 10)
        self.ent_coaching_training_start.insert(0, datetime.date(year=2021, month=10, day=28))
        self.ent_coaching_training_end.insert(0, datetime.date(year=2022, month=1, day=12))
        self.ent_coaching_cost_per_training_lesson.insert(0, "11,23")
        self.ent_invoice_nr.insert(0, "202112-99")
        self.ent_jc_name.insert(0, "Jobcenter Berlin Mitte")
        self.ent_jc_street_and_nr.insert(0, "Seydelstr. 2-5")
        self.ent_jc_zip_city.insert(0, "10117 Berlin")


    def create_go_button(self):

        self.btn_go = ttk.Button(self.frm_go, text="Rechnung erstellen!", command=self.create_invoice)
        self.btn_go.grid(row=0, column=0, columnspan=2, padx=20)

    def _get_data(self):

        # PARTICIPANT DATA
        self.participant_title = self.ent_participant_title.get()
        self.participant_name = self.ent_participant_name.get()
        self.participant_id = self.ent_participant_id.get()

        # COACHING DATA
        self.training_name = self.ent_coaching_training_name.get()
        self.nr_of_training_lessons = int(self.ent_coaching_training_nr_lessons.get())
        self.time_period_start = parse_date_from_string(self.ent_coaching_training_start.get())
        self.time_period_end = parse_date_from_string(self.ent_coaching_training_end.get())
        self.cost_per_training_lesson = float(self.ent_coaching_cost_per_training_lesson.get().replace(",", "."))

        # JOBCENTER
        self.jobcenter_name = self.ent_jc_name.get()
        self.jobcenter_street_and_nr = self.ent_jc_street_and_nr.get()
        self.jobcenter_zip_and_city = self.ent_jc_zip_city.get()

        # INVOICE DATA
        self.creation_date = parse_date_from_string(self.ent_invoice_date.get())
        self.payment_horizon = int(self.ent_invoice_payment_horizon.get())
        self.invoice_nr = self.ent_invoice_nr.get()
        self.signer = self.ent_invoice_signer.get()

    def create_invoice(self):

        self._get_data()
        jc_street, jc_nr = self.jobcenter_street_and_nr.split()
        jc_zip, jc_city = self.jobcenter_zip_and_city.split()
        jc = Jobcenter(name=self.jobcenter_name, street=jc_street, street_nr=jc_nr, zip_code=jc_zip, city=jc_city)
        invoice = PDFInvoice(
            participant_name=self.participant_name,
            participant_title=self.participant_title,
            participant_id=self.participant_id,
            avgs_coupon_nr="test",
            invoice_nr=self.invoice_nr,
            time_period_start=self.time_period_start,
            time_period_end=self.time_period_end,
            nr_of_training_lessons=self.nr_of_training_lessons,
            cost_per_training_lesson=self.cost_per_training_lesson,
            training_name=self.training_name,
            signer=self.signer,
            jobcenter=jc,
            payment_horizon=self.payment_horizon,
            creation_date=self.creation_date
        )

if __name__ == '__main__':
    gui = BeginnerLuftGUI()
    gui.mainloop()

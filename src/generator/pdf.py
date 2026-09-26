from __future__ import annotations
from dataclasses import dataclass, field
import datetime

from fpdf import FPDF


@dataclass
class ContentTopic:
    title: str
    page: int
    x: int = 0
    y: int = 0
    subs: list[ContentTopic] = field(default_factory=list)


contents: list[ContentTopic] = [
    ContentTopic(
        "1. Protocols",
        2,
        20,
        10,
        [
            ContentTopic("1.1 Bluetooth", 2, 20, 20),
            ContentTopic("1.2 Modbus-TCP", 2, 20, 130),
        ],
    ),
    ContentTopic(
        "2. Field Types",
        3,
        20,
        10,
        subs=[
            ContentTopic("2.1 Bool", 3, 20, 50),
            ContentTopic("2.2 UInt", 3, 20, 95),
            ContentTopic("2.3 Int", 3, 20, 120),
            ContentTopic("2.4 String", 3, 20, 145),
            ContentTopic("2.5 SWString", 3),
            ContentTopic("2.6 Version", 3),
            ContentTopic("2.7 Serial", 3),
        ],
    ),
    ContentTopic(
        "3. Fields",
        3,
        subs=[
            # TODO generate
        ],
    ),
]


def generate_pdf():
    pdf = CustomPDF()

    _cover_sheet(pdf)
    _table_of_contents(pdf)
    _protocols(pdf)
    _field_types(pdf)

    # Write to file
    pdf.output("out/Documentation.pdf")


# Helpers


class CustomPDF(FPDF):
    def footer(self):
        if self.page_no() == 1:
            return

        self.set_xy(-15, -15)
        self.set_font("Helvetica", size=8)
        page_text = f"{self.page_no() - 1}"
        self.cell(0, 10, page_text, new_x="LMARGIN", new_y="NEXT", align="C")


def _cover_sheet(pdf: FPDF):
    """Add cover sheet to pdf."""
    pdf.add_page()
    pdf.set_y(80)
    pdf.set_font("Helvetica", size=20)
    pdf.cell(text="Bluetti Registers", center=True)
    pdf.set_y(90)
    pdf.set_font("Helvetica", size=14)
    pdf.cell(text="Documentation", center=True)
    pdf.set_y(260)
    pdf.set_font("Helvetica", size=12)
    date = datetime.datetime.now().strftime("%B %d, %Y at %H:%M")
    pdf.cell(text=f"Generated on {date}", center=True)


def _table_of_contents(pdf: FPDF):
    """Add Table of contents to pdf."""
    pdf.add_page()
    pdf.set_font("Helvetica", size=20)
    pdf.cell(text="Table of contents", center=True)

    pdf.set_font("Helvetica", size=14)

    i = 0
    for topic in contents:
        i = _add_topic(pdf, topic, i=i)


def _add_topic(pdf: FPDF, topic: ContentTopic, indent=0, i=0) -> int:
    """Add a topic to the table of contents."""
    pdf.set_xy(20 + indent * 5, 30 + i * 7)
    link = pdf.add_link(page=topic.page + 1, x=float(topic.x), y=float(topic.y))
    pdf.cell(text=topic.title, link=link)
    pdf.set_x(-30)
    pdf.cell(text=str(topic.page))

    for sub in topic.subs:
        i = i + 1
        _add_topic(pdf, sub, indent + 1, i)

    return i + 1


def _protocols(pdf: FPDF):
    pdf.add_page()
    pdf.set_xy(20, 10)
    pdf.set_font("Helvetica", size=20)
    pdf.cell(text="1. Protocols")

    pdf.set_xy(20, 20)
    pdf.set_font("Helvetica", size=18)
    pdf.cell(text="1.1 Bluetooth")

    with open("docs/bluetooth.md", "r") as f:
        pdf.set_xy(25, 30)
        pdf.set_font("Helvetica", size=14)
        pdf.multi_cell(text=f.read(), markdown=True, w=160)
        f.close()

    pdf.set_xy(20, 130)
    pdf.set_font("Helvetica", size=18)
    pdf.cell(text="1.2 Modbus-TCP")

    with open("docs/modbus-tcp.md", "r") as f:
        pdf.set_xy(25, 140)
        pdf.set_font("Helvetica", size=14)
        pdf.multi_cell(text=f.read(), markdown=True, w=160)
        f.close()


def _field_types(pdf: FPDF):
    pdf.add_page()
    pdf.set_xy(20, 10)
    pdf.set_font("Helvetica", size=20)
    pdf.cell(text="2. Field Types")

    with open("docs/field_types.md", "r") as f:
        pdf.set_xy(25, 20)
        pdf.set_font("Helvetica", size=14)
        pdf.multi_cell(text=f.read(), markdown=True, w=160)
        f.close()

    pdf.set_xy(20, 50)
    pdf.set_font("Helvetica", size=18)
    pdf.cell(text="2.1 Bool")

    with open("docs/field_types/bool.md", "r") as f:
        pdf.set_xy(25, 60)
        pdf.set_font("Helvetica", size=14)
        pdf.multi_cell(text=f.read(), markdown=True, w=160)
        f.close()

    pdf.set_xy(20, 95)
    pdf.set_font("Helvetica", size=18)
    pdf.cell(text="2.2 UInt")

    with open("docs/field_types/uint.md", "r") as f:
        pdf.set_xy(25, 105)
        pdf.set_font("Helvetica", size=14)
        pdf.multi_cell(text=f.read(), markdown=True, w=160)
        f.close()

    pdf.set_xy(20, 120)
    pdf.set_font("Helvetica", size=18)
    pdf.cell(text="2.3 Int")

    with open("docs/field_types/int.md", "r") as f:
        pdf.set_xy(25, 130)
        pdf.set_font("Helvetica", size=14)
        pdf.multi_cell(text=f.read(), markdown=True, w=160)
        f.close()

    pdf.set_xy(20, 145)
    pdf.set_font("Helvetica", size=18)
    pdf.cell(text="2.4 String")

    with open("docs/field_types/string.md", "r") as f:
        pdf.set_xy(25, 155)
        pdf.set_font("Helvetica", size=14)
        pdf.multi_cell(text=f.read(), markdown=True, w=160)
        f.close()

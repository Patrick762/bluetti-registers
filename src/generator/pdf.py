from __future__ import annotations
from dataclasses import dataclass, field
import datetime

from fpdf import FPDF

from .datacls import DataField, DataProtocol


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
        5,
        20,
        10,
        [
            ContentTopic("1.1 Bluetooth", 2, 20, 20),
            ContentTopic("1.2 Modbus-TCP", 2, 20, 130),
        ],
    ),
    ContentTopic(
        "2. Field Types",
        6,
        20,
        10,
        subs=[
            ContentTopic("2.1 Bool", 3, 20, 50),
            ContentTopic("2.2 UInt", 3, 20, 95),
            ContentTopic("2.3 Int", 3, 20, 120),
            ContentTopic("2.4 String", 3, 20, 145),
            ContentTopic("2.5 SWString", 3, 20, 175),
            ContentTopic("2.6 Version", 4, 20, 20),
            ContentTopic("2.7 Serial", 4, 20, 60),
        ],
    ),
    ContentTopic(
        "3. Fields",
        8,
        20,
        10,
        subs=[],  # Generated
    ),
]


def generate_pdf(
    protocols: list[DataProtocol], translations: dict[str, dict[str, str]]
):
    pdf = CustomPDF()

    # generate field names for table of contents
    field_names: list[str] = []

    for proto in protocols:
        for field in proto.fields:
            if field.name not in field_names:
                field_names.append(field.name)

    field_names = sorted(field_names, key=str.lower)

    fields_per_page = 4
    contents[2].subs = [
        ContentTopic(f"3.{str(i+1)} {f}", 8 + (i // fields_per_page))
        for i, f in enumerate(field_names)
    ]

    _cover_sheet(pdf)
    _table_of_contents(pdf)
    _protocols(pdf)
    _field_types(pdf)
    _fields(pdf, field_names, protocols, translations)

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
    if i >= 34:
        pdf.add_page()
        pdf.set_font("Helvetica", size=14)
        i = 0

    pdf.set_xy(20 + indent * 5, 30 + i * 7)
    link = pdf.add_link(page=topic.page + 1, x=float(topic.x), y=float(topic.y))
    pdf.cell(text=topic.title, link=link)
    pdf.set_x(-30)
    pdf.cell(text=str(topic.page))

    i += 1

    for sub in topic.subs:
        i = _add_topic(pdf, sub, indent + 1, i)

    return i


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

    _add_field_type(pdf, "2.1 Bool", 50, "bool.md")
    _add_field_type(pdf, "2.2 UInt", 95, "uint.md")
    _add_field_type(pdf, "2.3 Int", 120, "int.md")
    _add_field_type(pdf, "2.4 String", 145, "string.md")
    _add_field_type(pdf, "2.5 SWString", 175, "swstring.md")

    pdf.add_page()
    _add_field_type(pdf, "2.6 Version", 20, "version.md")
    _add_field_type(pdf, "2.7 Serial", 60, "serial.md")


def _add_field_type(pdf: FPDF, title: str, y: int, md: str):
    pdf.set_xy(20, y)
    pdf.set_font("Helvetica", size=18)
    pdf.cell(text=title)

    with open(f"docs/field_types/{md}", "r") as f:
        pdf.set_xy(25, y + 10)
        pdf.set_font("Helvetica", size=14)
        pdf.multi_cell(text=f.read(), markdown=True, w=160)
        f.close()


def _fields(
    pdf: FPDF,
    field_names: str,
    protocols: list[DataProtocol],
    translations: dict[str, dict[str, str]],
):
    t_en = translations["en"]

    pdf.add_page()
    pdf.set_xy(20, 10)
    pdf.set_font("Helvetica", size=20)
    pdf.cell(text="3. Fields")

    fields_per_page = 4
    for i, f in enumerate(field_names):
        definitions: list[DataProtocol] = []

        for proto in protocols:
            for field in proto.fields:
                if field.name == f:
                    definitions.append(
                        DataProtocol(proto.version, proto.comm_type, [field])
                    )

        if i > 0 and (i % fields_per_page) == 0:
            pdf.add_page()

        _add_field(pdf, 20 + (i % fields_per_page) * 65, i, f, definitions, t_en[f])


def _add_field(
    pdf: FPDF, y: int, i: int, field_name: str, f: list[DataProtocol], text: str
):
    pdf.set_xy(20, y)
    pdf.set_font("Helvetica", size=18)
    pdf.cell(text=f"3.{str(i+1)} {field_name}")

    pdf.set_xy(25, y + 10)
    pdf.set_font("Helvetica", size=14)
    pdf.cell(text=text)

    table_data = [
        ["Protocol", "Version", "Start address", "Length", "Scaling", "Unit"],
    ] + [
        [
            p.comm_type,
            str(p.version),
            str(p.fields[0].start),
            str(p.fields[0].length),
            str(p.fields[0].scaling),
            p.fields[0].unit,
        ]
        for p in f
    ]

    pdf.set_xy(25, y + 20)
    pdf.set_font("Times", size=14)
    with pdf.table() as table:
        for data_row in table_data:
            row = table.row()
            for cell in data_row:
                row.cell(cell)

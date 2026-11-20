
import re


INSTITUTIONS = [
    # South African universities
    "Nelson Mandela University",
    "University of Cape Town",
    "University of Fort Hare",
    "University of Johannesburg",
    "University of Pretoria",
    "University of South Africa",
    "University of the Western Cape",
    "University of the Witwatersrand",
    "University of KwaZulu-Natal",
    "University of Limpopo",
    "University of Venda",
    "University of Zululand",
    "Walter Sisulu University",
    "Rhodes University",
    "Stellenbosch University",
    "North-West University",
    "University of Mpumalanga",
    "Sol Plaatje University",
    "University of the Free State",
    "Cape Peninsula University of Technology",
    "Durban University of Technology",
    "Tshwane University of Technology",
    "Vaal University of Technology",
    "Central University of Technology",

    # Colleges
    "Eastcape Midlands TVET College",
    "King Hintsa TVET College",
    "Buffalo City TVET College",
    "Lovedale TVET College",
    "Port Elizabeth TVET College",
    "South Cape TVET College",
    "False Bay TVET College",
    "Northlink College",
    "College of Cape Town",
    "Motheo TVET College",
    "Orbit TVET College",
    "Ekurhuleni East TVET College",
    "Ekurhuleni West TVET College",
    "Tshwane South TVET College",
    "Tshwane North TVET College",
]


def extract_institutions(text):
    """
    Identify known educational institutions mentioned in CV text.

    Returns a list of unique institution names.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    found_institutions = []

    for institution in sorted(INSTITUTIONS, key=len, reverse=True):
        pattern = (
            r"(?<!\w)"
            + re.escape(institution)
            + r"(?!\w)"
        )

        if re.search(pattern, text, re.IGNORECASE):
            found_institutions.append(institution)

    return found_institutions

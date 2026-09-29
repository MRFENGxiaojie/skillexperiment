# -*- coding: utf-8 -*-
import os
import zipfile
from openpyxl import Workbook
from openpyxl.styles import Font

ROOT = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.join(ROOT, "task")

# (user, score, comment, submitted_at, segment)
responses = [
    ("carlos@triptico.com.br", 10, "Great tool overall; please add BRL billing and local tax soon.", "2026-07-05 09:12", "Mid-Market"),
    ("j.parker@northwind.io", 8, "Love the kanban boards; just wish the app was faster.", "2026-07-05 11:47", "Enterprise"),
    ("lena@stacktack.io", 9, "Solid product, our dev team is very happy with it.", "2026-07-06 08:30", "Mid-Market"),
    ("priya@nimbus.co.in", 7, "Good value, but integrations break too often.", "2026-07-06 14:02", "Mid-Market"),
    ("devin@brightmedia.io", 10, "Excellent tool. Dark mode is the one thing we are waiting for.", "2026-07-07 10:21", "Mid-Market"),
    ("kenji.t@hanami.gg", 4, "Afternoon timeouts are killing us; search is too slow at our scale.", "2026-07-07 16:55", "Mid-Market"),
    ("sofia@meridien.fr", 9, "Very useful for our small team. Invite emails go to spam though.", "2026-07-08 09:40", "SMB"),
    ("elena@brightmode.nl", 8, "Mobile experience is frustrating, but the desktop app is fine.", "2026-07-08 13:18", "SMB"),
    ("sarah@figagency.com", 9, "Would recommend. A Gantt view would make it perfect for us.", "2026-07-09 11:05", "Enterprise"),
    ("tom@greenhouse.eco", 5, "I was charged after cancelling my trial; that left a bad taste.", "2026-07-10 09:33", "SMB"),
    ("maria.santos@cafeinternacional.com.br", 7, "Good onboarding, but billing in BRL with correct taxes is a must.", "2026-07-11 15:20", "Enterprise"),
    ("ian@compasslabs.com", 9, "Reliable and powerful. Need templates and workload limits next.", "2026-07-12 10:10", "Enterprise"),
    ("hana@kitsune.jp", 9, "Like it a lot; a native mobile app would really help our field team.", "2026-07-13 12:44", "Mid-Market"),
    ("gabe@paperplane.io", 9, "Great so far. Please add dark mode so our team stops squinting.", "2026-07-14 09:07", "SMB"),
    ("alice@lambda.dev", 6, "Billing is confusing; the upgrade process needs to be clearer.", "2026-07-15 17:29", "SMB"),
]

wb = Workbook()
ws = wb.active
ws.title = "responses"
ws.append(["user", "score", "comment", "submitted_at", "segment"])
for r in responses:
    ws.append(list(r))

total = len(responses)
promoters = sum(1 for r in responses if r[1] >= 9)
passives = sum(1 for r in responses if 7 <= r[1] <= 8)
detractors = sum(1 for r in responses if r[1] <= 6)
pct_promoters = round(promoters / total * 100, 1)
pct_detractors = round(detractors / total * 100, 1)
nps = round(pct_promoters - pct_detractors, 1)

ws2 = wb.create_sheet("summary")
ws2["A1"] = "Metric"
ws2["B1"] = "Value"
for r in [("Total responses", total),
          ("Promoters (9-10)", promoters),
          ("Passives (7-8)", passives),
          ("Detractors (0-6)", detractors),
          ("% Promoters", f"{pct_promoters}%"),
          ("% Detractors", f"{pct_detractors}%"),
          ("NPS score", nps)]:
    ws2.append(list(r))

bold = Font(bold=True)
for cell in ws2["1:1"]:
    cell.font = bold
for cell in ws2["A"]:
    cell.font = bold

xlsx_path = os.path.join(TASK, "nps-survey.xlsx")
wb.save(xlsx_path)

names = ["in-app-feedback.csv", "support-tickets.csv", "nps-survey.xlsx", "interview-notes.md"]
zip_path = os.path.join(TASK, "feedback-data.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for n in names:
        zf.write(os.path.join(TASK, n), arcname=n)

print("NPS =", nps)
print("Dist -> P:", promoters, "Pass:", passives, "Det:", detractors)

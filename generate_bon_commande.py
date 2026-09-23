from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

output = r"C:\Users\conta\OneDrive\Bureau\dynedoc-fatality\bon-de-commande-console-arcade.pdf"
font = r"C:\Windows\Fonts\arial.ttf"
font_bold = r"C:\Windows\Fonts\arialbd.ttf"
pdfmetrics.registerFont(TTFont("Arial", font))
pdfmetrics.registerFont(TTFont("Arial-Bold", font_bold))

ink = HexColor("#18212B")
muted = HexColor("#66717D")
accent = HexColor("#E85D35")
line = HexColor("#D9DEE3")
soft = HexColor("#F4F6F7")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Body", fontName="Arial", fontSize=8.6, leading=11, textColor=ink))
styles.add(ParagraphStyle(name="Small", fontName="Arial", fontSize=7.2, leading=9, textColor=muted))
styles.add(ParagraphStyle(name="TitleCustom", fontName="Arial-Bold", fontSize=24, leading=27, textColor=ink))
styles.add(ParagraphStyle(name="Subtitle", fontName="Arial", fontSize=10, leading=13, textColor=muted))
styles.add(ParagraphStyle(name="Section", fontName="Arial-Bold", fontSize=8, leading=10, textColor=accent))
styles.add(ParagraphStyle(name="Right", parent=styles["Body"], alignment=TA_RIGHT))
styles.add(ParagraphStyle(name="RightSmall", parent=styles["Small"], alignment=TA_RIGHT))
styles.add(ParagraphStyle(name="TableHead", fontName="Arial-Bold", fontSize=7.2, leading=9, textColor=colors.white))
styles.add(ParagraphStyle(name="Total", fontName="Arial-Bold", fontSize=11, leading=13, textColor=colors.white))

items = [
    ("ELEC-001", "Raspberry Pi 4 Model B, 4 Go de RAM, ordinateur principal de la console", 1, 75.00),
    ("DISP-001", "Écran LCD HDMI 5 pouces, résolution 800x480, avec support de fixation", 1, 65.00),
    ("CTRL-001", "Joystick arcade 8 directions avec microswitches", 2, 18.00),
    ("CTRL-002", "Bouton arcade lumineux ou standard, diamètre 30 mm", 8, 3.00),
    ("CTRL-003", "Encodeur USB arcade deux joueurs, reconnu comme clavier HID", 1, 18.00),
    ("MEM-001", "Carte microSD 32 Go, installation du système et du jeu", 1, 12.00),
    ("PWR-001", "Alimentation USB-C 5 V / 3 A compatible Raspberry Pi 4", 1, 15.00),
    ("PWR-002", "Batterie externe USB 5 000 mAh minimum, pour utilisation autonome", 1, 25.00),
    ("AUDIO-001", "Petit système audio USB ou haut-parleur amplifié", 1, 8.00),
    ("MECA-001", "Boîtier sur mesure, impression 3D ou découpe bois, avec visserie", 1, 35.00),
    ("MECA-002", "Câblage, connecteurs, interrupteur général et bouton d'arrêt propre", 1, 21.00),
]
subtotal = sum(qty * price for _, _, qty, price in items)
vat = subtotal * 0.20
total = subtotal + vat
money = lambda value: f"{value:,.2f} EUR".replace(",", "X").replace(".", ",").replace("X", " ")

story = []
header = Table([
    [Paragraph('<font color="#E85D35"><b>PROJET FATALITY</b></font><br/><font size="24"><b>Bon de commande</b></font><br/><font color="#66717D">Mini console arcade dédiée - 2 joueurs</font>', styles["Body"]),
     Paragraph('<b>BC-2026-001</b><br/><font color="#66717D">Date : 23/09/2026<br/>Validité : à confirmer</font>', styles["Right"])]
], colWidths=[115*mm, 55*mm])
header.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 3, accent),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10), ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
]))
story += [header, Spacer(1, 7*mm)]

box_style = TableStyle([
    ("BOX", (0, 0), (-1, -1), 0.7, line), ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
])
meta = Table([
    [Paragraph('<font color="#E85D35"><b>EMETTEUR / CLIENT</b></font><br/><br/>Nom : __________________________<br/>Adresse : _______________________<br/>E-mail : _________________________', styles["Body"]),
     Paragraph('<font color="#E85D35"><b>FOURNISSEUR</b></font><br/><br/>Société : ________________________<br/>Adresse : _______________________<br/>Référence devis : ________________', styles["Body"])]
], colWidths=[85*mm, 85*mm])
meta.setStyle(box_style)
story += [meta, Spacer(1, 5*mm)]

rows = [[Paragraph("Référence", styles["TableHead"]), Paragraph("Désignation", styles["TableHead"]), Paragraph("Qté", styles["TableHead"]), Paragraph("Prix unitaire HT", styles["TableHead"]), Paragraph("Total HT", styles["TableHead"])]]
for code, description, qty, price in items:
    rows.append([Paragraph(code, styles["Small"]), Paragraph(description, styles["Body"]), Paragraph(str(qty), styles["Right"]), Paragraph(money(price), styles["Right"]), Paragraph(money(qty * price), styles["Right"])])
order_table = Table(rows, colWidths=[22*mm, 86*mm, 12*mm, 25*mm, 25*mm], repeatRows=1)
order_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), ink), ("GRID", (0, 0), (-1, -1), 0.35, line),
    ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story += [order_table, Spacer(1, 4*mm)]

summary = Table([
    ["Sous-total HT", money(subtotal)],
    ["TVA estimative (20 %)", money(vat)],
    [Paragraph("Total TTC", styles["Total"]), Paragraph(money(total), styles["Total"])],
], colWidths=[48*mm, 35*mm], hAlign="RIGHT")
summary.setStyle(TableStyle([
    ("ALIGN", (1, 0), (1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, 1), 0.4, line),
    ("BACKGROUND", (0, 2), (-1, 2), accent), ("TEXTCOLOR", (0, 2), (-1, 2), colors.white),
    ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story += [summary, Spacer(1, 5*mm)]

note = Table([[Paragraph('<b>Objet de la commande :</b> réalisation d\'une mini console autonome démarrant directement sur le jeu Fatality en mode plein écran, avec commandes arcade pour deux joueurs. Les prix sont indicatifs et doivent être validés par devis avant achat.', styles["Body"])]], colWidths=[170*mm])
note.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), soft), ("LINEBEFORE", (0, 0), (0, -1), 3, accent), ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
story += [note, Spacer(1, 4*mm), Paragraph('<b>Spécifications attendues :</b> démarrage automatique sur le jeu, fonctionnement hors connexion, affichage HDMI 800x480, boutons reconnus comme entrées clavier USB, alimentation 5 V / 3 A, boîtier avec accès aux commandes et ventilation minimale. L adaptation du jeu pour deux joueurs et la configuration logicielle ne sont pas incluses dans le montant matériel.', styles["Small"]), Spacer(1, 8*mm)]

signatures = Table([[Paragraph('Signature du client, précédée de la mention « Bon pour accord »<br/><br/><br/>', styles["Small"]), Paragraph('Signature du fournisseur<br/><br/><br/>', styles["Small"])]], colWidths=[85*mm, 85*mm])
signatures.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 0.7, ink), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
story += [signatures, Spacer(1, 4*mm), Paragraph('Document préparatoire - prix indicatifs                                      Projet Fatality - Mini console arcade', styles["Small"])]

doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=14*mm, bottomMargin=14*mm, title="Bon de commande - Mini console arcade")
doc.build(story)
print(output)

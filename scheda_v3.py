import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

VERSION = "1.3.0"

W, H = A4

INK          = colors.HexColor('#1a1008')
PARCHMENT    = colors.HexColor('#f5edd6')
PARCHMENT_DK = colors.HexColor('#e8d9b5')
BORDER       = colors.HexColor('#6b4c1e')
ACCENT       = colors.HexColor('#8b3a0f')
LIGHT_LINE   = colors.HexColor('#c4a96a')
FILL_BG      = colors.HexColor('#fdf6e3')

def fancy_box(c, x, y, w, h, title=None, ts=8.5):
    c.setFillColor(colors.HexColor('#c4a96a'))
    c.roundRect(x+2, y-2, w, h, 3, fill=1, stroke=0)
    c.setFillColor(FILL_BG); c.setStrokeColor(BORDER); c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
    c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.4)
    c.roundRect(x+2.5, y+2.5, w-5, h-5, 2, fill=0, stroke=1)
    if title:
        banner(c, x+w/2, y+h-1, title, ts)

def banner(c, cx, cy, text, size=8.5):
    c.setFont("Helvetica-Bold", size)
    tw = c.stringWidth(text, "Helvetica-Bold", size)
    bw, bh = tw+18, size+6
    bx, by = cx-bw/2, cy-bh/2
    c.setFillColor(BORDER); c.setStrokeColor(INK); c.setLineWidth(0.6)
    c.roundRect(bx, by, bw, bh, 2, fill=1, stroke=1)
    for flip in (False, True):
        path = c.beginPath()
        ex = bx if not flip else bx+bw
        dx = -5  if not flip else 5
        path.moveTo(ex, by+bh*0.2); path.lineTo(ex+dx, by+bh/2)
        path.lineTo(ex, by+bh*0.8); path.close()
        c.setFillColor(ACCENT); c.drawPath(path, fill=1, stroke=0)
    c.setFillColor(PARCHMENT)
    c.drawCentredString(cx, by+3.5, text)

def iline(c, x, y, w, label=None, ls=6.5):
    c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.6)
    c.line(x, y, x+w, y)
    if label:
        c.setFont("Helvetica", ls); c.setFillColor(ACCENT)
        c.drawString(x, y+2, label); c.setFillColor(INK)

def diam_line(c, x, y, w):
    mid = x+w/2
    c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.7)
    c.line(x, y, mid-6, y); c.line(mid+6, y, x+w, y)
    p = c.beginPath()
    p.moveTo(mid, y+4); p.lineTo(mid+4, y)
    p.lineTo(mid, y-4); p.lineTo(mid-4, y); p.close()
    c.setFillColor(ACCENT); c.setStrokeColor(BORDER); c.setLineWidth(0.5)
    c.drawPath(p, fill=1, stroke=1)

def stat_block(c, cx, cy, label, sz=46):
    bx, by = cx-sz/2, cy-sz/2
    c.setFillColor(PARCHMENT_DK); c.setStrokeColor(BORDER); c.setLineWidth(1.5)
    c.roundRect(bx, by, sz, sz, 6, fill=1, stroke=1)
    m = 5
    c.setFillColor(FILL_BG); c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.5)
    c.roundRect(bx+m, by+m, sz-m*2, sz-m*2, 3, fill=1, stroke=1)
    # modifier box below — empty, no label
    mw, mh = sz*0.60, 13
    c.setFillColor(PARCHMENT_DK); c.setStrokeColor(BORDER); c.setLineWidth(1)
    c.roundRect(cx-mw/2, by-mh-2, mw, mh, 2, fill=1, stroke=1)
    banner(c, cx, by-mh-14, label, 7.2)

def skill_row(c, x, y, name, attr, row_w):
    c.setFillColor(FILL_BG); c.setStrokeColor(BORDER); c.setLineWidth(0.8)
    c.circle(x+5, y+4, 4, fill=1, stroke=1)
    c.setFillColor(FILL_BG); c.setStrokeColor(BORDER); c.setLineWidth(0.6)
    c.rect(x+16, y+1, 7, 7, fill=1, stroke=1)
    c.roundRect(x+28, y, 16, 9, 1, fill=1, stroke=1)
    c.setFont("Helvetica", 7.8); c.setFillColor(INK)
    c.drawString(x+48, y+2, name)
    c.setFont("Helvetica-Oblique", 6.5); c.setFillColor(ACCENT)
    c.drawRightString(x+row_w-2, y+2, f"({attr})"); c.setFillColor(INK)

def corner(c, x, y, fx=False, fy=False):
    c.saveState(); c.translate(x, y)
    if fx: c.scale(-1, 1)
    if fy: c.scale(1, -1)
    c.setStrokeColor(BORDER); c.setLineWidth(0.8); c.setFillColor(ACCENT)
    c.line(0,0,14,0); c.line(0,0,0,14)
    c.circle(0,0,3, fill=1, stroke=0)
    c.restoreState()

def build():
    os.makedirs("output", exist_ok=True)
    out_path = f"output/scheda_personaggio_v{VERSION}.pdf"
    c = canvas.Canvas(out_path, pagesize=A4)
    c.setTitle("Historia — Scheda del Personaggio")

    # background
    c.setFillColor(PARCHMENT); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor('#e0cfa0')); c.setLineWidth(0.15)
    for i in range(0, int(W+H), 10):
        c.line(max(0,i-H), min(H,i), min(W,i), max(0,i-W))
    c.setStrokeColor(BORDER); c.setLineWidth(2.5)
    c.roundRect(6,6,W-12,H-12,8,fill=0,stroke=1)
    c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.8)
    c.roundRect(10,10,W-20,H-20,6,fill=0,stroke=1)
    corner(c,12,12); corner(c,W-12,12,fx=True)
    corner(c,12,H-12,fy=True); corner(c,W-12,H-12,fx=True,fy=True)

    M = 16

    # ── HEADER ──────────────────────────────────────────────────────────────
    # Title: Historia in large italic serif feel
    c.setFont("Helvetica-BoldOblique", 18); c.setFillColor(BORDER)
    c.drawCentredString(W/2, H-M-8, "Historia")
    c.setFont("Helvetica-Oblique", 7); c.setFillColor(ACCENT)
    c.drawCentredString(W/2, H-M-17, "Scheda del Personaggio")
    c.setStrokeColor(ACCENT); c.setLineWidth(1.2)
    c.line(M+4, H-M-21, W-M-4, H-M-21)

    r1y = H-M-34
    for fw,fl,fx in [(200,"Nome",M+4),(118,"Famiglia",M+212),
                      (108,"Specie",M+338),(105,"Mestiere",M+454)]:
        iline(c, fx, r1y, fw, fl)

    r2y = r1y-18
    for fw,fl,fx in [(72,"Iniziativa",M+4),(72,"Ispirazione",M+84),
                      (72,"Velocità",M+164),(44,"PP",M+244),
                      (32,"Tg",M+296),(219,"Ventura e Risalto",M+340)]:
        iline(c, fx, r2y, fw, fl)

    diam_line(c, M, r2y-10, W-M*2)

    # ════════════════════════════════════════════════════════════════════════
    # BODY: three columns side by side
    #   LEFT  = Abilità
    #   CENTER= Caratteristiche (stats)
    #   RIGHT = Competenze
    # ════════════════════════════════════════════════════════════════════════
    body_top = r2y - 18

    LW = 182   # abilità column
    CW = 148   # stats column
    RW = W - M*2 - LW - CW - 16   # competenze column (~remaining ≈ 215)
    LX = M
    CX = LX + LW + 8
    RX = CX + CW + 8

    # ── LEFT: Abilità ───────────────────────────────────────────────────────
    skills = [
        ("Acrobazia","Des"),("Addestrare Animali","Sag"),("Arcano","Int"),
        ("Atletica","For"),("Furtività","Des"),("Indagare","Int"),
        ("Inganno","Car"),("Intimidire","Car"),("Intrattenere","Car"),
        ("Intuizione","Sag"),("Medicina","Sag"),("Natura","Int"),
        ("Percezione","Sag"),("Persuasione","Car"),("Rapidità di Mano","Des"),
        ("Religione","Int"),("Sopravvivenza","Sag"),("Storia","Int"),
    ]
    SK_H = 13
    sk_box_h = len(skills)*SK_H + 26
    sk_y = body_top - sk_box_h
    fancy_box(c, LX, sk_y, LW, sk_box_h, "Abilità", 9)

    c.setFont("Helvetica", 6); c.setFillColor(ACCENT)
    c.drawCentredString(LX+9,    sk_y+sk_box_h-16, "Cpt")
    c.drawCentredString(LX+23.5, sk_y+sk_box_h-16, "Mst")
    c.drawCentredString(LX+40,   sk_y+sk_box_h-16, "Mdf")
    c.setFillColor(INK); c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.4)
    c.line(LX+5, sk_y+sk_box_h-18, LX+LW-5, sk_y+sk_box_h-18)

    for i,(sk,attr) in enumerate(skills):
        sy = sk_y+sk_box_h-30-i*SK_H
        skill_row(c, LX+4, sy, sk, attr, LW-8)
        if i < len(skills)-1:
            c.setStrokeColor(colors.HexColor('#ddd0b0')); c.setLineWidth(0.25)
            c.line(LX+42, sy-1, LX+LW-6, sy-1)

    # ── CENTER: Caratteristiche (2×3 grid) ──────────────────────────────────
    SZ     = 46
    MODH   = 15
    NAMH   = 16
    CELL_H = SZ + MODH + NAMH + 8
    CELL_W = SZ + 26

    stats = [
        ("Forza","For"),       ("Intelligenza","Int"),
        ("Destrezza","Des"),   ("Saggezza","Sag"),
        ("Costituzione","Cos"),("Carisma","Car"),
    ]
    grid_w  = 2*CELL_W
    grid_ox = CX + (CW - grid_w)/2 + CELL_W/2
    stat_top = body_top - SZ/2 - 8

    for idx,(sname,_) in enumerate(stats):
        col = idx%2; row = idx//2
        sx = grid_ox + col*CELL_W
        sy = stat_top - row*CELL_H
        stat_block(c, sx, sy, sname, SZ)

    # bottom of stats grid (used to know how tall the center used)
    stat_bottom = stat_top - 2*CELL_H - SZ/2 - MODH - NAMH

    # ── RIGHT: Competenze + Bonus circle ────────────────────────────────────
    comp_box_h = body_top - sk_y   # same height as abilità column
    comp_y = sk_y

    # Competenze main box (full height of right column)
    fancy_box(c, RX, comp_y, RW, comp_box_h, "Competenze", 8.5)

    # Bonus circle interrupting the top border
    circ_r  = 20
    circ_cx = RX + RW - circ_r - 8
    circ_cy = comp_y + comp_box_h          # centre sits on the top edge

    # erase the top border segment under the circle
    c.setFillColor(PARCHMENT); c.setStrokeColor(PARCHMENT); c.setLineWidth(0)
    c.rect(circ_cx - circ_r + 1, circ_cy - 3, (circ_r - 1) * 2, 6, fill=1, stroke=0)

    # outer circle
    c.setFillColor(PARCHMENT_DK); c.setStrokeColor(BORDER); c.setLineWidth(1.2)
    c.circle(circ_cx, circ_cy, circ_r, fill=1, stroke=1)
    # thin inner ring close to edge, leaving space for text
    c.setFillColor(FILL_BG); c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.4)
    c.circle(circ_cx, circ_cy, circ_r - 3, fill=1, stroke=1)
    # "bonus" curved along the inside bottom arc
    arc_font, arc_size = "Helvetica-Oblique", 5.5
    arc_text = "bonus"
    arc_r = circ_r - 7        # text baseline radius (inside)
    spacing = 1.0             # extra pt between characters
    c.setFont(arc_font, arc_size); c.setFillColor(ACCENT)
    char_widths = [c.stringWidth(ch, arc_font, arc_size) for ch in arc_text]
    total_w = sum(char_widths) + spacing * (len(arc_text) - 1)
    total_span = total_w / arc_r  # radians
    angle = math.radians(270) - total_span / 2
    for ch, cw in zip(arc_text, char_widths):
        mid = angle + (cw / 2) / arc_r
        x = circ_cx + arc_r * math.cos(mid)
        y = circ_cy + arc_r * math.sin(mid)
        c.saveState()
        c.translate(x, y)
        c.rotate(math.degrees(mid) + 90)
        c.drawCentredString(0, 0, ch)
        c.restoreState()
        angle += (cw + spacing) / arc_r

    # competenze lines
    lines_comp = int((comp_box_h - 26) // 13)
    for li in range(lines_comp):
        iline(c, RX+8, comp_y+comp_box_h-24-li*13, RW-16)

    # ════════════════════════════════════════════════════════════════════════
    # PERSONALITY ROW: Tratto | Ideale | Legame | Difetto  (side by side)
    # placed just below the three columns (= below skills box = sk_y)
    # ════════════════════════════════════════════════════════════════════════
    diam_line(c, M, sk_y-8, W-M*2)

    pers_gap   = 6
    pers_h     = 62   # height of personality boxes
    pers_y     = sk_y - 14 - pers_h
    pers_names = ["Tratto","Ideale","Legame","Difetto"]
    pers_w     = (W - M*2 - pers_gap*(len(pers_names)-1)) / len(pers_names)

    for i, pname in enumerate(pers_names):
        px = M + i*(pers_w+pers_gap)
        fancy_box(c, px, pers_y, pers_w, pers_h, pname, 8)
        lines_p = max(2, int((pers_h-20)//13))
        for li in range(lines_p):
            iline(c, px+6, pers_y+pers_h-22-li*13, pers_w-12)

    # ════════════════════════════════════════════════════════════════════════
    # COMBAT SECTION: Classe Armatura | Attacchi | Azioni | Azioni Bonus | Reazioni
    # ════════════════════════════════════════════════════════════════════════
    diam_line(c, M, pers_y-8, W-M*2)

    combat_top = pers_y - 14
    combat_h   = 83   # +15% rispetto a 72

    # Classe Armatura (narrow, left)
    ca_w = 58
    ca_y = combat_top - combat_h
    fancy_box(c, M, ca_y, ca_w, combat_h, "Classe Armatura", 7)
    c.setFillColor(FILL_BG); c.setStrokeColor(BORDER); c.setLineWidth(1.5)
    circ_r = 13
    c.circle(M+ca_w/2, ca_y+combat_h*0.68, circ_r, fill=1, stroke=1)

    # Indebolimento — dividing line, label, 6 fillable dots
    ind_label_y = ca_y + combat_h*0.38
    c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.5)
    c.line(M+4, ind_label_y, M+ca_w-4, ind_label_y)
    banner(c, M+ca_w/2, ca_y + combat_h*0.30, "Indebolimento", 6)
    # 6 dots to fill in pencil
    dot_r = 4
    dot_count = 6
    dot_y = ca_y + combat_h*0.13
    dot_spacing = (ca_w - 16) / (dot_count - 1)
    for di in range(dot_count):
        dx = M + 8 + di * dot_spacing
        c.setFillColor(FILL_BG); c.setStrokeColor(BORDER); c.setLineWidth(0.8)
        c.circle(dx, dot_y, dot_r, fill=1, stroke=1)

    # Attacchi
    att_x = M + ca_w + 8
    att_w = 152
    fancy_box(c, att_x, ca_y, att_w, combat_h, "Attacchi", 9)
    c.setFont("Helvetica-Bold", 6.5); c.setFillColor(ACCENT)
    c.drawString(att_x+4, ca_y+combat_h-16, "Arma / Attacco")
    c.drawString(att_x+82, ca_y+combat_h-16, "Bonus")
    c.drawString(att_x+108, ca_y+combat_h-16, "Danno/Tipo")
    c.setFillColor(INK); c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.4)
    c.line(att_x+4, ca_y+combat_h-18, att_x+att_w-4, ca_y+combat_h-18)
    row_h_att = (combat_h - 22) / 4
    for i in range(4):
        ay = ca_y+combat_h-20-i*row_h_att
        c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.5)
        c.line(att_x+4, ay, att_x+80, ay)
        c.line(att_x+82, ay, att_x+106, ay)
        c.line(att_x+108, ay, att_x+att_w-4, ay)

    # Azioni / Azioni Bonus / Reazioni  (3 equal columns filling remaining width)
    act_x   = att_x + att_w + 8
    act_tot = W - M - act_x
    act_gap = 5
    act_w   = (act_tot - act_gap*2) / 3

    for i, aname in enumerate(["Azioni","Azioni Bonus","Reazioni"]):
        ax = act_x + i*(act_w+act_gap)
        fancy_box(c, ax, ca_y, act_w, combat_h, aname, 7.5)
        lines_a = max(3, int((combat_h-22)//12))
        for li in range(lines_a):
            iline(c, ax+5, ca_y+combat_h-24-li*12, act_w-10)

    # ════════════════════════════════════════════════════════════════════════
    # BOTTOM ROW: [P.Ferita + Dadi Vita stacked] | Conio | Equipaggiamento
    # ════════════════════════════════════════════════════════════════════════
    diam_line(c, M, ca_y-8, W-M*2)

    bot_top = ca_y - 14
    bot_h   = bot_top - (M + 10)
    bot_y   = M + 10

    # P. Ferita + Dadi Vita stacked in one column
    pf_col_w = 80
    pf_h_dv  = bot_h * 0.38               # Dadi Vita: compact
    pf_h_pf  = bot_h - pf_h_dv - 6       # P.Ferita: larger

    # ── Dadi Vita (bottom, smaller) ─────────────────────────────────────────
    fancy_box(c, M, bot_y, pf_col_w, pf_h_dv, "Dadi Vita", 7.5)
    c.setFont("Helvetica", 6.5); c.setFillColor(ACCENT)
    c.drawString(M+4, bot_y+pf_h_dv-22, "Totale:")
    iline(c, M+30, bot_y+pf_h_dv-20, pf_col_w-34)
    c.drawString(M+4, bot_y+pf_h_dv-36, "Tipo:")
    iline(c, M+24, bot_y+pf_h_dv-34, pf_col_w-28)

    # 3 rows of 5 dots below Tipo, centred in remaining space
    dot_r        = 4
    dot_cols     = 4
    dot_rows     = 4
    dot_margin   = 16
    dot_x_gap    = (pf_col_w - dot_margin * 2) / (dot_cols - 1)
    dot_y_gap    = 10
    space_top    = bot_y + pf_h_dv - 46
    space_bot    = bot_y + 14
    grid_h       = (dot_rows - 1) * dot_y_gap
    dot_y_start  = (space_top + space_bot) / 2 + grid_h / 2
    for row in range(dot_rows):
        dy = dot_y_start - row * dot_y_gap
        for col in range(dot_cols):
            dx = M + dot_margin + col * dot_x_gap
            c.setFillColor(FILL_BG); c.setStrokeColor(BORDER); c.setLineWidth(0.8)
            c.circle(dx, dy, dot_r, fill=1, stroke=1)
    c.setFillColor(INK)

    # ── P. Ferita (top, larger) ──────────────────────────────────────────────
    pf_y2 = bot_y + pf_h_dv + 6
    fancy_box(c, M, pf_y2, pf_col_w, pf_h_pf, "P. Ferita", 7.5)

    # Massimo: small label + short line at the top
    c.setFont("Helvetica", 6.5); c.setFillColor(ACCENT)
    c.drawString(M+5, pf_y2+pf_h_pf-32, "Massimo:")
    iline(c, M+38, pf_y2+pf_h_pf-30, pf_col_w-43)

    # Attuale + Temporanei: stacked vertically, full column width
    box_w       = pf_col_w - 10
    box_h       = 40
    box_x       = M + 5
    lbl_h       = 9
    gap_lbl_box = 3
    gap_boxes   = 10

    region_top = pf_y2 + pf_h_pf - 40
    region_bot = pf_y2 + 8
    content_h  = lbl_h + gap_lbl_box + box_h + gap_boxes + lbl_h + gap_lbl_box + box_h
    pad        = (region_top - region_bot - content_h) / 2

    att_lbl_y = region_top - pad - lbl_h
    att_box_y = att_lbl_y - gap_lbl_box - box_h
    tmp_lbl_y = att_box_y - gap_boxes - lbl_h
    tmp_box_y = tmp_lbl_y - gap_lbl_box - box_h

    c.setFont("Helvetica", 6); c.setFillColor(ACCENT)
    c.drawCentredString(box_x + box_w/2, att_lbl_y, "Attuali")
    c.drawCentredString(box_x + box_w/2, tmp_lbl_y, "Temporanei")

    # Attuale: solid, prominent (stat-block style)
    c.setFillColor(PARCHMENT_DK); c.setStrokeColor(BORDER); c.setLineWidth(1.5)
    c.roundRect(box_x, att_box_y, box_w, box_h, 3, fill=1, stroke=1)
    c.setFillColor(FILL_BG); c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.4)
    c.roundRect(box_x+3, att_box_y+3, box_w-6, box_h-6, 2, fill=1, stroke=1)

    # Temporanei: faded palette + dashed border
    c.setFillColor(FILL_BG); c.setStrokeColor(LIGHT_LINE); c.setLineWidth(1.0)
    c.setDash(3, 2)
    c.roundRect(box_x, tmp_box_y, box_w, box_h, 3, fill=1, stroke=1)
    c.setDash()
    c.setStrokeColor(colors.HexColor('#ddd0b0')); c.setLineWidth(0.3)
    c.setDash(2, 2)
    c.roundRect(box_x+3, tmp_box_y+3, box_w-6, box_h-6, 2, fill=0, stroke=1)
    c.setDash()

    c.setFillColor(INK)

    # Conio (shrunk to make room for XP below)
    conio_x = M + pf_col_w + 8
    conio_w = 72
    xp_h    = 62
    xp_gap  = 6
    conio_y = bot_y + xp_h + xp_gap
    conio_h = bot_h - xp_h - xp_gap
    fancy_box(c, conio_x, conio_y, conio_w, conio_h, "Conio", 7.5)

    # Totale conio value box
    cv_w, cv_h = conio_w - 20, 20
    cv_x = conio_x + 10
    cv_y = conio_y + conio_h - 18 - cv_h
    c.setFont("Helvetica", 6); c.setFillColor(ACCENT)
    c.drawCentredString(conio_x + conio_w/2, cv_y + cv_h + 3, "Totale")
    c.setFillColor(PARCHMENT_DK); c.setStrokeColor(BORDER); c.setLineWidth(1.2)
    c.roundRect(cv_x, cv_y, cv_w, cv_h, 2, fill=1, stroke=1)
    c.setFillColor(FILL_BG); c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.4)
    c.roundRect(cv_x+2, cv_y+2, cv_w-4, cv_h-4, 1, fill=1, stroke=1)

    # Coin rows with generous write boxes
    coins = [("MO","Oro"),("MA","Argento"),("MR","Rame"),("MB","Bronzo")]
    coin_top   = cv_y - 8
    coin_bot   = conio_y + 8
    coin_gap   = (coin_top - coin_bot) / len(coins)
    wb_h       = max(16, coin_gap - 13)

    for ci, (code, name) in enumerate(coins):
        area_top = coin_top - ci * coin_gap
        lbl_y    = area_top - 9
        wb_y     = lbl_y - 3 - wb_h
        c.setFont("Helvetica-Bold", 6.5); c.setFillColor(BORDER)
        c.drawString(conio_x+5, lbl_y, code)
        c.setFont("Helvetica-Oblique", 5.5); c.setFillColor(ACCENT)
        c.drawString(conio_x+22, lbl_y, name)
        c.setFillColor(FILL_BG); c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.8)
        c.roundRect(conio_x+5, wb_y, conio_w-10, wb_h, 2, fill=1, stroke=1)

    # XP (under Conio): "Livello ___" on top, XP write box below
    fancy_box(c, conio_x, bot_y, conio_w, xp_h, "XP", 7.5)
    c.setFont("Helvetica", 6.5); c.setFillColor(ACCENT)
    lvl_y = bot_y + xp_h - 22
    c.drawString(conio_x + 5, lvl_y, "Livello")
    iline(c, conio_x + 28, lvl_y - 1, conio_w - 33)
    xp_box_x = conio_x + 5
    xp_box_w = conio_w - 10
    xp_box_h = 32
    xp_box_y = bot_y + 4
    c.setFillColor(PARCHMENT_DK); c.setStrokeColor(BORDER); c.setLineWidth(1.2)
    c.roundRect(xp_box_x, xp_box_y, xp_box_w, xp_box_h, 2, fill=1, stroke=1)
    c.setFillColor(FILL_BG); c.setStrokeColor(LIGHT_LINE); c.setLineWidth(0.4)
    c.roundRect(xp_box_x+2, xp_box_y+2, xp_box_w-4, xp_box_h-4, 1, fill=1, stroke=1)
    c.setFillColor(INK)

    # Equipaggiamento (fills rest, 2 columns)
    equip_x = conio_x + conio_w + 8
    equip_w = W - equip_x - M
    fancy_box(c, equip_x, bot_y, equip_w, bot_h, "Equipaggiamento", 7.5)
    col_gap  = 8
    col_w    = (equip_w - 10 - col_gap) / 2
    lines_eq = max(3, int((bot_h-20)//12))
    for col in range(2):
        cx = equip_x + 5 + col * (col_w + col_gap)
        for li in range(lines_eq):
            iline(c, cx, bot_y+bot_h-22-li*12, col_w)

    # footer
    c.setFont("Helvetica-Oblique", 5.5); c.setFillColor(LIGHT_LINE)
    c.drawCentredString(W/2, 12, "✦  Historia  ✦")

    c.save()
    print(f"Done → {out_path}")

build()

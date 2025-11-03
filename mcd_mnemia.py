import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.lines as mlines

def draw_table(ax, x, y, w, h, title, fields):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, linewidth=2))
    ax.text(x + w/2, y + h - 0.12, title, ha='center', va='top',
            fontsize=13, fontweight='bold')
    ax.text(x + 0.14, y + h - 0.42, "\n".join(fields),
            ha='left', va='top', fontsize=11)
    return (x, y, w, h)

def connect_h(ax, p1, p2, label, left_card, right_card):
    x1, y1, w1, h1 = p1; x2, y2, w2, h2 = p2
    x1c, y1c = x1 + w1, y1 + h1/2
    x2c, y2c = x2, y2 + h2/2
    ax.add_line(mlines.Line2D([x1c, x2c], [y1c, y2c], lw=1.8, color='black'))
    ax.text((x1c + x2c)/2, (y1c + y2c)/2 + 0.12, label, fontsize=11, ha='center')
    ax.text(x1c - 0.1, y1c + 0.1, left_card, fontsize=11, ha='right')
    ax.text(x2c + 0.1, y2c + 0.1, right_card, fontsize=11, ha='left')

def connect_v(ax, p1, p2, label, top_card, bottom_card):
    x1, y1, w1, h1 = p1; x2, y2, w2, h2 = p2
    x1c, y1c = x1 + w1/2, y1
    x2c, y2c = x2 + w2/2, y2 + h2
    ax.add_line(mlines.Line2D([x1c, x2c], [y1c, y2c], lw=1.8, color='black'))
    ax.text((x1c + x2c)/2 + 0.12, (y1c + y2c)/2, label, fontsize=11, ha='left')
    ax.text(x1c, y1c + 0.1, top_card, fontsize=11, ha='center', va='bottom')
    ax.text(x2c, y2c - 0.1, bottom_card, fontsize=11, ha='center', va='top')

# Canvas
fig, ax = plt.subplots(figsize=(15, 10))
ax.axis('off')

# Tables
cat = draw_table(ax, 0.5, 6.5, 3.8, 1.7, "CATEGORY", [
    "id_category (PK)",
    "name (ex. position_du_corps,",
    "      partie_du_corps,",
    "      vitesse_d_execution)"
])
con = draw_table(ax, 5.2, 6.5, 3.8, 1.7, "CONSTRAINT", [
    "id_constraint (PK)",
    "category_id (FK → CATEGORY)",
    "label (ex. assis, bras, lent)"
])
mov = draw_table(ax, 5.2, 4.0, 3.8, 1.7, "MOVEMENT", [
    "id_movement (PK)",
    "label (A, B, C)"
])
mch = draw_table(ax, 9.6, 3.8, 4.2, 2.2, "MOVEMENT_CHOICES", [
    "id_choice (PK)",
    "movement_id (FK → MOVEMENT)",
    "category_id (FK → CATEGORY)",
    "constraint_id (FK → CONSTRAINT)",
    "UNIQUE(movement_id, category_id)"
])
insp = draw_table(ax, 0.5, 1.8, 3.8, 1.6, "POETIC_INSPIRATION", [
    "id_poetic_inspiration (PK)",
    "label, source, created_at"
])
phr = draw_table(ax, 5.2, 1.8, 3.8, 1.6, "CHOREOGRAPHIC_PHRASE", [
    "id_choreographic_phrase (PK)",
    "label (ex. CM1 – Séquence 1 (Brume))",
    "poetic_inspiration_id (FK → POETIC_INSPIRATION)"
])
pause = draw_table(ax, 9.6, 2.0, 3.8, 1.4, "PAUSE", [
    "id_pause (PK)",
    "label (aucune, courte, longue)"
])
step = draw_table(ax, 5.2, -0.4, 3.8, 2.2, "CHOREOGRAPHIC_STEP", [
    "id_step (PK)",
    "choreographic_phrase_id (FK → CHOREOGRAPHIC_PHRASE)",
    "order_idx (1,2,3,...)",
    "movement_id (FK → MOVEMENT, nullable)",
    "pause_id (FK → PAUSE, nullable)",
    "CHECK XOR movement/pause",
    "UNIQUE(choreographic_phrase_id, order_idx)"
])

# Relations
connect_h(ax, cat, con, "regroupe / contient", "1", "N")
connect_h(ax, con, mch, "peut être choisie dans", "1", "N")
connect_h(ax, cat, mch, "désigne la famille de", "1", "N")
connect_h(ax, mov, mch, "est composé de (1 par catégorie)", "1", "N")
connect_h(ax, insp, phr, "inspire", "1", "N")
connect_v(ax, phr, step, "se compose de (étapes ordonnées)", "1", "N")
connect_h(ax, step, mov, "référence (étape = mouvement)", "N", "1")
connect_h(ax, step, pause, "insère (étape = pause)", "N", "1")

plt.title("MnémIA — MCDal", fontsize=15, pad=20)
plt.tight_layout()
plt.savefig("MCD_MnemIA_final.png", dpi=300, bbox_inches='tight')
print("✅ Diagramme généré : MCD_MnemIA_final.png")

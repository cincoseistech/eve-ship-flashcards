import streamlit as st
import pandas as pd
import random
import json
import os

# --- Page Config ---
st.set_page_config(
    page_title="EVE Ship Flashcards",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Clean up general spacing */
    .block-container { padding-top: 2rem; }

    /* Card container */
    .card-container {
        background: #1a1a2e;
        border: 1px solid #30305a;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .card-label {
        color: #888;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    .card-field {
        font-size: 1rem;
        margin: 0.3rem 0;
        color: #e0e0e0;
    }
    .card-field-label {
        color: #7a7aad;
    }
    .card-field-value {
        color: #ffffff;
        font-weight: 600;
    }

    /* Score bar */
    .score-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 1rem;
        background: #12121f;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #ccc;
    }
    .score-correct { color: #4caf50; font-weight: 600; }
    .score-wrong { color: #f44336; font-weight: 600; }

    /* Button row styling */
    .stButton > button {
        width: 100%;
        border-radius: 6px;
    }

    /* Sidebar section headers */
    .sidebar-section {
        font-size: 0.8rem;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1rem;
        margin-bottom: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

PRESETS_FILE = "flashcard_presets.json"

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_excel("eve_ships_complete.xlsx")
    return df

df = load_data()

AVAILABLE_COLS = [c for c in df.columns if c != 'typeID']
all_classes = sorted(df['groupName'].dropna().unique().tolist())

# --- Built-in Presets ---
BUILTIN_PRESETS = {
    "Visual ID — Image to Name": {
        "show_image_front": True,
        "front_fields": [],
        "show_image_back": False,
        "back_fields": ["typeName", "groupName"],
        "ship_classes": "__all__",
        "res_as_percent": True,
        "builtin": True
    },
    "Name ID — Name to Image": {
        "show_image_front": False,
        "front_fields": ["typeName"],
        "show_image_back": True,
        "back_fields": ["groupName"],
        "ship_classes": "__all__",
        "res_as_percent": True,
        "builtin": True
    },
    "Fitting Knowledge — Name to Slots": {
        "show_image_front": False,
        "front_fields": ["typeName", "groupName"],
        "show_image_back": False,
        "back_fields": ["High Slots", "Medium Slots", "Low Slots",
                        "Turret Hardpoints", "Launcher Hardpoints",
                        "Rig Slots", "Calibration",
                        "Drone Bandwidth", "Drone Capacity"],
        "ship_classes": "__all__",
        "res_as_percent": True,
        "builtin": True
    },
    "Full Profile — Image to Stats": {
        "show_image_front": True,
        "front_fields": [],
        "show_image_back": False,
        "back_fields": ["typeName", "groupName",
                        "Structure Hitpoints", "Armor Hitpoints", "Shield Capacity",
                        "Powergrid Output", "CPU Output",
                        "High Slots", "Medium Slots", "Low Slots",
                        "Turret Hardpoints", "Launcher Hardpoints",
                        "Maximum Velocity", "Signature Radius",
                        "Drone Bandwidth", "Drone Capacity"],
        "ship_classes": "__all__",
        "res_as_percent": True,
        "builtin": True
    },
    "Tank Profile — Name to Resists": {
        "show_image_front": False,
        "front_fields": ["typeName", "groupName"],
        "show_image_back": False,
        "back_fields": ["Structure Hitpoints", "Armor Hitpoints", "Shield Capacity",
                        "Shield EM Damage Resistance", "Shield Thermal Damage Resistance",
                        "Shield Kinetic Damage Resistance", "Shield Explosive Damage Resistance",
                        "Armor EM Damage Resistance", "Armor Thermal Damage Resistance",
                        "Armor Kinetic Damage Resistance", "Armor Explosive Damage Resistance"],
        "ship_classes": "__all__",
        "res_as_percent": True,
        "builtin": True
    },
    "Navigation — Name to Movement": {
        "show_image_front": False,
        "front_fields": ["typeName", "groupName"],
        "show_image_back": False,
        "back_fields": ["Maximum Velocity", "Inertia Modifier",
                        "Ship Warp Speed", "Warp Speed Multiplier",
                        "Signature Radius", "mass"],
        "ship_classes": "__all__",
        "res_as_percent": True,
        "builtin": True
    },
    "Electronic Warfare — Name to Sensors": {
        "show_image_front": False,
        "front_fields": ["typeName", "groupName"],
        "show_image_back": False,
        "back_fields": ["Scan Resolution", "Maximum Targeting Range",
                        "Maximum Locked Targets", "Signature Radius",
                        "Gravimetric Sensor Strength", "Ladar Sensor Strength",
                        "Magnetometric Sensor Strength", "RADAR Sensor Strength",
                        "ECM Resistance", "Sensor Warfare Resistance"],
        "ship_classes": "__all__",
        "res_as_percent": True,
        "builtin": True
    },
    "Quick ID — Image to Class and Slots": {
        "show_image_front": True,
        "front_fields": [],
        "show_image_back": False,
        "back_fields": ["typeName", "groupName", "marketGroupName",
                        "High Slots", "Medium Slots", "Low Slots",
                        "Turret Hardpoints", "Launcher Hardpoints"],
        "ship_classes": "__all__",
        "res_as_percent": True,
        "builtin": True
    },
}

# --- Preset Persistence ---
def load_custom_presets():
    if os.path.exists(PRESETS_FILE):
        with open(PRESETS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_custom_presets(presets):
    with open(PRESETS_FILE, 'w') as f:
        json.dump(presets, f, indent=2)

def get_all_presets():
    custom = load_custom_presets()
    combined = {}
    combined.update(BUILTIN_PRESETS)
    combined.update(custom)
    return combined

def safe_cols(col_list):
    return [c for c in col_list if c in AVAILABLE_COLS]

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.markdown("## Flashcard Configuration")

# --- Presets ---
st.sidebar.markdown('<div class="sidebar-section">Presets</div>', unsafe_allow_html=True)

all_presets = get_all_presets()
preset_names = ["Manual"] + list(all_presets.keys())
selected_preset = st.sidebar.selectbox("Active Preset", options=preset_names, label_visibility="collapsed")

if selected_preset != "Manual" and selected_preset in all_presets:
    if st.sidebar.button("Apply Preset"):
        p = all_presets[selected_preset]
        st.session_state['_preset_applied'] = p
        st.rerun()

preset_data = st.session_state.pop('_preset_applied', None)

if preset_data:
    st.session_state['w_image_front'] = preset_data.get("show_image_front", True)
    st.session_state['w_image_back'] = preset_data.get("show_image_back", False)
    st.session_state['w_front_fields'] = safe_cols(preset_data.get("front_fields", []))
    st.session_state['w_back_fields'] = safe_cols(preset_data.get("back_fields", []))
    st.session_state['w_res_percent'] = preset_data.get("res_as_percent", True)
    if preset_data.get("ship_classes") == "__all__":
        st.session_state['w_ship_classes'] = all_classes
    else:
        st.session_state['w_ship_classes'] = [c for c in preset_data.get("ship_classes", all_classes) if c in all_classes]
    st.session_state.card_index = 0
    st.session_state.flipped = False
    st.rerun()

st.sidebar.markdown("---")

# --- Ship Classes ---
st.sidebar.markdown('<div class="sidebar-section">Ship Classes</div>', unsafe_allow_html=True)
selected_classes = st.sidebar.multiselect(
    "Ship Classes",
    options=all_classes,
    default=st.session_state.get('w_ship_classes', all_classes),
    key='w_ship_classes',
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# --- Front ---
st.sidebar.markdown('<div class="sidebar-section">Front of Card</div>', unsafe_allow_html=True)
show_image_front = st.sidebar.checkbox(
    "Show ship image",
    value=st.session_state.get('w_image_front', True),
    key='w_image_front'
)
front_fields = st.sidebar.multiselect(
    "Front data fields",
    options=AVAILABLE_COLS,
    default=st.session_state.get('w_front_fields', safe_cols(['typeName'])),
    key='w_front_fields',
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# --- Back ---
st.sidebar.markdown('<div class="sidebar-section">Back of Card</div>', unsafe_allow_html=True)
show_image_back = st.sidebar.checkbox(
    "Show ship image",
    value=st.session_state.get('w_image_back', False),
    key='w_image_back'
)
back_fields = st.sidebar.multiselect(
    "Back data fields",
    options=AVAILABLE_COLS,
    default=st.session_state.get('w_back_fields', safe_cols(['groupName'])),
    key='w_back_fields',
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# --- Options ---
st.sidebar.markdown('<div class="sidebar-section">Display Options</div>', unsafe_allow_html=True)
res_as_percent = st.sidebar.checkbox(
    "Show resistances as percentages",
    value=st.session_state.get('w_res_percent', True),
    key='w_res_percent'
)

st.sidebar.markdown("---")

# --- Save Preset ---
st.sidebar.markdown('<div class="sidebar-section">Save Current Configuration</div>', unsafe_allow_html=True)
new_preset_name = st.sidebar.text_input("Preset name", placeholder="e.g. Frigate Visual Drill", label_visibility="collapsed")
if st.sidebar.button("Save Preset"):
    if new_preset_name.strip():
        custom = load_custom_presets()
        custom[new_preset_name.strip()] = {
            "show_image_front": show_image_front,
            "front_fields": front_fields,
            "show_image_back": show_image_back,
            "back_fields": back_fields,
            "ship_classes": selected_classes if set(selected_classes) != set(all_classes) else "__all__",
            "res_as_percent": res_as_percent,
            "builtin": False
        }
        save_custom_presets(custom)
        st.sidebar.success(f"Saved: {new_preset_name.strip()}")
        st.rerun()
    else:
        st.sidebar.error("Enter a preset name.")

# --- Delete Preset ---
custom_presets = load_custom_presets()
if custom_presets:
    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="sidebar-section">Delete Custom Preset</div>', unsafe_allow_html=True)
    del_target = st.sidebar.selectbox("Select preset", options=list(custom_presets.keys()),
                                       key='del_preset_select', label_visibility="collapsed")
    if st.sidebar.button("Delete Preset"):
        custom_presets.pop(del_target, None)
        save_custom_presets(custom_presets)
        st.sidebar.success(f"Deleted: {del_target}")
        st.rerun()

# --- Debug ---
with st.sidebar.expander("Column Reference"):
    st.write(AVAILABLE_COLS)

# =====================================================
# MAIN CONTENT
# =====================================================

filtered_df = df[df['groupName'].isin(selected_classes)].reset_index(drop=True)

if len(filtered_df) == 0:
    st.warning("No ships match your current filter. Adjust ship classes in the sidebar.")
    st.stop()

# --- Session State ---
if 'card_index' not in st.session_state:
    st.session_state.card_index = 0
if 'flipped' not in st.session_state:
    st.session_state.flipped = False
if 'deck_order' not in st.session_state:
    st.session_state.deck_order = list(range(len(filtered_df)))
if 'score_correct' not in st.session_state:
    st.session_state.score_correct = 0
if 'score_wrong' not in st.session_state:
    st.session_state.score_wrong = 0
if 'last_filter_hash' not in st.session_state:
    st.session_state.last_filter_hash = None

filter_hash = hash(tuple(selected_classes))
if st.session_state.last_filter_hash != filter_hash:
    st.session_state.deck_order = list(range(len(filtered_df)))
    st.session_state.card_index = 0
    st.session_state.flipped = False
    st.session_state.last_filter_hash = filter_hash

# Clamp index
max_idx = len(st.session_state.deck_order) - 1
if st.session_state.card_index > max_idx:
    st.session_state.card_index = max_idx

# --- Header ---
st.markdown("## EVE Online — Ship Flashcards")

# Score and position bar
card_num = st.session_state.card_index + 1
total = len(filtered_df)
correct = st.session_state.score_correct
wrong = st.session_state.score_wrong

st.markdown(
    f'<div class="score-bar">'
    f'<span>Card {card_num} of {total}</span>'
    f'<span><span class="score-correct">{correct} correct</span>'
    f'&nbsp;&nbsp;/&nbsp;&nbsp;'
    f'<span class="score-wrong">{wrong} missed</span></span>'
    f'</div>',
    unsafe_allow_html=True
)

# --- Deck Controls ---
col_shuf, col_reset = st.columns(2)
with col_shuf:
    if st.button("Shuffle Deck"):
        st.session_state.deck_order = list(range(len(filtered_df)))
        random.shuffle(st.session_state.deck_order)
        st.session_state.card_index = 0
        st.session_state.flipped = False
        st.rerun()
with col_reset:
    if st.button("Reset Score"):
        st.session_state.score_correct = 0
        st.session_state.score_wrong = 0
        st.rerun()

# --- Current Ship ---
idx = st.session_state.deck_order[st.session_state.card_index]
ship = filtered_df.iloc[idx]
type_id = int(ship['typeID'])
image_url = f"https://images.evetech.net/types/{type_id}/render?size=512"

# --- Value Formatting ---
def format_value(col, val):
    if pd.isna(val):
        return "—"
    if res_as_percent and 'Damage Resistance' in col:
        if isinstance(val, (int, float)) and 0 <= val <= 1:
            return f"{(1 - val) * 100:.1f}%"
        elif isinstance(val, (int, float)):
            return f"{val:.1f}%"
    if isinstance(val, float):
        if val == int(val):
            return f"{int(val):,}"
        return f"{val:,.2f}"
    return str(val)

# --- Render Card ---
def render_card(fields, show_image, side_label):
    st.markdown(
        f'<div class="card-container">'
        f'<div class="card-label">{side_label}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    # Streamlit can't nest widgets inside raw HTML, so we render below the label
    # Re-do with pure streamlit for image + fields inside a visual block

    # Actually render with streamlit components
    pass

# Using streamlit containers for clean card look
st.markdown("---")

side_label = "FRONT" if not st.session_state.flipped else "BACK"
active_fields = front_fields if not st.session_state.flipped else back_fields
active_image = show_image_front if not st.session_state.flipped else show_image_back

st.caption(side_label)

if active_image:
    col_img_l, col_img_c, col_img_r = st.columns([1, 3, 1])
    with col_img_c:
        st.image(image_url, use_container_width=True)

if active_fields:
    for col in active_fields:
        val = ship.get(col, "—")
        display_val = format_value(col, val)
        st.markdown(f"**{col}:** &nbsp; {display_val}", unsafe_allow_html=True)
elif not active_image:
    st.info("No fields or image selected for this side. Configure in the sidebar.")

st.markdown("---")

# --- Navigation ---
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("Previous", use_container_width=True):
        st.session_state.card_index = max(0, st.session_state.card_index - 1)
        st.session_state.flipped = False
        st.rerun()

with c2:
    if st.button("Flip Card", use_container_width=True):
        st.session_state.flipped = not st.session_state.flipped
        st.rerun()

with c3:
    if st.button("Next", use_container_width=True):
        st.session_state.card_index = min(max_idx, st.session_state.card_index + 1)
        st.session_state.flipped = False
        st.rerun()

with c4:
    if st.button("Correct", use_container_width=True):
        st.session_state.score_correct += 1
        st.session_state.card_index = min(max_idx, st.session_state.card_index + 1)
        st.session_state.flipped = False
        st.rerun()

with c5:
    if st.button("Missed", use_container_width=True):
        st.session_state.score_wrong += 1
        st.session_state.card_index = min(max_idx, st.session_state.card_index + 1)
        st.session_state.flipped = False
        st.rerun()

# --- Footer ---
st.markdown("---")
st.caption("Configure card sides and ship filters using the sidebar. Save configurations as presets for quick access.")

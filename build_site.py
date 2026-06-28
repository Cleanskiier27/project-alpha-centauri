import os
import re

# Source configurations
root = "docs/centauri"
master_doc_md = "docs/Centauri_Master_Document.md"
output_dir = "_site"

# Define the chapters list
sections = {
    "A_Origin_Vector": [
        "CIS-A1-PDM_Problem_Definition_Matrix.md",
        "CIS-A2-SFS_Scientific_Foundations_Scan.md",
        "CIS-A3-CHS_Concept_Hypothesis_Sheet.md",
        "CIS-A4-FEM_Feasibility_Envelope_Model.md",
        "CIS-A5-UID_Umbrella_Integration_Draft.md",
    ],
    "B_Seed_Vector": [
        "CIS-B1-PAB_Preliminary_Architecture_Blueprint.md",
        "CIS-B2-MBL_Mirror_Base_Lattice_Map.md",
        "CIS-B3-A0R_Prototype_Alpha0_Report.md",
        "CIS-B4-RFMA_Risk_Failure_Mode_Atlas.md",
        "CIS-B5-SP1G_SBIR_Phase1_Readiness_Gate.md",
    ],
    "C_Ignition_Vector": [
        "CIS-C1-P1WA_Phase1_Workplan_Activation.md",
        "CIS-C2-A1R_Prototype_Alpha1_Report.md",
        "CIS-C3-EVL_Experimental_Validation_Log.md",
        "CIS-C4-MID_Mission_Interface_Draft.md",
        "CIS-C5-P1CA_Phase1_Closeout_TRL_Audit.md",
    ],
    "D_Ascent_Vector": [
        "CIS-D1-P2SEP_Phase2_Systems_Engineering_Plan.md",
        "CIS-D2-B0R_Prototype_Beta0_Report.md",
        "CIS-D3-PGMIS_Pass_Glass_Morphism_Integration_Spec.md",
        "CIS-D4-EQP_Environmental_Qualification_Pathway.md",
        "CIS-D5-MOSTL_Mission_Ops_Simulation_Trial_Log.md",
    ],
    "E_Orbit_Vector": [
        "CIS-E1-B1R_Prototype_Beta1_Report.md",
        "CIS-E2-EILM_Extended_Infrastructure_Layer_Map.md",
        "CIS-E3-MSSTR_Mission_Scenario_Stress_Test_Report.md",
        "CIS-E4-LORR1_Lunar_Ops_Readiness_Review.md",
        "CIS-E5-CVD_Commercialization_Vector_Draft.md",
    ],
    "F_Translunar_Vector": [
        "CIS-F1-G0R_Prototype_Gamma0_Report.md",
        "CIS-F2-MICP_Mission_Integration_Certification_Packet.md",
        "CIS-F3-ODI_Operational_Deployment_Index.md",
        "CIS-F4-CSE_Commercialization_Scaling_Engine.md",
        "CIS-F5-CAR_Centauri_Apex_Review.md",
    ],
}

# Collect linear order of all chapters for next/prev navigation
flat_chapters = []
for sec, files in sections.items():
    sec_name = sec.replace("_", " ")
    for f in files:
        name_part = f.replace(".md", "")
        parts = name_part.split("_", 1)
        doc_code = parts[0]
        doc_title = parts[1].replace("_", " ")
        flat_chapters.append({
            "section_key": sec,
            "section_name": sec_name,
            "filename": f,
            "code": doc_code,
            "title": doc_title,
            "html_filename": f"{doc_code}.html"
        })

# Simple Markdown to HTML parser
def md_to_html(md_text):
    html = []
    lines = md_text.splitlines()
    in_list = False
    in_num_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # Lists closing check
        if not stripped.startswith("- ") and not stripped.startswith("* ") and not re.match(r'^\d+\.', stripped):
            if in_list:
                html.append("</ul>")
                in_list = False
            if in_num_list:
                html.append("</ol>")
                in_num_list = False

        if not stripped:
            html.append("<br>")
            continue

        # Headers
        if stripped.startswith("# "):
            html.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped.startswith("## "):
            html.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("### "):
            html.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("#### "):
            html.append(f"<h4>{stripped[5:]}</h4>")
        
        # Horizontal rule
        elif stripped == "---":
            html.append("<hr>")
            
        # Bullet list items
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            content = stripped[2:]
            # Process inline strong/emphasis
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
            html.append(f"<li>{content}</li>")
            
        # Numbered list items
        elif re.match(r'^\d+\.', stripped):
            if not in_num_list:
                html.append("<ol>")
                in_num_list = True
            content = re.sub(r'^\d+\.\s*', '', stripped)
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
            html.append(f"<li>{content}</li>")
            
        # Regular paragraph
        else:
            # Inline replacements
            content = stripped
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
            
            # Key-value metadata formatting
            if re.match(r'^<strong>Document ID:</strong>', content) or \
               re.match(r'^<strong>CIS Layer:</strong>', content) or \
               re.match(r'^<strong>Centauri Phase:</strong>', content) or \
               re.match(r'^<strong>TRL Target:</strong>', content) or \
               re.match(r'^<strong>Grid Slot:</strong>', content) or \
               re.match(r'^<strong>PRECISELIENS Node:</strong>', content):
                html.append(f"<div class='metadata-item'>{content}</div>")
            else:
                html.append(f"<p>{content}</p>")
                
    # Close any open lists at the end
    if in_list:
        html.append("</ul>")
    if in_num_list:
        html.append("</ol>")
        
    return "\n".join(html)

# CSS design tokens common to all pages
CSS_COMMON = """
:root {
  --bg: #030510;
  --surface: rgba(255, 255, 255, 0.03);
  --surface-hover: rgba(255, 255, 255, 0.06);
  --border: rgba(255, 255, 255, 0.08);
  --primary: #00c6ff;
  --secondary: #7b2fff;
  --accent: #ff6b35;
  --text: #e8eaf6;
  --muted: rgba(232, 234, 246, 0.5);
  --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}
* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior: smooth; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Outfit', sans-serif;
  min-height: 100vh;
  background-image:
    radial-gradient(ellipse at 10% 20%, rgba(0,198,255,0.06) 0%, transparent 55%),
    radial-gradient(ellipse at 90% 80%, rgba(123,47,255,0.06) 0%, transparent 55%);
}
body::before {
  content:'';
  position:fixed;
  inset:0;
  background-image:
    radial-gradient(1px 1px at 15% 15%, rgba(255,255,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 45% 65%, rgba(255,255,255,0.2) 0%, transparent 100%),
    radial-gradient(1px 1px at 75% 25%, rgba(255,255,255,0.25) 0%, transparent 100%),
    radial-gradient(1px 1px at 85% 85%, rgba(255,255,255,0.2) 0%, transparent 100%);
  pointer-events: none;
  z-index: 0;
}
nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 18px 8%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(20px);
  background: rgba(3,5,16,0.85);
  border-bottom: 1px solid var(--border);
}
.nav-logo {
  font-weight: 900;
  font-size: 1.15rem;
  letter-spacing: 3px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-transform: uppercase;
  text-decoration: none;
}
.nav-links { display:flex; gap:30px; }
.nav-links a {
  color: var(--muted);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: color 0.2s;
}
.nav-links a:hover { color: var(--primary); }

.container {
  max-width: 1000px;
  margin: 120px auto 80px;
  padding: 0 4%;
  position: relative;
  z-index: 1;
}

/* Typography styles inside content */
h1 { font-size: 2.5rem; font-weight: 800; margin-bottom: 24px; color: #fff; }
h2 { font-size: 1.6rem; font-weight: 700; margin: 40px 0 20px; color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: 8px; }
h3 { font-size: 1.25rem; font-weight: 600; margin: 30px 0 15px; color: #fff; }
p { font-size: 1rem; color: var(--text); line-height: 1.7; margin-bottom: 16px; opacity: 0.9; }
ul, ol { margin-left: 20px; margin-bottom: 24px; }
li { font-size: 0.95rem; line-height: 1.7; margin-bottom: 8px; color: var(--text); opacity: 0.9; }
hr { border: none; border-top: 1px solid var(--border); margin: 30px 0; }
strong { color: #fff; }

/* Metadata styling */
.metadata-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 24px;
  border-radius: 16px;
  margin: 32px 0;
  backdrop-filter: blur(10px);
}
.metadata-item {
  font-family: 'Outfit', sans-serif;
  font-size: 0.9rem;
  color: var(--muted);
}
.metadata-item strong {
  color: var(--primary);
  font-weight: 500;
}

/* Nav controls */
.prev-next-nav {
  display: flex;
  justify-content: space-between;
  margin-top: 60px;
  padding-top: 30px;
  border-top: 1px solid var(--border);
  gap: 20px;
}
.nav-card {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 20px;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
}
.nav-card:hover {
  border-color: var(--primary);
  background: var(--surface-hover);
  transform: translateY(-2px);
}
.nav-card.prev { align-items: flex-start; }
.nav-card.next { align-items: flex-end; text-align: right; }
.nav-card-label { font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; color: var(--muted); margin-bottom: 6px; }
.nav-card-title { font-weight: 600; font-size: 0.95rem; color: #fff; }

/* Table of contents and layout */
.layout-with-sidebar {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 40px;
}
.sidebar {
  position: sticky;
  top: 120px;
  max-height: calc(100vh - 160px);
  overflow-y: auto;
  border-right: 1px solid var(--border);
  padding-right: 20px;
}
.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
.sidebar-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 16px;
  letter-spacing: 2px;
}
.sidebar-links { list-style: none; margin: 0; }
.sidebar-links li { margin-bottom: 8px; }
.sidebar-links a {
  text-decoration: none;
  font-size: 0.85rem;
  color: var(--muted);
  transition: color 0.2s;
  display: block;
  padding: 6px 8px;
  border-radius: 6px;
}
.sidebar-links a:hover, .sidebar-links a.active {
  color: var(--primary);
  background: var(--surface);
}
.vector-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 50px;
  font-size: 0.7rem;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
}
.vector-badge.a { background: rgba(0,198,255,0.15); color: var(--primary); border: 1px solid rgba(0,198,255,0.3); }
.vector-badge.b { background: rgba(123,47,255,0.15); color: #b388ff; border: 1px solid rgba(123,47,255,0.3); }
.vector-badge.c { background: rgba(255,107,53,0.15); color: var(--accent); border: 1px solid rgba(255,107,53,0.3); }
.vector-badge.d { background: rgba(0,230,118,0.15); color: #00e676; border: 1px solid rgba(0,230,118,0.3); }
.vector-badge.e { background: rgba(255,214,0,0.15); color: #ffd600; border: 1px solid rgba(255,214,0,0.3); }
.vector-badge.f { background: rgba(255,61,113,0.15); color: #ff3d71; border: 1px solid rgba(255,61,113,0.3); }

footer {
  border-top: 1px solid var(--border);
  padding: 40px 0;
  text-align: center;
  font-size: 0.8rem;
  color: var(--muted);
  margin-top: 80px;
}
"""

def generate_header(title, active_page=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Project Alpha Centauri</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>{CSS_COMMON}</style>
</head>
<body>
  <nav>
    <a href="../index.html" class="nav-logo">α Centauri</a>
    <div class="nav-links">
      <a href="../index.html#phases">Phases</a>
      <a href="../master_doc.html">Master Doc</a>
      <a href="https://github.com/Cleanskiier27/project-alpha-centauri">GitHub</a>
    </div>
  </nav>
  <div class="container">
"""

# Ensure outputs directories exist
os.makedirs(os.path.join(output_dir, "chapters"), exist_ok=True)

# Generate individual chapter pages
for idx, ch in enumerate(flat_chapters):
    # Read the markdown source
    filepath = os.path.join(root, ch["section_key"], ch["filename"])
    with open(filepath, "r", encoding="utf-8") as f_in:
        content = f_in.read()
    
    # Strip main title since we generate it in HTML wrapper
    content_clean = re.sub(r'^#\s+.*?\n', '', content)
    
    # Parse Metadata Section to put in beautiful Grid box
    metadata_items = []
    other_lines = []
    
    in_meta = True
    for line in content_clean.splitlines():
        if in_meta:
            if line.strip().startswith("---"):
                in_meta = False
                continue
            if line.strip():
                metadata_items.append(line)
        else:
            other_lines.append(line)
            
    parsed_meta = md_to_html("\n".join(metadata_items))
    parsed_body = md_to_html("\n".join(other_lines))
    
    # Navigation Cards
    nav_html = []
    nav_html.append("<div class='prev-next-nav'>")
    if idx > 0:
        prev_ch = flat_chapters[idx - 1]
        nav_html.append(f"""
          <a href="{prev_ch['code']}.html" class="nav-card prev">
            <span class="nav-card-label">← Previous Phase ({prev_ch['code']})</span>
            <span class="nav-card-title">{prev_ch['title']}</span>
          </a>
        """)
    else:
        nav_html.append("<div style='flex:1;'></div>")
        
    if idx < len(flat_chapters) - 1:
        next_ch = flat_chapters[idx + 1]
        nav_html.append(f"""
          <a href="{next_ch['code']}.html" class="nav-card next">
            <span class="nav-card-label">Next Phase ({next_ch['code']}) →</span>
            <span class="nav-card-title">{next_ch['title']}</span>
          </a>
        """)
    else:
        nav_html.append("<div style='flex:1;'></div>")
    nav_html.append("</div>")
    
    # Sidebar compilation
    sidebar_links = []
    for other_ch in flat_chapters:
        # Highlight active
        active_class = "class='active'" if other_ch["code"] == ch["code"] else ""
        sidebar_links.append(f"<li><a href='{other_ch['code']}.html' {active_class}>{other_ch['code']}: {other_ch['title']}</a></li>")
    
    vector_class = ch["section_key"][0].lower() # e.g. 'a', 'b', etc
    
    # Compile Page HTML
    page_html = []
    page_html.append(generate_header(f"{ch['code']} - {ch['title']}"))
    
    page_html.append(f"""
      <div class="layout-with-sidebar">
        <aside class="sidebar">
          <div class="sidebar-title">Pipeline Registry</div>
          <ul class="sidebar-links">
            {"".join(sidebar_links)}
          </ul>
        </aside>
        <main>
          <span class="vector-badge {vector_class}">{ch['section_name']}</span>
          <h1>{ch['title']}</h1>
          <div class="metadata-grid">
            {parsed_meta}
          </div>
          <div class="markdown-body">
            {parsed_body}
          </div>
          {"".join(nav_html)}
        </main>
      </div>
      <footer>
        PROJECT ALPHA CENTAURI &bull; CIS TECHNOLOGY MATURATION REGISTRY
      </footer>
    """)
    
    page_html.append("</div></body></html>")
    
    # Write file
    out_path = os.path.join(output_dir, "chapters", f"{ch['code']}.html")
    with open(out_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(page_html))

print(f"Generated {len(flat_chapters)} HTML artifact chapters.")

# Generate Master Document HTML with sidebar TOC
master_doc_body_md = ""
if os.path.exists(master_doc_md):
    with open(master_doc_md, "r", encoding="utf-8") as f_md:
        master_doc_body_md = f_md.read()
else:
    # Stitch on the fly if file doesn't exist
    print("Warning: Master MD not found. Generating body dynamically.")
    
# Clean up MD links and headings for Master Doc output
master_doc_body_html = md_to_html(master_doc_body_md)

# TOC for master document
master_toc = []
for sec, files in sections.items():
    sec_name = sec.replace("_", " ")
    sec_anchor = sec.lower()
    master_toc.append(f"<li style='margin-top: 12px; font-weight: 600;'><a href='#{sec_anchor}'>{sec_name}</a></li>")
    for f in files:
        name_part = f.replace(".md", "")
        parts = name_part.split("_", 1)
        doc_code = parts[0]
        doc_title = parts[1].replace("_", " ")
        anchor_title = name_part.lower().replace("_", "-").replace(" ", "-")
        master_toc.append(f"<li style='margin-left: 15px;'><a href='#{anchor_title}' style='font-size:0.8rem;'>{doc_code}: {doc_title}</a></li>")

master_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Centauri Master Document | CIS Framework</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    {CSS_COMMON}
    .layout-with-sidebar {{
      grid-template-columns: 320px 1fr;
    }}
    .sidebar {{
      max-height: calc(100vh - 160px);
    }}
    h1 {{ font-size: 2.8rem; line-height: 1.1; margin-bottom: 24px; background: linear-gradient(135deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .markdown-body h1 {{
      font-size: 2rem;
      margin-top: 60px;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 12px;
      color: #fff;
      -webkit-text-fill-color: initial;
      background: none;
    }}
    .markdown-body h2 {{
      font-size: 1.4rem;
      color: var(--primary);
    }}
  </style>
</head>
<body>
  <nav>
    <a href="index.html" class="nav-logo">α Centauri</a>
    <div class="nav-links">
      <a href="index.html#phases">Phases</a>
      <a href="master_doc.html" class="active">Master Doc</a>
      <a href="https://github.com/Cleanskiier27/project-alpha-centauri">GitHub</a>
    </div>
  </nav>
  <div class="container">
    <div class="layout-with-sidebar">
      <aside class="sidebar">
        <div class="sidebar-title">Master Document TOC</div>
        <ul class="sidebar-links">
          {"".join(master_toc)}
        </ul>
      </aside>
      <main class="markdown-body">
        {master_doc_body_html}
      </main>
    </div>
    <footer>
      PROJECT ALPHA CENTAURI &bull; CIS TECHNOLOGY MATURATION REGISTRY
    </footer>
  </div>
</body>
</html>
"""

with open(os.path.join(output_dir, "master_doc.html"), "w", encoding="utf-8") as f_out:
    f_out.write(master_html)

print("Generated master_doc.html")

# Generate index.html landing page with references updated to HTML files
# Let's dynamically output the landing page based on the structure of sections
landing_cards = []
for sec, files in sections.items():
    sec_name = sec.replace("_", " ")
    vector_class = sec[0].lower() # a, b, c, d, e, f
    
    # Select icon
    icons = {"a": "🔭", "b": "🌱", "c": "🔥", "d": "🚀", "e": "🛸", "f": "🌕"}
    icon = icons.get(vector_class, "🔭")
    
    # Retrieve phase target TRL/SBIR info
    phase_meta = {
        "a": {"trl": "TRL 1–2", "sbir": "Pre-Phase I"},
        "b": {"trl": "TRL 2–4", "sbir": "Phase I Entry"},
        "c": {"trl": "TRL 3–4", "sbir": "Phase I Execution"},
        "d": {"trl": "TRL 4–6", "sbir": "Phase II"},
        "e": {"trl": "TRL 6–7", "sbir": "Late Phase II"},
        "f": {"trl": "TRL 7–9", "sbir": "Phase III"}
    }
    meta = phase_meta.get(vector_class, {"trl": "", "sbir": ""})
    
    items_html = []
    for f in files:
        name_part = f.replace(".md", "")
        parts = name_part.split("_", 1)
        doc_code = parts[0]
        doc_title = parts[1].replace("_", " ")
        items_html.append(f"""
          <li>
            <span class="artifact-id">{doc_code}</span>
            <a href="chapters/{doc_code}.html" style="color:var(--muted); text-decoration:none; transition:color 0.2s;" onmouseover="this.style.color='#00c6ff'" onmouseout="this.style.color='var(--muted)'">{doc_title}</a>
          </li>
        """)
        
    landing_cards.append(f"""
      <div class="phase-card">
        <div class="phase-header">
          <div class="phase-icon {vector_class}">{icon}</div>
          <div>
            <div class="phase-name">{sec_name}</div>
            <div class="phase-trl">{meta['trl']} &bull; {meta['sbir']}</div>
          </div>
        </div>
        <ul class="phase-artifacts">
          {"".join(items_html)}
        </ul>
      </div>
    """)

index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Project Alpha Centauri | CIS Framework</title>
  <meta name="description" content="30-phase SBIR and TRL-aligned maturation pipeline for Project Alpha Centauri. NASA Artemis lunar technology development framework.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    {CSS_COMMON}
    
    /* Stars background animation */
    @keyframes starPulse {{
      0%, 100% {{ opacity: 0.3; }}
      50% {{ opacity: 1; }}
    }}
    
    /* Hero */
    .hero {{
      position: relative;
      z-index: 1;
      min-height: 80vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 120px 8% 80px;
    }}
    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 16px;
      border: 1px solid rgba(0,198,255,0.3);
      border-radius: 50px;
      font-size: 0.75rem;
      font-family: 'JetBrains Mono', monospace;
      color: var(--primary);
      margin-bottom: 32px;
      background: rgba(0,198,255,0.05);
      letter-spacing: 1px;
    }}
    .hero-badge::before {{ content:'◉'; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}

    h1 {{
      font-size: clamp(2.5rem, 7vw, 5.5rem);
      font-weight: 900;
      line-height: 1.05;
      letter-spacing: -1px;
      margin-bottom: 24px;
    }}
    .gradient-text {{
      background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .hero-sub {{
      font-size: 1.15rem;
      color: var(--muted);
      max-width: 600px;
      line-height: 1.7;
      margin-bottom: 48px;
    }}
    .hero-buttons {{ display:flex; gap:16px; flex-wrap:wrap; justify-content:center; }}
    .btn {{
      padding: 14px 32px;
      border-radius: 50px;
      font-size: 0.95rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.25s;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      color: #fff;
      box-shadow: 0 4px 24px rgba(0,198,255,0.3);
    }}
    .btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,198,255,0.4); }}
    .btn-outline {{
      border: 1px solid var(--border);
      color: var(--text);
      background: var(--surface);
    }}
    .btn-outline:hover {{ border-color: var(--primary); color: var(--primary); }}

    /* Stats bar */
    .stats-bar {{
      position: relative;
      z-index: 1;
      display: flex;
      justify-content: center;
      gap: 0;
      flex-wrap: wrap;
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      background: rgba(255,255,255,0.01);
      backdrop-filter: blur(10px);
    }}
    .stat {{
      padding: 28px 48px;
      text-align: center;
      border-right: 1px solid var(--border);
      flex: 1;
      min-width: 160px;
    }}
    .stat:last-child {{ border-right: none; }}
    .stat-num {{
      font-size: 2.2rem;
      font-weight: 900;
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-family: 'JetBrains Mono', monospace;
    }}
    .stat-label {{ font-size: 0.8rem; color: var(--muted); margin-top: 4px; letter-spacing: 1px; text-transform: uppercase; }}

    /* Sections */
    .section {{
      position: relative;
      z-index: 1;
      padding: 100px 8%;
      max-width: 1300px;
      margin: 0 auto;
    }}
    .section-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      color: var(--primary);
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-bottom: 16px;
    }}
    .section-title {{
      font-size: clamp(1.8rem, 4vw, 2.8rem);
      font-weight: 800;
      margin-bottom: 16px;
    }}
    .section-sub {{
      color: var(--muted);
      font-size: 1rem;
      line-height: 1.7;
      max-width: 560px;
      margin-bottom: 60px;
    }}

    /* Phase grid */
    .phases-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 20px;
    }}
    .phase-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px;
      transition: all 0.3s;
      position: relative;
      overflow: hidden;
      backdrop-filter: blur(10px);
    }}
    .phase-card::before {{
      content:'';
      position:absolute;
      inset:0;
      opacity:0;
      transition: opacity 0.3s;
      border-radius: 16px;
      background: radial-gradient(circle at top right, rgba(0, 198, 255, 0.05), transparent 60%);
      pointer-events: none;
    }}
    .phase-card:hover {{ transform: translateY(-4px); border-color: rgba(0,198,255,0.3); }}
    .phase-card:hover::before {{ opacity:1; }}
    .phase-header {{ display:flex; align-items:center; gap:14px; margin-bottom:20px; }}
    .phase-icon {{
      width: 44px; height: 44px;
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 1.2rem;
      flex-shrink: 0;
    }}
    .phase-icon.a {{ background: rgba(0,198,255,0.15); }}
    .phase-icon.b {{ background: rgba(123,47,255,0.15); }}
    .phase-icon.c {{ background: rgba(255,107,53,0.15); }}
    .phase-icon.d {{ background: rgba(0,230,118,0.15); }}
    .phase-icon.e {{ background: rgba(255,214,0,0.15); }}
    .phase-icon.f {{ background: rgba(255,61,113,0.15); }}
    .phase-name {{ font-weight: 700; font-size: 1.05rem; color: #fff; }}
    .phase-trl {{ font-size: 0.75rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; }}
    .phase-artifacts {{ list-style: none; }}
    .phase-artifacts li {{
      padding: 7px 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      font-size: 0.85rem;
      color: var(--muted);
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .phase-artifacts li:last-child {{ border-bottom: none; }}
    .phase-artifacts li::before {{ content:'→'; color: var(--primary); font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; }}
    .artifact-id {{ font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--primary); min-width: 85px; }}

    /* Master doc CTA */
    .master-doc-cta {{
      position: relative;
      z-index: 1;
      margin: 80px 8%;
      padding: 60px;
      border-radius: 24px;
      background: linear-gradient(135deg, rgba(0,198,255,0.08) 0%, rgba(123,47,255,0.08) 100%);
      border: 1px solid rgba(0,198,255,0.2);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 40px;
      flex-wrap: wrap;
      backdrop-filter: blur(15px);
    }}
    .master-doc-cta h2 {{ font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; color: #fff; }}
    .master-doc-cta p {{ color: var(--muted); font-size: 0.95rem; line-height: 1.6; max-width: 500px; }}

    /* Footer overrides */
    footer.main-footer {{
      border-top: 1px solid var(--border);
      padding: 40px 8%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-top: 80px;
    }}
    .footer-brand {{ font-weight: 700; font-size: 0.9rem; opacity: 0.6; }}
    .footer-links {{ display:flex; gap:24px; }}
    .footer-links a {{ color: var(--muted); text-decoration: none; font-size: 0.85rem; transition: color 0.2s; }}
    .footer-links a:hover {{ color: var(--primary); }}

    @media (max-width: 768px) {{
      .stat {{ padding: 20px 24px; }}
      .master-doc-cta {{ padding: 40px 28px; }}
      footer.main-footer {{ flex-direction: column; text-align: center; }}
    }}
  </style>
</head>
<body>

  <nav>
    <a href="#" class="nav-logo">α Centauri</a>
    <div class="nav-links">
      <a href="#phases">Phases</a>
      <a href="master_doc.html">Master Doc</a>
      <a href="https://github.com/Cleanskiier27/project-alpha-centauri">GitHub</a>
    </div>
  </nav>

  <section class="hero">
    <div class="hero-badge">CIS Framework &bull; TRL 1–9 &bull; SBIR Phase I–III</div>
    <h1><span class="gradient-text">Project Alpha Centauri</span></h1>
    <p class="hero-sub">
      A 30-phase SBIR and TRL-aligned maturation pipeline for lunar technology development,
      fully integrated with the CIS Umbrella, PLLC Mirror/Base, and PRECISELIENS visualization layer.
    </p>
    <div class="hero-buttons">
      <a href="master_doc.html" class="btn btn-primary">📄 Read Master Document</a>
      <a href="https://github.com/Cleanskiier27/project-alpha-centauri" class="btn btn-outline">⭐ View on GitHub</a>
    </div>
  </section>

  <div class="stats-bar">
    <div class="stat"><div class="stat-num">30</div><div class="stat-label">CIS Artifacts</div></div>
    <div class="stat"><div class="stat-num">6</div><div class="stat-label">Mission Phases</div></div>
    <div class="stat"><div class="stat-num">TRL 9</div><div class="stat-label">Target Readiness</div></div>
    <div class="stat"><div class="stat-num">3</div><div class="stat-label">SBIR Phases</div></div>
    <div class="stat"><div class="stat-num">41k</div><div class="stat-label">Words</div></div>
  </div>

  <div class="section" id="phases">
    <div class="section-label">// Mission Architecture</div>
    <h2 class="section-title">Six Vector Phases</h2>
    <p class="section-sub">Each phase delivers 5 CIS artifacts, progressing the technology from concept to flight-proven TRL 9.</p>

    <div class="phases-grid">
      {"".join(landing_cards)}
    </div>
  </div>

  <div class="master-doc-cta">
    <div>
      <h2>📄 Centauri Master Document</h2>
      <p>All 30 CIS artifacts stitched into a single 1,600-line document — structured with an interactive Table of Contents, normalized heading hierarchy, and phase-by-phase chapter divisions.</p>
    </div>
    <a href="master_doc.html" class="btn btn-primary" style="white-space:nowrap;">Read Full Document →</a>
  </div>

  <div class="section" id="visualizations" style="padding-top: 20px;">
    <div class="section-label">// Mission Control Center</div>
    <h2 class="section-title">Interactive Visualizations & Specs</h2>
    <p class="section-sub">Experience real-time interactive space operations, neural synchronizations, and deep-space role allocations.</p>
    
    <div class="phases-grid">
      <div class="phase-card" style="border-color: rgba(123, 47, 255, 0.25);">
        <div class="phase-header">
          <div class="phase-icon b">🛰️</div>
          <div>
            <div class="phase-name">Interactive Simulations</div>
            <div class="phase-trl">PRECISELIENS Layer</div>
          </div>
        </div>
        <ul class="phase-artifacts">
          <li><span class="artifact-id">NAV-SYS</span><a href="viz/galactic_navigation_system.html" style="color:var(--muted); text-decoration:none;">Galactic Navigation System</a></li>
          <li><span class="artifact-id">EXO-HUB</span><a href="viz/proxima_b_exohub.html" style="color:var(--muted); text-decoration:none;">Proxima B Exohub Console</a></li>
          <li><span class="artifact-id">TERRA</span><a href="viz/proxima_b_terraforming.html" style="color:var(--muted); text-decoration:none;">Proxima B Terraforming Panel</a></li>
          <li><span class="artifact-id">SLIDES</span><a href="viz/galactic_mission_slides.html" style="color:var(--muted); text-decoration:none;">Galactic Mission Slides</a></li>
        </ul>
      </div>

      <div class="phase-card" style="border-color: rgba(0, 198, 255, 0.25);">
        <div class="phase-header">
          <div class="phase-icon a">🔬</div>
          <div>
            <div class="phase-name">Core Specs & Metrics</div>
            <div class="phase-trl">Galactic Framework</div>
          </div>
        </div>
        <ul class="phase-artifacts">
          <li><span class="artifact-id">SYNC</span><a href="viz/bigtree_sync.html" style="color:var(--muted); text-decoration:none;">Bigtree Neural Sync Log</a></li>
          <li><span class="artifact-id">CLUSTER</span><a href="viz/galactic_cluster_specs.html" style="color:var(--muted); text-decoration:none;">Galactic Cluster Specifications</a></li>
          <li><span class="artifact-id">ROLES</span><a href="galactic_roles.html" style="color:var(--muted); text-decoration:none;">Galactic Roles Granted</a></li>
          <li><span class="artifact-id">SPECS</span><a href="project_specs.html" style="color:var(--muted); text-decoration:none;">Full System Specs Matrix</a></li>
          <li><span class="artifact-id">AI-DATA</span><a href="ai_training_personalization.html" style="color:var(--muted); text-decoration:none;">AI Training & Personalization</a></li>
          <li><span class="artifact-id">GUIDE</span><a href="implementation_guide.html" style="color:var(--muted); text-decoration:none;">Implementation Guide</a></li>
          <li><span class="artifact-id">STERIL</span><a href="sterilization.html" style="color:var(--muted); text-decoration:none;">Sterilization Protocol</a></li>
          <li><span class="artifact-id">CHECKLIST</span><a href="sterilization_checklist.html" style="color:var(--muted); text-decoration:none;">Sterilization Checklist</a></li>
          <li><span class="artifact-id">BID-JSON</span><a href="NASA_SBIR_ROBOTIC_BID.json" style="color:var(--muted); text-decoration:none;">NASA SBIR Robotic Bid JSON</a></li>
          <li><span class="artifact-id">BID-SUBMIT</span><a href="nasa_robotic_bid.html" style="color:var(--muted); text-decoration:none;">Robotic Swarm Bid Proposal</a></li>
        </ul>
      </div>
    </div>
  </div>

  <footer class="main-footer">
    <div class="footer-brand">PROJECT ALPHA CENTAURI &bull; CIS FRAMEWORK</div>
    <div class="footer-links">
      <a href="https://github.com/Cleanskiier27/project-alpha-centauri">GitHub</a>
      <a href="master_doc.html">Master Document</a>
    </div>
  </footer>

</body>
</html>
"""

with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f_out:
    f_out.write(index_html)

print("Generated index.html with interactive artifact catalog links.")

# -------------------------------------------------------------
# Additional copy and conversion scripts for complete build
# -------------------------------------------------------------
import shutil

# Copy viz directory to _site/viz
viz_src = "viz"
viz_dest = os.path.join(output_dir, "viz")
if os.path.exists(viz_src):
    try:
        shutil.copytree(viz_src, viz_dest, dirs_exist_ok=True)
        print("Copied viz folder to _site/viz")
    except Exception as e:
        print(f"Warning: Could not copy viz folder: {e}")

# Copy json bid payload
bid_src = "docs/NASA_SBIR_ROBOTIC_BID.json"
bid_dest = os.path.join(output_dir, "NASA_SBIR_ROBOTIC_BID.json")
if os.path.exists(bid_src):
    shutil.copy2(bid_src, bid_dest)
    print("Copied NASA_SBIR_ROBOTIC_BID.json to _site/")

# Convert other md files in docs/ to HTML
docs_to_convert = [
    ("docs/GALACTIC_ROLES_GRANTED.md", "galactic_roles.html", "Galactic Roles"),
    ("docs/PROJECT_SPECS_FULL.md", "project_specs.html", "Project Specifications"),
    ("docs/AI_TRAINING_AND_DATA_PERSONALIZATION.md", "ai_training_personalization.html", "AI Training"),
    ("docs/IMPLEMENTATION_GUIDE.md", "implementation_guide.html", "Implementation Guide"),
    ("docs/STERILIZATION.md", "sterilization.html", "Sterilization Protocol"),
    ("docs/STERILIZATION_CHECKLIST.md", "sterilization_checklist.html", "Sterilization Checklist"),
    ("docs/NASA-ROBOTIC-BID-SUBMISSION.md", "nasa_robotic_bid.html", "Robotic Swarm Proposal"),
]

for src_md, out_name, doc_title in docs_to_convert:
    if os.path.exists(src_md):
        with open(src_md, "r", encoding="utf-8") as f_in:
            md_text = f_in.read()
        parsed_body = md_to_html(md_text)
        
        page_html = []
        page_html.append(generate_header(doc_title))
        page_html.append(f"""
          <div style="max-width: 800px; margin: 40px auto; padding: 0 4%;">
            <a href="index.html" style="color: var(--primary); text-decoration: none; font-size: 0.9rem; font-family: 'JetBrains Mono', monospace;">&larr; Back to Dashboard</a>
            <div class="markdown-body" style="margin-top: 30px;">
              {parsed_body}
            </div>
          </div>
          <footer>
            PROJECT ALPHA CENTAURI &bull; CIS TECHNOLOGY MATURATION REGISTRY
          </footer>
        """)
        page_html.append("</div></body></html>")
        
        # Write file (adjust links from chapters folder back to root)
        header_adjusted = generate_header(doc_title).replace("../index.html", "index.html").replace("../master_doc.html", "master_doc.html")
        page_html[0] = header_adjusted
        
        with open(os.path.join(output_dir, out_name), "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(page_html))
        print(f"Generated {out_name} from {src_md}")


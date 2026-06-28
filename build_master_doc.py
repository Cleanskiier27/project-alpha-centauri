import os

root = "docs/centauri"
output_file = "docs/Centauri_Master_Document.md"

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

doc_content = []
doc_content.append("# Project Alpha Centauri: Master Document\n\n")
doc_content.append("## Executive Summary\n\n")
doc_content.append("This document compiles the 30-phase SBIR- and TRL-aligned maturation pipeline for Project Alpha Centauri. It details the progression from core scientific principles through experimental validation, systems engineering, orbital simulation, and lunar operational readiness.\n\n")

doc_content.append("## Table of Contents\n\n")
for section, files in sections.items():
    section_name_clean = section.replace("_", " ")
    section_anchor = section.lower()
    doc_content.append(f"- [{section_name_clean}](#{section_anchor})\n")
    for f in files:
        name_part = f.replace(".md", "")
        parts = name_part.split("_", 1)
        doc_code = parts[0]
        doc_title = parts[1].replace("_", " ")
        # Build anchor matching how typical markdown renderers create IDs (e.g. cis-a1-pdm-problem-definition-matrix)
        anchor_title = name_part.lower().replace("_", "-").replace(" ", "-")
        doc_content.append(f"  - [{doc_code}: {doc_title}](#{anchor_title})\n")

doc_content.append("\n---\n\n")

for section, files in sections.items():
    section_name_clean = section.replace("_", " ")
    doc_content.append(f"# {section_name_clean}\n\n")
    for f in files:
        filepath = os.path.join(root, section, f)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as file_in:
                content = file_in.read()
                
                # Demote headers by one level to maintain proper outline hierarchy in the combined doc
                lines = content.splitlines()
                demoted_lines = []
                for line in lines:
                    if line.startswith("#"):
                        demoted_lines.append("#" + line)
                    else:
                        demoted_lines.append(line)
                content_demoted = "\n".join(demoted_lines)
                doc_content.append(content_demoted)
                doc_content.append("\n\n---\n\n")
        else:
            print(f"Warning: File not found: {filepath}")

# Remove the last separator if it is a horizontal rule
if doc_content and doc_content[-1] == "\n\n---\n\n":
    doc_content.pop()

# Ensure target directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w", encoding="utf-8") as file_out:
    file_out.writelines(doc_content)

print(f"Stitched master document written successfully to: {output_file}")

---
name: RNA Immunoprecipitation qPCR Protocol
id: PROT-0014
version: 1.0
description: Protocol for RNA immunoprecipitation followed by RT-qPCR to detect RNA-protein interactions
author: Jordan Lab
created: 2025-05-06
materials:
  - Cell culture dishes
  - PBS (cold)
  - UV crosslinker (254 nm) or formaldehyde
  - Lysis buffer with RNase inhibitors
  - Protein A/G beads
  - Antibodies for target protein
  - IgG control antibody
  - Glycine solution (for formaldehyde quenching)
  - RNA isolation reagents
  - RT-qPCR reagents
steps:
  - "Grow cells to desired confluency"
  - "Perform crosslinking (UV or formaldehyde)"
  - "Harvest and lyse cells"
  - "Pre-clear lysates"
  - "Perform immunoprecipitation with specific antibody"
  - "Wash beads to remove non-specific binding"
  - "Reverse crosslinks if needed"
  - "Isolate RNA from immunoprecipitated complex"
  - "Perform RT-qPCR to detect target RNA"
notes: |
  Two crosslinking methods are described: UV (254 nm) and formaldehyde
  UV crosslinking is more specific but requires specialized equipment
  Formaldehyde crosslinking is simpler but may have higher background
  Always include appropriate controls (IgG, input RNA)
---

#Protocol 

Crosslinking RNA to a specific protein of interest in cells or lysates is a common step in RNA immunoprecipitation (RIP) or related methods (e.g., CLIP-seq). Once crosslinked and immunoprecipitated, the RNA can be extracted for downstream RT-qPCR analysis. Below is a general overview of two frequently used crosslinking methods—UV crosslinking and formaldehyde crosslinking—along with key steps and considerations.

### UV Crosslinking
UV crosslinking at 254 nm forms covalent bonds between nucleic acids and amino acids in close proximity. This approach is often used in CLIP (crosslinking immunoprecipitation) protocols, but it can be adapted for simpler RIP-RT-qPCR workflows.

#### Typical workflow:
1. Grow cells to the desired confluency in culture dishes.
2. Wash cells with cold PBS to remove media and serum proteins. Keep cells on ice if needed to minimize RNase activity.
3. Add fresh cold PBS to cover the cells.
4. Crosslink with UV 254 nm at an energy of approximately 150–300 mJ/cm². (The optimal dose depends on cell type and the sensitivity of the RNA or protein. Over-crosslinking can damage RNA, while under-crosslinking may reduce yield.)
5. Harvest cells by scraping or gentle trypsinization (depending on the downstream protocol).
6. Lyse cells under mild conditions suitable for maintaining RNP complexes. (Often a nonionic or mild ionic detergent is used in the lysis buffer, along with RNase inhibitors.)
7. Perform immunoprecipitation using an antibody specific to the RNA-binding protein of interest.
8. Pre-clear lysates (e.g., with protein A/G beads alone) to reduce nonspecific binding.
9. Add the specific antibody, followed by protein A/G beads.
10. Wash beads thoroughly to remove nonspecific complexes.
11. Reverse crosslink (if needed) or proceed directly to RNA purification, depending on the protocol. Some protocols lyse or treat with proteinase K to release RNA from the protein-bead complex.
12. Isolate RNA from the immunoprecipitated complex.
13. Reverse transcribe and perform qPCR to detect the RNA targets that were bound by the protein.
14. Key considerations for UV crosslinking:
15. Irradiation distance/energy: Keep the distance between the UV lamp and cells/lysate standardized to ensure reproducibility.
16. Crosslinking efficiency vs. RNA integrity: Higher UV doses may degrade RNA. It’s important to titrate energy.
17. Protective measures: UV light is harmful to skin and eyes. Always use shields and PPE.

#### Formaldehyde Crosslinking

##### Overview:
Formaldehyde can be used to crosslink proteins and nucleic acids by reacting with amino and imino groups. It is less commonly used for fine-scale mapping studies (like CLIP-seq) because it can be somewhat reversible and can introduce more nonspecific crosslinks. However, it is still used in some RIP and ChIP (chromatin IP) approaches.

##### Typical workflow:
Grow cells to desired confluency.
Prepare fresh formaldehyde at a working concentration (often 1% final in the culture medium) to fix cells.
Add formaldehyde directly to cells in culture medium (or in PBS) and incubate typically for 5–10 minutes at room temperature or 37 °C (depending on the protocol).
Quench the reaction by adding glycine (often to a final concentration of 125 mM) for 5–10 minutes.
Wash the cells with cold PBS.
Harvest cells carefully.
Lyse cells under conditions that preserve protein-RNA complexes (often using mild detergents, protease inhibitors, and RNase inhibitors).
Immunoprecipitate using a specific antibody against the protein of interest.
Wash beads to remove nonspecific material.
Reverse crosslink by heating or using other conditions specified in the protocol (formaldehyde crosslinks can often be reversed by heating at 65 °C for several hours in the presence of SDS and/or high salt).
Isolate RNA from the immunoprecipitated sample.
Reverse transcribe and perform qPCR to quantify target RNA levels.
Key considerations for formaldehyde crosslinking:
Crosslinking stringency: Formaldehyde can create more nonspecific crosslinks; optimizing crosslinking time and concentration is key.
Reversibility: Ensure you reverse crosslinks thoroughly to recover intact RNA for RT-qPCR.
Toxicity: Formaldehyde is highly toxic and volatile, so follow safety guidelines (work in a fume hood, use PPE).

#### Choosing the Method
#### UV Crosslinking
1. Generally provides more specific crosslinks between directly interacting residues (protein–RNA).
2. Can require specialized equipment (UV crosslinker).
3. More commonly used in CLIP-based methods for precise mapping of RNA-protein interaction sites.
4. Formaldehyde Crosslinking
5. Straightforward chemical method.
6. Potentially higher background due to nonspecific crosslinks.
7. Reversal requires heating and/or high salt conditions, which can be harsh on samples.
8. For many RNA-IP followed by RT-qPCR experiments (RIP-qPCR), mild crosslinking using UV at 254 nm is quite popular because it preserves specificity. However, if you already have a formaldehyde-based protocol optimized for your lab, that can also work.

#### Final Tips
Pilot Experiments: 
	Always optimize crosslinking conditions (time, energy, concentration) to balance specificity vs. yield.
	Test different crosslinking strengths and confirm via a known positive RNA target.
Include Controls:
	Use an IgG control or a nonspecific antibody to measure background binding.
Use input RNA to normalize or calculate percentage of input in qPCR.
Validate with Known Targets:
	If possible, use a known RNA that your protein interacts with as a positive control.
Handle RNA Carefully:
	Incorporate RNase inhibitors in all buffers, and keep samples cold when possible.


#### Safety Considerations:
1. UV crosslinking: protect from direct UV exposure; follow lamp manufacturer’s guidelines.
2. Formaldehyde: use a fume hood; wear gloves and goggles.


**By choosing the appropriate crosslinking approach and carefully optimizing the conditions, you can capture stable RNA-protein interactions, immunoprecipitate your protein of interest, and then detect and quantify the associated RNAs by RT-qPCR.**

---
name: BCA Assay for Protein Abundance Determination
id: PROT-0010
version: 1.0
description: Protocol for colorimetric detection and quantitation of total protein using bicinchoninic acid (BCA)
author: Jordan Lab
created: 2025-05-06
materials:
  - BCA Reagent A
  - BCA Reagent B
  - BSA standards
  - Microplate
  - Plate reader (562 nm capability)
  - Pipettes and tips
steps:
  - "Determine number of standards and unknowns to quantify"
  - "Prepare working reagent (WR) by mixing BCA reagent A and B in 50:1 ratio"
  - "Pipette 10 µL of each standard/sample into microplate wells"
  - "Add 200 µL of WR to each well and mix for 30 seconds"
  - "Incubate at 37°C for 30 minutes"
  - "Measure absorbance at 562 nm"
  - "Create standard curve and determine protein concentrations"
notes: |
  Based on Pierce BCA Protein Assay Kit (Thermo Scientific)
  Assay is nearly linear with protein concentrations from 20-2000 µg/mL
  For increased sensitivity, incubation time can be extended to 2 hours
---

#Protocol 

1. Determine the number of standards and unknowns you need to quantify:
    

2. (Number of standards + Number of unknowns) x (Number of replicates) x (Volume of WR per sample) = Total WR volume
    

3. Mix 50 parts of BCA reagent A with 1 part of BCA reagent B (50:1 ratio, Reagent A:B).
    

4. Example: Combine 5 mL of reagent A with 0.1 mL of reagent B to prepare 5.1 mL of WR.
    
5. Note: Initial turbidity when reagent B is added to reagent A will disappear with mixing, yielding a clear, green WR.
    

6. Pipette 10 µL of each standard or unknown sample replicates into a microplate well.
    
7. Add 200 µL of the WR to each well and mix the plate thoroughly for 30 seconds.
    
8. Incubate at 37°C for 30 minutes.
    
9. Measure the absorbance at 562 nm on (core facility) plate reader.
    
10. Subtract the average 562 nm absorbance measurement of the blank standard replicates from the 562 nm measurements of all other individual standard and unknown sample replicates.
    
11. Prepare a standard curve by plotting the average blank–corrected 562 nm measurement for each BSA standard vs. its concentration in µg/mL. Use the standard curve to determine the protein concentration of each unknown sample.
    

**
**

Standard Preparation

  

Prepare standards in the using the same buffer you collected your protein samples in as the diluent.

  

|Vial|Volume of Diluent|Volume and Source of BSA|Final BSA Concentration (µg/mL)|
|---|---|---|---|
|A|0|300 µL of stock|2,000|
|B|125 µL|375 µL of stock|1,500|
|C|325 µL|325 µL of stock|1,000|
|D|175 µL|175 µL of vial B dilution|750|
|E|325 µL|325 µL of vial C dilution|500|
|F|325 µL|325 µL of vial E dilution|250|
|G|325 µL|325 µL of vial F dilution|125|
|H|400 µL|100 µL of vial G dilution|25|
|I|400 µL|0|0 (Blank)|

  
  **

Pierce BCA Protein Assay Kit (Thermo Scientific ) Protocol

  

Background:

- The kit uses bicinchoninic acid (BCA) for colorimetric detection and quantitation of total protein.
    
- It's based on the biuret reaction, where Cu+2 is reduced to Cu+1 by protein in an alkaline medium.
    
- The cuprous cation (Cu+1) is detected using BCA, forming a purple-colored complex that absorbs at 562 nm.
    
- The assay is nearly linear with protein concentrations from 20–2000 µg/mL.
    
- Protein concentrations are usually determined against a standard protein like bovine serum albumin (BSA).
    
- ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcka1kV7JyE-wobGCZVdzAMfYtdUeY1znSSiwfDwwYmGxxlOOdyIViCfWX7cXr9gTdXoVPGpYMHA0MqDd4X4Ypxcd_ruLrPACkT2misFNu9h2uNt0lxj1CdDBNTNi4RMxozetuC?key=meF1uyEKsycTs30xvLd7mXoN)
    

**
  
  
  
  
  
****

Note:

- Wavelengths from 540–590 nm have been used successfully with this method.
    
- Plate readers, which use a shorter light path length than cuvette spectrophotometers, require a greater sample to WR ratio to obtain the same sensitivity as the standard test tube procedure. If higher 562 nm measurements are desired, increase the incubation time to 2 hours.
    
- Increasing the incubation time or ratio of sample volume to WR increases the net 562 nm measurement for each well and lowers both the minimum detection level of the reagent and the working range of the assay. As long as all standards and unknowns are treated identically, such modifications are useful.
    

  

1. Subtract the average 562 nm absorbance measurement of the blank standard replicates from the 562 nm measurements of all other individual standard and unknown sample replicates.
    
2. Prepare a standard curve by plotting the average blank–corrected 562 nm measurement for each BSA standard vs. its concentration in µg/mL. Use the standard curve to determine the protein concentration of each unknown sample.
    

Note: If using curve-fitting algorithms associated with a microplate reader, a four-parameter (quadratic) or best–fit curve provides more accurate results than a purely linear fit. If plotting results by hand, a point–to–point curve is preferable to a linear fit to the standard points.

**
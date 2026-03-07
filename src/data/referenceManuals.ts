export interface ReferenceManual {
  id: string;
  name: string;
  author: string;
  content: string;
}

export const VET_REFERENCE_MANUALS: ReferenceManual[] = [
  {
    id: "merck-cattle-001",
    name: "Merck Veterinary Manual: Digestive System (Cattle)",
    author: "Merck & Co., Inc.",
    content: `[Source: Merck Veterinary Manual - Digestive System/Bloat]
BLOAT IN RUMINANTS (FROTHY BLOAT)
Etiology: Frothy bloat is usually associated with the ingestion of leguminous plants (alfalfa, clovers) or high-grain rations in feedlots.
Clinical Findings: Distention of the left ruminoreticular compartment is the primary sign. In severe cases, labored breathing and protrusion of the tongue occur.
Treatment: For frothy bloat, use an antifoaming agent like poloxalene (25–50 g, PO). In emergency cases, a trocar and cannula may be required.

[Source: Merck Veterinary Manual - Digestive System/Hardware Disease]
TRAUMATIC RETICULOPERITONITIS (HARDWARE DISEASE)
Etiology: Ingestion of metallic objects (nails, wire) that settle in the reticulum.
Clinical Findings: Sudden drop in milk production, arched back, reluctance to move, and a "grunt" heard on the grunt test (pressure on the xiphoid).
Prevention: Administration of a reticulum magnet at 6–8 months of age is the standard preventative measure.`
  },
  {
    id: "merck-cattle-002",
    name: "Merck Veterinary Manual: Respiratory System (Cattle)",
    author: "Merck & Co., Inc.",
    content: `[Source: Merck Veterinary Manual - Respiratory System/BRD]
BOVINE RESPIRATORY DISEASE COMPLEX (BRD)
Etiology: Multifacted, involving stress (weaning, transport), viral pathogens (IBR, BVDV), and bacterial pathogens (Mannheimia haemolytica).
Clinical Findings: Fever (104–106°F), serous to mucopurulent nasal discharge, increased respiratory rate, and coughing.
Treatment: Early treatment with long-acting antibiotics (e.g., Tulathromycin, Florfenicol) is critical for success.`
  },
  {
    id: "merck-cattle-003",
    name: "Merck Veterinary Manual: Reproductive System (Cattle)",
    author: "Merck & Co., Inc.",
    content: `[Source: Merck Veterinary Manual - Reproductive System/Dystocia]
DYSTOCIA (DIFFICULT CALVING)
Etiology: Fetal oversize, malpresentation, uterine inertia, or pelvic immaturity in heifers.
Clinical Findings: Prolonged labor (>2 hours of active straining without progress), visible fetal parts without delivery, cow in distress.
Treatment: Correct malpresentation manually with adequate lubrication. Apply obstetric chains above fetlock joints and traction in downward arc following cow's straining. If unresolvable within 30 minutes of correction, perform fetotomy or cesarean section.
Prevention: Select bulls with low birth weight EPDs for heifer breeding. Ensure heifers reach 65% of mature body weight before first breeding.

[Source: Merck Veterinary Manual - Reproductive System/Retained Placenta]
RETAINED FETAL MEMBRANES (RETAINED PLACENTA)
Definition: Failure to expel placenta within 12–24 hours post-calving.
Etiology: Dystocia, twins, abortion, selenium/vitamin E deficiency, hypocalcemia, or premature calving.
Clinical Findings: Visible fetal membranes hanging from vulva beyond 24 hours. May progress to metritis with fetid discharge, fever, and drop in milk production.
Treatment: Do NOT forcibly remove retained membranes — increases risk of hemorrhage and endometrial damage. Administer systemic antibiotics (oxytetracycline) if signs of systemic illness. Allow natural separation within 5–7 days. Monitor rectal temperature daily.

[Source: Merck Veterinary Manual - Reproductive System/Metritis]
PUERPERAL METRITIS
Etiology: Bacterial contamination of uterus post-calving, often following dystocia or retained placenta. Common organisms: E. coli, Fusobacterium necrophorum, Trueperella pyogenes.
Clinical Findings: Fetid, watery, red-brown uterine discharge within 10 days of calving; fever >103.5°F; depression; reduced milk yield; anorexia.
Treatment: Systemic antibiotics — ceftiofur (2.2 mg/kg IM, 5 days) is first-line. NSAIDs (flunixin meglumine) for fever and pain. Intrauterine antibiotics are of limited additional benefit.
Prognosis: Early treatment leads to good recovery; delayed cases may result in chronic endometritis and reduced fertility.

[Source: Merck Veterinary Manual - Reproductive System/Ovarian Cysts]
CYSTIC OVARIAN DISEASE
Definition: Anovulatory follicles ≥25 mm persisting for ≥10 days without a corpus luteum.
Types: Follicular cysts (thin-walled, estrogen-producing) vs. luteal cysts (thick-walled, progesterone-producing).
Clinical Findings: Irregular or absent estrous cycles; nymphomania (continuous estrus) in follicular cysts; anestrus in luteal cysts. Diagnosis confirmed by rectal palpation or ultrasonography.
Treatment: GnRH (100 mcg IV/IM) to induce luteinization, followed by PGF2α 7 days later. Alternatively, manual rupture (luteal cysts only) or progesterone-based protocols (CIDR).`
  },
  {
    id: "merck-cattle-004",
    name: "Merck Veterinary Manual: Mastitis (Cattle)",
    author: "Merck & Co., Inc.",
    content: `[Source: Merck Veterinary Manual - Mastitis/Overview]
MASTITIS IN DAIRY CATTLE
Definition: Inflammation of the mammary gland, almost always caused by microbial infection. The most economically significant disease in dairy cattle worldwide.

CLASSIFICATION
Clinical Mastitis: Visible abnormalities in milk (flakes, clots, watery secretion) with or without swelling, heat, and pain in the udder. May be accompanied by systemic signs (fever, depression) in severe cases.
Subclinical Mastitis: No visible changes in milk or udder, but elevated somatic cell count (SCC >200,000 cells/mL). Diagnosed via California Mastitis Test (CMT) or SCC.

ETIOLOGY
Contagious pathogens (spread cow-to-cow during milking): Staphylococcus aureus, Streptococcus agalactiae, Mycoplasma bovis.
Environmental pathogens (acquired from environment): E. coli, Klebsiella spp., Streptococcus uberis, Streptococcus dysgalactiae.

CLINICAL FINDINGS
Mild/Moderate: Abnormal milk secretion, mild udder swelling. Cow is alert and eating.
Severe/Peracute: Hard, hot, painful quarter; watery or bloody secretion; cow is febrile (>104°F), depressed, anorexic. Gram-negative (coliform) mastitis can cause toxic shock.

TREATMENT
Mild-Moderate: Intramammary antibiotics (pirlimycin, cloxacillin) per label. Frequent stripping of affected quarter. NSAIDs for pain.
Severe: IV fluids, systemic antibiotics (ceftiofur or penicillin + aminoglycoside), flunixin meglumine (2.2 mg/kg IV). Oxytocin to aid milk let-down and frequent stripping.
Culling consideration: Chronic S. aureus cases rarely cure; cull or segregate to prevent herd spread.

MILKING HYGIENE PROTOCOLS
Pre-dipping: Apply germicidal pre-dip (iodine 0.5–1%), contact time 30 seconds, wipe dry with individual paper towel.
Unit attachment: Attach within 60–90 seconds of stimulation to capture let-down reflex.
Post-dipping: Apply barrier post-dip (iodine 1% with emollient) immediately after unit removal.
Teat scoring: Score teat-end condition quarterly (1=smooth, 4=very rough/hyperkeratotic). Scores ≥3 indicate over-milking or liner issues.

DRY COW THERAPY
Selective dry cow therapy (SDCT): Treat only quarters with SCC >200,000 or culture-positive at dry-off.
Blanket dry cow therapy (BDCT): Treat all quarters — use in high SCC herds (herd average >250,000 cells/mL).
Internal teat sealant (bismuth subnitrate): Use in all cows regardless of infection status to form physical barrier during dry period.`
  },
  {
    id: "merck-cattle-005",
    name: "Merck Veterinary Manual: Foot & Hoof Disorders (Cattle)",
    author: "Merck & Co., Inc.",
    content: `[Source: Merck Veterinary Manual - Foot & Hoof/Laminitis]
LAMINITIS (PODODERMATITIS ASEPTICA DIFFUSA)
Etiology: Subacute ruminal acidosis (SARA) from high-grain diets, resulting in release of vasoactive substances that disrupt hoof laminar blood flow. Subclinical cases are the most economically significant.
Clinical Findings:
- Acute: Severe lameness, reluctance to move, shifting weight, lying down excessively, elevated hoof temperature, pain on hoof testers.
- Subclinical: No overt lameness; identified at routine trimming by sole hemorrhages (red/yellow discoloration), yellow waxy sole, and white line zone abnormalities.
- Chronic: Flat soles, widened white line, "slipper foot" conformation, concave dorsal wall.
Treatment: NSAIDs (flunixin meglumine or ketoprofen). Correct dietary management — ensure adequate effective fiber (NDF >28% of DM, particle length >1.9 cm). Provide adequate lying time and rubber flooring.
Prevention: Gradual transition to high-energy diets. Sodium bicarbonate buffer (0.75% of DM). Hoof trimming every 6 months.

[Source: Merck Veterinary Manual - Foot & Hoof/Foot Rot]
FOOT ROT (INTERDIGITAL NECROBACILLOSIS / FOUL-IN-THE-FOOT)
Etiology: Fusobacterium necrophorum and Porphyromonas levii (formerly Bacteroides melaninogenicus) infecting the interdigital skin after trauma or maceration from wet conditions.
Clinical Findings: Acute, severe lameness in one limb. Symmetric swelling of the interdigital space and coronary band. Characteristic foul odor. Interdigital skin shows necrotic lesion with gray-white exudate. Fever (103–104°F) common.
Treatment: Penicillin (22,000 IU/kg IM, 3–5 days) or oxytetracycline (11 mg/kg IV, 3 days) or ceftiofur. Clean and debride interdigital lesion. Apply topical sulfadimethoxine or copper sulfate bandage. Most cases resolve within 3–5 days with appropriate antibiotics.
Prevention: Footbaths with copper sulfate (5%) or formalin (3–5%) 2–3x/week. Reduce mud and standing water. Zinc supplementation.

[Source: Merck Veterinary Manual - Foot & Hoof/Digital Dermatitis]
DIGITAL DERMATITIS (MORTELLARO'S DISEASE)
Etiology: Treponema spp. (spirochetes) — highly contagious, spreads cow-to-cow via contaminated environment and milking equipment.
Clinical Findings: Painful, circumscribed, strawberry-like lesion typically at the skin-horn junction of the plantar pastern (heel bulb). Lesions classified by M-scoring system:
- M0: Normal skin
- M1: Small (<2 cm) active ulcer
- M2: Classical large (>2 cm) active ulcer — most painful, animal lifts foot repeatedly
- M3: Healing lesion with scab
- M4: Chronic, proliferative lesion
Treatment: Individual cow: topical oxytetracycline spray (apply, leave uncovered if possible). Wrap lesions only if heavily contaminated environment. Systemic antibiotics for severe cases.
Herd control: Footbath with lincomycin or oxytetracycline solution (footbath antibiotic protocols per vet prescription). Copper sulfate footbaths for maintenance. Identify and treat all M2 lesions promptly.`
  },
  {
    id: "merck-cattle-006",
    name: "Merck Veterinary Manual: Neonatal & Calf Health",
    author: "Merck & Co., Inc.",
    content: `[Source: Merck Veterinary Manual - Neonatal/Colostrum Management]
COLOSTRUM MANAGEMENT & FAILURE OF PASSIVE TRANSFER
Importance: Calves are born agammaglobulinemic (no circulating antibodies). Colostrum IgG absorption is maximal in first 4 hours and ceases by 24 hours.
Passive Transfer Assessment: Serum total protein >5.5 g/dL (refractometer) or serum IgG >10 g/L at 24–48 hours of age = adequate passive transfer.
Failure of Passive Transfer (FPT): Serum IgG <10 g/L. Associated with 3–5x higher morbidity and 2x higher mortality.
Protocol:
- Feed ≥4 liters of high-quality colostrum (Brix refractometer reading ≥22%) within first 2 hours of birth.
- If dam colostrum unavailable or poor quality, use frozen bank colostrum or commercial colostrum replacer (≥150 g IgG).
- Test colostrum quality before feeding with colostrometer or Brix refractometer.

[Source: Merck Veterinary Manual - Neonatal/Calf Scours]
NEONATAL CALF DIARRHEA (SCOURS)
Etiology by age:
- Day 1–3: E. coli K99 (enterotoxigenic), Salmonella
- Day 3–7: Rotavirus, Coronavirus
- Day 7–21: Cryptosporidium parvum
- Day >14: Salmonella, Coronavirus, dietary
Clinical Findings: Profuse watery diarrhea; dehydration (assessed by skin tent, sunken eyes, inability to stand); acidosis; weakness; hypothermia in severe cases.
Dehydration scoring:
- <5%: Mild, alert, stands
- 6–8%: Moderate, skin tent >2 sec, weak suckle
- 8–10%: Severe, cannot stand, sunken eyes
- >10%: Moribund, requires IV fluids immediately
Treatment:
Oral electrolytes: First-line for calves that can stand and suckle. Use alkalinizing solution (contain bicarbonate or acetate). Feed 2–4 L every 6–12 hours. Do NOT mix with milk — give separately.
IV fluids: For calves unable to stand. Isotonic saline + sodium bicarbonate (for acidosis). Calculate deficit: % dehydration × body weight (kg) = liters needed.
Antibiotics: Only if systemic illness (fever, septicemia). Trimethoprim-sulfa or enrofloxacin. Do NOT use antibiotics routinely for viral scours.

[Source: Merck Veterinary Manual - Neonatal/Navel Ill]
OMPHALITIS & OMPHALOPHLEBITIS (NAVEL ILL)
Etiology: Bacterial infection of umbilical structures (urachal remnant, umbilical arteries/vein) — E. coli, Trueperella pyogenes, Fusobacterium. Often a sequel to poor navel disinfection or wet, contaminated calving environment.
Clinical Findings: Swelling, heat, and pain at navel; purulent discharge; fever; depression. May extend to liver abscess, peritonitis, or polyarthritis (joint ill).
Treatment: Systemic antibiotics for minimum 7–14 days (penicillin or ampicillin). Surgical drainage if abscess present. IV fluids if systemically ill. Prognosis is guarded if internal structures are involved.
Prevention: Dip navel in 7% tincture of iodine or chlorhexidine immediately after birth. Ensure clean, dry calving environment.

[Source: Merck Veterinary Manual - Neonatal/Calf Pneumonia]
ENZOOTIC PNEUMONIA IN CALVES
Etiology: Multifactorial — primary viral pathogens (RSV, PI3, BCoV) followed by secondary bacterial infection (Mannheimia haemolytica, Pasteurella multocida, Mycoplasma bovis).
Risk factors: Overcrowding, poor ventilation, mixing of age groups, wide temperature fluctuations, FPT.
Clinical Findings: Fever (>104°F), increased respiratory rate and effort, nasal discharge (serous progressing to mucopurulent), coughing, depression, reduced growth rate.
DART scoring (used in many operations): Depression + Appetite loss + Respiratory signs + Temperature — score ≥4 indicates treatment.
Treatment: Tulathromycin (2.5 mg/kg SC, single dose) or florfenicol (40 mg/kg SC). NSAIDs reduce fever and improve recovery. Reassess within 48–72 hours.`
  },
  {
    id: "merck-cattle-007",
    name: "Merck Veterinary Manual: Metabolic Diseases & Nutrition (Cattle)",
    author: "Merck & Co., Inc.",
    content: `[Source: Merck Veterinary Manual - Metabolic/Milk Fever]
HYPOCALCEMIA (MILK FEVER / PARTURIENT PARESIS)
Etiology: Rapid onset of lactation depletes serum calcium faster than homeostatic mechanisms can compensate. Most common in high-producing cows in 2nd+ lactation. Jersey breed predisposed.
Clinical Findings:
- Stage 1 (hypersensitivity): Excitement, hypersensitivity, tetany, fine muscle tremors, shuffling gait. Often unobserved.
- Stage 2 (sternal recumbency): Cow sits in sternal recumbency with S-shaped neck curve, dull, cold extremities, dry muzzle, subnormal temperature (96–100°F), heart rate increased and pulse weak.
- Stage 3 (lateral recumbency): Coma, bloat, death if untreated.
Treatment: IV calcium borogluconate (500 mL of 23% solution given slowly over 10–15 minutes while monitoring heart). SQ/IM calcium solutions for additional dose. Monitor for cardiac arrhythmias during infusion (slow or pause if heart irregularity occurs).
Prevention: Low dietary cation-anion difference (DCAD) diet in dry period (anionic salts). Oral calcium boluses at calving. Ensure vitamin D adequacy.

[Source: Merck Veterinary Manual - Metabolic/Ketosis]
KETOSIS (ACETONEMIA)
Etiology: Negative energy balance (NEB) in early lactation when glucose demand exceeds intake/gluconeogenesis capacity. Fat mobilization produces ketone bodies (BHB, acetone, acetoacetate).
Types:
- Type I (underfeeding): Weeks 2–6 postpartum; thin body condition.
- Type II (fatty liver / overfeeding): Periparturient in overconditioned cows (BCS >3.75 at dry-off).
Clinical Findings: Reduced feed intake, drop in milk production, weight loss, sweet/fruity odor on breath, possible nervous signs (licking, bellowing, incoordination in nervous ketosis).
Diagnosis: Cowside BHB test — blood BHB >1.2 mmol/L = subclinical; >3.0 mmol/L = clinical ketosis. Urine/milk ketone strips useful for screening.
Treatment: IV dextrose (500 mL of 50% dextrose) for rapid correction. Propylene glycol (300–500 mL PO, twice daily for 3–5 days) as oral glucogenic precursor. Dexamethasone for refractory cases. B12 and niacin as adjuncts.
Prevention: Avoid overconditioned cows at dry-off (target BCS 3.0–3.25). Feed propylene glycol preventatively for 14 days pre-calving in high-risk cows.

[Source: Merck Veterinary Manual - Metabolic/Grass Tetany]
HYPOMAGNESEMIA (GRASS TETANY / GRASS STAGGERS)
Etiology: Inadequate magnesium absorption, typically in lactating beef cows grazing lush, rapidly growing pasture in early spring. High potassium and nitrogen in grass impairs Mg absorption.
Clinical Findings: Acute: Sudden onset of excitability, muscle tremors, hypersensitivity to touch/sound, staggering, convulsions, death within hours. Chronic: Reduced appetite, reduced milk, nervousness.
Treatment: IV magnesium sulfate (50% solution, 200–400 mL slowly IV) combined with calcium. Administer with caution — rapid IV can cause cardiac arrest. SQ magnesium given simultaneously for longer effect.
Prevention: Supplement magnesium via feed (magnesium oxide, 60 g/cow/day) or free-choice mineral. Apply dolomitic limestone to pastures. Avoid putting hungry, stressed cattle onto high-risk pastures.

[Source: Merck Veterinary Manual - Metabolic/Acidosis]
RUMINAL ACIDOSIS
Subacute Ruminal Acidosis (SARA):
Definition: Rumen pH 5.5–5.8 for prolonged periods (>3 hours/day). No overt clinical signs but significant production losses and secondary diseases.
Etiology: Excessive rapidly fermentable carbohydrates (starch, sugars) relative to effective fiber in the diet.
Consequences: Laminitis, reduced fiber digestion, reduced milk fat (milk fat depression <3.2%), diarrhea, reduced feed intake variability, liver abscesses.
Diagnosis: Rumenocentesis (pH <5.5 in 1 of 3 cows = herd problem), milk fat analysis, fecal scoring (loose, frothy, undigested grain).

Acute Ruminal Acidosis:
Etiology: Grain overload (access to concentrate without adaptation) or sudden diet change.
Clinical Findings: Profound depression, anorexia, rumen atony, watery diarrhea (may contain undigested grain), dehydration, rumen pH <5.0, staggering gait, recumbency.
Treatment: Remove grain source. Mild cases: sodium bicarbonate drench (1 kg in 20 L water). Moderate: rumen lavage via stomach tube. Severe: rumenotomy to physically remove contents. IV fluids (isotonic saline + bicarbonate) for systemic acidosis. Thiamine (vitamin B1) for polioencephalomalacia prevention.`
  },
  {
    id: "merck-cattle-008",
    name: "Vaccination Protocols Reference: Cattle",
    author: "AABP / USDA APHIS",
    content: `[Source: AABP Vaccination Guidelines - Beef Cattle]
BEEF CATTLE VACCINATION PROTOCOLS

CORE VACCINES (recommended for all herds):

Clostridial (7-way or 8-way — covers C. chauvoei, septicum, novyi, sordellii, perfringens C&D, haemolyticum):
- Calves: First dose at 2–4 months, booster 4 weeks later. Annual booster.
- Cows: Booster 4–6 weeks pre-calving annually to maximize colostral antibodies.

IBR (Infectious Bovine Rhinotracheitis / BHV-1) + BVD (Types 1 & 2) + PI3 + BRSV (modified live virus, MLV):
- Modified live virus preferred for superior immunity.
- Calves (nursing): At 2–4 months of age with booster at weaning.
- Replacement heifers: Vaccinate with MLV before breeding (minimum 30 days before breeding for reproductive safety).
- Cows: Annual booster. Do NOT use MLV in pregnant cows — use killed vaccine only if animal is pregnant.
- High-risk stocker/feedlot cattle: On arrival, use MLV; intranasal IBR/PI3 can be used regardless of pregnancy status.

BRUCELLOSIS (Calfhood Vaccination):
- Heifers 4–12 months of age with RB51 strain vaccine.
- Administered by accredited veterinarian only — state/federal regulations apply.
- Provides USDA-certified status.

Leptospirosis (5-way Lepto: L. pomona, hardjo, grippotyphosa, canicola, icterohaemorrhagiae):
- Cows/heifers: Vaccinate 4–6 weeks pre-breeding. Annual booster, or semi-annual in endemic areas.
- Consider hardjo-bovis specific vaccines in herds with reproductive failure.

Bovine Rotavirus/Coronavirus/E. coli K99 (scours vaccines):
- Cows: 2 doses 8–6 weeks before calving, then annual booster 4–6 weeks pre-calving.
- Passive transfer via colostrum protects neonates.

RESPIRATORY VACCINES — STOCKER/FEEDLOT ARRIVAL PROTOCOL
Day 0 (arrival): MLV BRD vaccine (IBR, BVD1&2, PI3, BRSV) + Clostridial 7-way + Pasteurella/Mannheimia bacterin-toxoid.
Day 14–21: Booster MLV respiratory if initial vaccine was killed. Clostridial booster if not previously vaccinated.

[Source: AABP Vaccination Guidelines - Dairy Cattle]
DAIRY CATTLE VACCINATION PROTOCOLS

Fresh Cow Protocol (at dry-off and pre-calving):
- Clostridial 7-way: Booster at dry-off.
- J5/Re-17 (E. coli bacterin): 2 doses — at dry-off and 2 weeks pre-calving. Reduces severity of coliform mastitis.
- Scours vaccine (rotavirus/coronavirus/E. coli): 2 doses pre-calving as above.
- Leptospirosis: Annually at dry-off.

Calves — Dairy Protocol:
- At birth: Intranasal IBR/PI3 vaccine (safe in neonates, overcomes maternal antibody interference).
- 2–4 months: MLV BRD vaccine + Clostridial 7-way, booster 4 weeks later.
- 4–6 months: Leptospirosis (2 doses, 4 weeks apart).`
  },
  {
    id: "merck-cattle-009",
    name: "Merck Veterinary Manual: Parasitology (Cattle)",
    author: "Merck & Co., Inc.",
    content: `[Source: Merck Veterinary Manual - Parasitology/Internal Parasites]
INTERNAL PARASITES IN CATTLE

KEY PARASITES
Gastrointestinal Nematodes:
- Ostertagia ostertagi (brown stomach worm): Most economically significant GI parasite in North America. Larvae inhibit in gastric glands in late fall (Type II ostertagiasis), causing severe protein-losing enteropathy in spring. Signs: Diarrhea, bottle jaw (submandibular edema), weight loss, reduced milk production.
- Cooperia spp.: Small intestine; primarily in young cattle; reduced growth rate.
- Haemonchus placei (barber pole worm): Abomasum; blood-sucking; signs of anemia and bottle jaw.

Lungworm (Dictyocaulus viviparus):
- Verminous pneumonia — particularly in naïve first-season grazing cattle.
- Signs: Coughing (hoose), dyspnea, tachypnea after rain-associated mass emergence of larvae.

Liver Flukes (Fasciola hepatica):
- Chronic: Biliary hyperplasia, reduced production, poor body condition. Acute: Hemorrhagic hepatitis (rare, with heavy challenge).
- Diagnosis: Fecal sedimentation (eggs are operculated), ELISA, or liver enzyme elevation.
- Treatment: Triclabendazole (effective against all fluke stages including immature). Clorsulon + ivermectin for adult flukes.

ANTHELMINTIC CLASSES
- Benzimidazoles (BZ): Albendazole, fenbendazole. Oral. Effective against adults and some larvae.
- Macrocyclic Lactones (ML): Ivermectin, doramectin, eprinomectin, moxidectin. Injectable, pour-on, or oral. Broad spectrum including external parasites.
- Levamisole (LV): Injectable or pour-on. Narrow spectrum; useful in ML-resistant populations.
- Combination products: BZ + ML used for refugia-based resistance management.

ANTHELMINTIC RESISTANCE MANAGEMENT
- Perform fecal egg count reduction tests (FECRT) to confirm resistance: <95% reduction = resistance suspected.
- Maintain refugia: Never treat 100% of herd. Leave 10–15% of lowest-risk animals untreated to dilute resistant alleles.
- Rotate by mode of action, not by brand name. Rotate based on FECRT results, not on calendar.
- Strategic timing: Treat at housing (fall) to prevent overwinter pasture contamination. Spring treatment at turnout for high-risk youngstock.

FAMACHA SCORING (for Haemonchus-predominant herds):
- Visual scoring of ocular conjunctival color 1–5 (1=red/optimal to 5=white/severely anemic).
- Treat only animals scoring 3–5. Do not treat score 1–2 animals — preserve refugia.
- Requires trained personnel. Validate by periodically checking PCV in scored animals.

[Source: Merck Veterinary Manual - Parasitology/External Parasites]
EXTERNAL PARASITES IN CATTLE

Cattle Lice:
- Sucking lice (Linognathus vituli, Haematopinus eurysternus): Blood-sucking; cause anemia and intense pruritus.
- Chewing/biting lice (Damalinia bovis): Feed on skin debris; less pathogenic.
- Signs: Pruritus, rubbing, hair loss, rough coat, reduced production. Worst in winter (lice are cold-season parasites).
- Treatment: Macrocyclic lactones (injectable ivermectin), synthetic pyrethroids (pour-on), or organophosphates. Treat all animals in herd simultaneously. Repeat in 14 days to kill newly hatched larvae (no product kills eggs).

Mange (Sarcoptic, Psoroptic, Chorioptic):
- Sarcoptic (Sarcoptes scabiei): Burrowing mite; intense pruritus, thick crusted skin lesions; notifiable in some states.
- Psoroptic (Psoroptes bovis): Surface mite; large weeping crusted lesions on neck, topline.
- Chorioptic (Chorioptes bovis): Legs and tail head; least pathogenic.
- Treatment: Macrocyclic lactones (2 injections 14 days apart for most mites). Psoroptic mange may require longer treatment.

Horn Flies (Haematobia irritans):
- 20–40 blood meals/day; threshold for treatment = >200 flies/animal.
- Control: Insecticide ear tags (pyrethroid or organophosphate), pour-on pyrethroids, back rubbers, ivermectin.
- Rotate insecticide class annually to manage resistance.

Face Flies (Musca autumnalis):
- Vector for Moraxella bovis (cause of infectious bovine keratoconjunctivitis / pinkeye).
- Control: Insecticide ear tags, dust bags, face fly traps.`
  },
  {
    id: "merck-cattle-010",
    name: "Drug Withdrawal Times Reference: Cattle",
    author: "FDA CVM / FARAD",
    content: `[Source: FARAD Drug Withdrawal Reference - Cattle]
DRUG WITHDRAWAL TIMES — BEEF & DAIRY CATTLE
IMPORTANT: Withdrawal times listed are label minimums under standard dosing. Extralabel use (different dose, route, or species) requires veterinary guidance and may significantly extend withdrawal times. Contact FARAD (1-888-873-2723) for extralabel withdrawal estimates.

ANTIBIOTICS — BEEF CATTLE (meat withdrawal)
- Penicillin G (procaine, 6,600 IU/kg IM): Meat 10 days. Milk: 48–96 hours (product dependent). Not approved in dairy cattle at certain doses.
- Oxytetracycline (LA-200, 20 mg/kg IM): Meat 28 days. Milk: not approved for lactating dairy cattle at this dose.
- Ceftiofur (Excenel, 2.2 mg/kg IM): Meat 3 days. Milk: 0 days (Spectramast LC: 72 hours).
- Tulathromycin (Draxxin, 2.5 mg/kg SC): Meat 18 days. Not for use in dairy cattle >20 months.
- Florfenicol (Nuflor, 40 mg/kg SC): Meat 38 days (single dose). Not approved for dairy cattle.
- Enrofloxacin (Baytril, 7.5–12.5 mg/kg SC): Meat 28 days. NOT FOR USE IN DAIRY CATTLE — prohibited by FDA.
- Tilmicosin (Micotil, 10 mg/kg SC): Meat 28 days. NOT APPROVED FOR DAIRY. CAUTION: Fatal if injected in humans or swine.
- Gamithromycin (Zactran, 6 mg/kg SC): Meat 35 days. Not for lactating dairy cattle.

ANTIBIOTICS — DAIRY CATTLE (milk withdrawal)
- Ceftiofur (Spectramast LC intramammary): Milk 72 hours, meat 16 days.
- Pirlimycin (Pirsue intramammary): Milk 36 hours (9 milkings), meat 9 days.
- Cloxacillin (Dry Cow intramammary, dry cow use): Must not be used within 28 days of calving. Milk withhold: 28 days post-calving minimum.
- Amoxicillin (Amoxi-Mast intramammary): Milk 60 hours, meat 12 days.

NSAIDs (Non-Steroidal Anti-Inflammatory Drugs)
- Flunixin meglumine (Banamine, 2.2 mg/kg IV): Meat 4 days. Milk 36 hours (dairy cattle, label dose IV only).
- Ketoprofen (Ketofen, 3 mg/kg IV/IM): Meat 7 days (extralabel). Milk: extralabel withdrawal, consult FARAD.
- Meloxicam (extralabel in US): Meat 10–14 days (extralabel estimate). Consult FARAD.
- Aspirin (oral): Meat 1 day. Milk: 24–48 hours.

PARASITICIDES
- Ivermectin injectable (200 mcg/kg SC): Meat 35 days. NOT approved for use in lactating dairy cattle.
- Ivermectin pour-on: Meat 48 days. NOT approved for lactating dairy.
- Eprinomectin pour-on (Eprinex): Meat 0 days. Milk 0 days — APPROVED for lactating dairy cattle.
- Doramectin injectable: Meat 35 days. Not for dairy.
- Clorsulon (Curatrem, for liver flukes): Meat 8 days. Not approved for dairy.
- Fenbendazole (Panacur, Safe-Guard): Meat 8 days. Milk 0 days (approved for lactating dairy).
- Albendazole: Meat 27 days. NOT FOR USE IN DAIRY. DO NOT USE IN FIRST 45 DAYS OF PREGNANCY (teratogenic).

HORMONES & OTHER
- Dexamethasone (injectable): Meat 0–3 days (product dependent). Milk 72 hours. Do not use in pregnant animals — causes abortion.
- Oxytocin: No established withdrawal. Meat and milk considered negligible.
- Prostaglandin F2α (Lutalyse): Meat 1 day. Milk 0 days.
- GnRH (Factrel, Cystorelin): No withdrawal required.
- Propylene glycol (oral): No withdrawal required. GRAS (Generally Recognized as Safe).`
  },
  {
    id: "merck-cattle-011",
    name: "Body Condition Scoring Guide: Dairy & Beef Cattle",
    author: "Penn State Extension / Purdue University",
    content: `[Source: Penn State Extension - Body Condition Scoring Guide]
BODY CONDITION SCORING (BCS) — CATTLE
Scale: 1 (emaciated) to 5 (obese) in 0.25-point increments for dairy; 1–9 scale used in beef (converted below).

DAIRY CATTLE BCS — Key Anatomical Reference Points
Evaluate: Tailhead/pin bones, thurls, short ribs, backbone (lumbar vertebrae), ribs.

Score 1.0 (Emaciated):
- All bones extremely prominent and easily visible from a distance.
- Deep cavities around tailhead and pin bones. No fatty tissue palpable anywhere.
- Animal is severely debilitated. Immediate nutritional intervention required.

Score 2.0 (Thin):
- Backbone, ribs, and pin bones visually prominent.
- Slight depression around tailhead. Some muscle definition visible.
- Unacceptable for cows entering any production stage.

Score 2.5:
- Ribs visible but not individually prominent.
- Tailhead depression present but shallow. First sacral vertebra palpable.
- Acceptable for mid-to-late lactation only.

Score 3.0 (Ideal for most stages):
- Ribs felt with light pressure but not visible.
- Tailhead has small amount of fatty tissue; pin bones felt but not prominent.
- Target at: mid-lactation, dry-off, breeding.

Score 3.25–3.5 (Target at dry-off and calving):
- Slight fat covering over ribs; individual ribs require firm pressure to feel.
- Tailhead area has obvious fat fill.
- Target BCS at dry-off: 3.25–3.5. Target at calving: 3.0–3.25.
- Cows >3.5 at calving have elevated risk of ketosis and fatty liver.

Score 4.0 (Fat):
- Ribs not palpable. Large fat deposits over tailhead, loin, and brisket.
- Associated with metabolic disease risk at calving.

Score 5.0 (Obese):
- Completely covered in fat. Animal structurally distorted. Mobility impaired.
- Rare in field conditions. Serious welfare concern.

KEY BCS TARGETS BY STAGE (Dairy):
- Early lactation (0–60 DIM): 2.5–3.0 (acceptable loss of ≤0.5 BCS units from calving)
- Mid-lactation (60–200 DIM): 2.75–3.25 (regaining condition)
- Late lactation (>200 DIM): 3.0–3.5
- Dry-off: 3.25–3.5
- Calving: 3.0–3.25

BODY CONDITION SCORING — BEEF CATTLE (1–9 scale)
Score 1: Emaciated. All bones visible. No muscle mass. Near death.
Score 2: Very thin. Some muscle mass but no subcutaneous fat.
Score 3: Thin. Ribs easily visible. Hindquarters sunken.
Score 4: Borderline. Ribs noticeable but not prominent. Some fat over loin.
Score 5: Moderate (ideal). Ribs not visible. Good muscle. Brisket shows minimal fat.
Score 6: Good. Fat cover over ribs and around tailhead. Brisket fill evident.
Score 7: Fat. Soft fat over ribs. Patchy fat around tailhead.
Score 8: Obese. Fat deposits over ribs and brisket. Tailhead buried in fat.
Score 9: Very obese. Mobility impaired. Massive fat deposits throughout.

KEY BCS TARGETS (Beef):
- Cows at calving: 5–6 (heifers: 5–5.5)
- Cows at breeding: 5–6 (allow 60 days post-calving for rebreeding)
- Cows at weaning: ≥5
- Thin cows (BCS ≤4) at calving have significantly reduced rebreeding rates (>20% reduction in conception).

PRACTICAL BCS USE
- Score entire herd at: dry-off, calving, 60 DIM, mid-lactation, and pre-breeding.
- Identify outliers: cows losing >1 BCS unit in 60 days need nutritional and health investigation.
- Herd-level benchmarking: If >15% of cows score <2.5 at any point, review nutrition program.
- BCS changes lag 2–4 weeks behind dietary changes — adjust early.`
  }
];

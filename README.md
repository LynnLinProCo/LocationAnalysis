# Location Analysis
Quantitatively Evaluate Spatial Efficiency in patient-to-clinic scheduling across In-state (GA) Clinics.

## Executive Summary

This study examines whether patients are being scheduled at the geographically optimal clinics and how travel distance affects appointment adherence. Using cleaned geospatial data from 2023–2025, we found that only 62.09% of patients were assigned to their nearest clinic, with an average optimal travel distance of 9.17 km (5.70 miles). A preliminary Pearson correlation analysis revealed that distance had a negligible influence on appointment attendance from 2023–2025 (R² = 0.044), but this relationship strengthened to a moderate R² = 0.3495 in 2025 alone, suggesting that historical data may obscure present-day behavioral trends. 

| **R² Range** | **Strength of Relationship** | **Interpretation** |
|---------------|-------------------------------|--------------------|
| 0.00 – 0.10 | Very Weak | Distance has almost no effect; other factors dominate. |
| 0.10 – 0.30 | Weak | Distance shows minor influence on appointment behavior. |
| 0.30 – 0.50 | Moderate | Distance moderately affects appointment attendance. |
| 0.50 – 0.70 | Strong | Distance strongly predicts appointment outcomes. |
| 0.70 – 1.00 | Very Strong | Distance nearly fully explains appointment behavior. |

Table 1: Reference to the metric R². R² (pronounced “R-squared”) tells you how much of the change in one thing can be "causing" another thing to happen. In this case, we are evaluating whether increase in distance has an effect on patient showing up at a clinic.

## Data Cleaning
Ensure all records reflect valid, geospatially mappable entities within GA.

## 1. Data Pre-Processing and Cleaning

**Goal:** Ensure all records reflect valid, geospatially mappable entities within Georgia state (GA).  
**Source:** NexGen SQL-based EHR system (SSMS).

**Filters Applied:**
- Retained only entries where `Home State = 'GA'`
- ZIP codes restricted to exactly five digits using RegEx `^\d{5}$`
- Removed null, empty, or malformed ZIPs
- Excluded records with missing or non-finite values in:
  - `Home Edit.Latitude`
  - `Home Edit.Longitude`
  - `Clinic Edit.Latitude`
  - `Clinic Edit.Longitude`

---

### **Data Cleaning Summary**

| Metric | Count |
|---------|-------:|
| **Total Rows** | 54,133 |
| **Invalid State (not GA)** | 2,477 |
| **Invalid ZIP (non-5 digits)** | 2,052 |
| **Missing ZIP** | 1,792 |
| **Valid Rows After Cleaning** | 51,336 |

**Overall Error Rate:** `5.16%`

The 5.16% error rate primarily results from incomplete or malformed demographic data. When integrating demographic data from the NexGen system via SQL scripts, validation should occur at the **data entry** or **ETL** stage.  

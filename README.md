# Location Analysis
Quantitatively Evaluate Spatial Efficiency in patient-to-clinic scheduling across In-state (GA) Clinics.
<img width="1312" height="737" alt="Screenshot 2025-10-27 at 5 23 35 PM" src="https://github.com/user-attachments/assets/772c3270-9ffd-455b-81b9-2a619c0330fd" />

https://app.powerbi.com/view?r=eyJrIjoiODkwMjIzMDItMjA4MS00NmY2LWE4NzUtY2EzY2NhNDkzNzY1IiwidCI6IjljZjYyODBiLTg1NWYtNGY5Ni1iZDJiLTU1Y2MzMjBkNmJhYyIsImMiOjJ9

## Executive Summary

This study examines whether patients are being scheduled at the geographically optimal clinics and how travel distance affects appointment adherence. Using cleaned geospatial data from 2023–2025, we found that only 62.09% of patients were assigned to their nearest clinic, with an average optimal travel distance of 9.17 km (5.70 miles). A preliminary Pearson correlation analysis revealed that distance had a negligible influence on appointment attendance from 2023–2025 (R² = 0.044), but this relationship strengthened to a moderate R² = 0.3495 in 2025 alone, suggesting that historical data may obscure present-day behavioral trends. 

Note: 9.17 km is a theoretical lower bound → “If every patient went to their nearest clinic, the average trip would be 9.17 km.” The current real average is 14.02 km, which is about 8.7 miles. 

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


## 2. Nearest-Clinic Distance Computation

Algorithm: k-Nearest Neighbor search via cKDTree (SciPy)
<img width="1313" height="736" alt="Screenshot 2025-10-27 at 5 23 26 PM" src="https://github.com/user-attachments/assets/0836b29a-b667-41e0-87c0-33963ca57507" />


Each patient’s home coordinates were compared against all unique clinic coordinates.
The cKDTree structure allows O(log n) nearest neighbor searches, efficiently identifying the closest clinic.
For each patient i:
<img width="369" height="55" alt="image" src="https://github.com/user-attachments/assets/421247a3-f1ef-47ab-bcda-f0903fa6a818" />

Distances were calculated geodesically (WGS84 ellipsoid) via Geopy to yield accurate kilometer-based values.
## 3. Interpretation

The 62.09 % OSR indicates that 37.91 % of patients could be reassigned to a closer clinic through 23-25, suggesting potential inefficiencies in scheduling algorithms or possible capacity overloads. The 9.17 km mean nearest-clinic distance establishes a geographic benchmark for expected patient travel radius in GA.

## 4. Recommendations for Next Steps

Conduct cluster density analysis (K-Means or DBSCAN) to validate whether clinic locations align with patient population centers.

Implement load balancing metrics to prevent overutilization of geographically central clinics.


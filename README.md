# LocationAnalysis
Quantitatively Evaluate Spatial Efficiency in patient-to-clinic scheduling across In-state (GA) Clinics.

## Executive Summary

This study examines whether patients are being scheduled at the geographically optimal clinics and how travel distance affects appointment adherence. Using cleaned geospatial data from 2023–2025, we found that only 62.09% of patients were assigned to their nearest clinic, with an average optimal travel distance of 9.17 km (5.70 miles). A preliminary Pearson correlation analysis revealed that distance had a negligible influence on appointment attendance from 2023–2025 (R² = 0.044), but this relationship strengthened to a moderate R² = 0.3495 in 2025 alone, suggesting that historical data may obscure present-day behavioral trends. These findings emphasize the importance of time-specific modeling when evaluating spatial efficiency and patient compliance patterns.

| **R² Range** | **Strength of Relationship** | **Interpretation** |
|---------------|-------------------------------|--------------------|
| 0.00 – 0.10 | Very Weak | Distance has almost no effect; other factors dominate. |
| 0.10 – 0.30 | Weak | Distance shows minor influence on appointment behavior. |
| 0.30 – 0.50 | Moderate | Distance moderately affects appointment attendance. |
| 0.50 – 0.70 | Strong | Distance strongly predicts appointment outcomes. |
| 0.70 – 1.00 | Very Strong | Distance nearly fully explains appointment behavior. |

Table 1: Reference to the metric R². R² (pronounced “R-squared”) tells you how much of the change in one thing can be "causing" another thing to happen. In this case, we are evaluating whether increase in distance has an effect on patient showing up at a clinic.


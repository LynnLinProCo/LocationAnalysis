# Data Cleaning
Using ```python spyder```, first, I summarized what kind of invalid, missing data there could be. 
## Statistical Validation of Error Rate

After reviewing invalid and missing data (excluding duplicate accounts), we observed an overall **error rate of 5.16%** across **~500,000 rows**.  
The cleaning process for duplicated account is thus deferred until the data lake is stabilized under the **Mendelion data architecture**.

### Using the Central Limit Theorem (CLT)
**Formula:**  
Error Rate = (Invalid State + Invalid ZIP + Missing ZIP) / Total Rows

**Calculation:**  
Error Rate = (2,477 + 2,052 + 1,792) ÷ 54,133 = **0.0516 (≈ 5.16%)**

---

### **Central Limit Theorem Justification**

Because our dataset contains more than 50,000 rows, the **Central Limit Theorem (CLT)** allows us to assume the sample error rate follows an approximately normal distribution.  
We can estimate the standard error (SE) and confidence interval for the true population error rate.

**Standard Error (SE):**  
SE = sqrt( p * (1 - p) / n )  
= sqrt( 0.0516 * (1 - 0.0516) / 54,133 )  
= **0.00094**

**95% Confidence Interval:**  
5.16% ± 1.96 × 0.094% → **(5.0%, 5.3%)**

---

### **Interpretation**

The 5.16% observed error rate is statistically stable, with a margin of error of only ±0.18%.  
This suggests our estimate of data quality is highly reliable even before large-scale cleaning through the **Mendelion data architecture**.  

```python
import pandas as pd

df = pd.read_csv('analysis.csv')

# --- Create flags ---
invalid_state = df['Home Stat'] != 'GA'
invalid_zip = ~df['Home'].astype(str).str.match(r'^\d{5}$', na=False)
missing_zip = df['Home'].isna() | (df['Home'].astype(str).str.strip() == '')

# --- Count issues ---
summary = {
    'Total rows': len(df),
    'Invalid state (not GA)': invalid_state.sum(),
    'Invalid ZIP (non-5 digits)': invalid_zip.sum(),
    'Missing ZIP': missing_zip.sum()
}

# --- Filter cleaned data ---
clean_df = df[~(invalid_state | invalid_zip | missing_zip)]

summary['Valid rows after cleaning'] = len(clean_df)

print("\n--- Data Cleaning Summary ---")
for k, v in summary.items():
    print(f"{k}: {v}")

clean_df.to_csv('cleaned_data.csv', index=False)
print("\nCleaned dataset exported to 'cleaned_data.csv'")
```

import pandas as pd
from scipy.spatial import cKDTree
from geopy.distance import geodesic

# --- Load cleaned data ---
df = pd.read_csv('cleaned_data.csv')

invalid_state = df['Home State'] != 'GA'
invalid_zip = ~df['Home'].astype(str).str.match(r'^\d{5}$', na=False)
missing_zip = df['Home'].isna() | (df['Home'].astype(str).str.strip() == '')

# Remove rows with missing lat/long values
missing_coords = df[['Home Edit.Latitude', 'Home Edit.Longitude', 
                     'Clinic Edit.Latitude', 'Clinic Edit.Longitude']].isna().any(axis=1)

clean_df = df[~(invalid_state | invalid_zip | missing_zip | missing_coords)]

print(f"Valid rows after cleaning: {len(clean_df)}")

# --- Convert coordinates to float and ensure finite values ---
clean_df = clean_df.astype({
    'Home Edit.Latitude': 'float',
    'Home Edit.Longitude': 'float',
    'Clinic Edit.Latitude': 'float',
    'Clinic Edit.Longitude': 'float'
})

# --- Build coordinate arrays ---
patient_coords = clean_df[['Home Edit.Latitude', 'Home Edit.Longitude']].to_numpy()
clinic_coords = clean_df[['Clinic Edit.Latitude', 'Clinic Edit.Longitude']].drop_duplicates().to_numpy() #drop duplicated clinics

# --- Find nearest clinic for each patient ---
tree = cKDTree(clinic_coords)
dist, idx = tree.query(patient_coords, k=1)

# --- Add nearest clinic + distance ---
clean_df['NearestClinicLat'] = clinic_coords[idx][:, 0]
clean_df['NearestClinicLon'] = clinic_coords[idx][:, 1]
clean_df['NearestClinicDist_km'] = [
    geodesic(p, c).km for p, c in zip(patient_coords, clinic_coords[idx])
]

# --- Compare actual vs. nearest ---
clean_df['IsOptimal'] = (
    (clean_df['Clinic Edit.Latitude'] == clean_df['NearestClinicLat']) &
    (clean_df['Clinic Edit.Longitude'] == clean_df['NearestClinicLon'])
)
optimal_rate = clean_df['IsOptimal'].mean() #using mean to compare

print(f"\nOptimal scheduling rate: {optimal_rate:.2%}")
print(f"Average patient-to-nearest-clinic distance: {clean_df['NearestClinicDist_km'].mean():.2f} km")

clean_df.to_csv('clinic_optimization_results.csv', index=False)
print("\nResults exported to 'clinic_optimization_results.csv'")

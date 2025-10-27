# Data Extraction
Relational data queries. A raw data file extracts appointment records without historical context, while a wrangled data file links to the raw data to enable visualizations: 1) patient paths, distribution, and travel distance; 2) central heatmap showing clinic congestion.
<img width="806" height="705" alt="image" src="https://github.com/user-attachments/assets/96060be6-3593-4e32-8a6e-1795ce89f2c2" />


## Raw Appointment Data
```sql
SELECT person_nbr AS [Patient ID],
location_name AS [Location],
appt_date AS [Appointment Date],
sub.create_timestamp AS [Created Time],
p.zip AS [Home],
LEFT(lm.zip, 5) AS [Clinic],
appt_kept_ind AS [Appointment Status],
p.state AS [Home State] FROM(

  SELECT
    person_id,
    location_id,
    appt_date,
    create_timestamp,
    appt_kept_ind,
    ROW_NUMBER() OVER ( --window function to select the first ever appointment
      PARTITION BY person_id
      ORDER BY create_timestamp ASC
    ) AS rn
  FROM appointments
  WHERE appt_type = 'U' --appointment type U means the appointment contains the latest update 
) sub
LEFT JOIN person p ON p.person_id = sub.person_id
LEFT JOIN location_mstr lm ON lm.location_id = sub.location_id
WHERE rn = 1 AND person_nbr is not null AND YEAR(appt_date)>2022;
```
## Wrangled Data Power BI Scripting
## Getting Longitude and Latitude data via Webscrapping
## Calculating distance

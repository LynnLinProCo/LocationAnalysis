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

## Getting Longitude and Latitude data via Webscrapping
```power bi
let
    Source = (zip as text) =>
        let
            url = "https://nominatim.openstreetmap.org/search?country=us&postalcode=" & zip & "&format=json",
            response = Json.Document(Web.Contents(url, [Headers=[#"User-Agent"="PowerBI-Geocoder"]])),
            first = if List.Count(response) > 0 then response{0} else null,
            lat = if first <> null then first[lat] else null,
            lon = if first <> null then first[lon] else null,
            result = if first <> null then [Zip=zip, Latitude=lat, Longitude=lon] else [Zip=zip, Latitude=null, Longitude=null]
        in
            result
in
    Source
```
After making the above query to make a function, invoke the function in the original data query:
```power bi
   #"Added Custom1" = Table.AddColumn(#"Added Custom", "Clinic Edit", each fnGetLatLon([Clinic])),
```
## Calculating distance
```DAX
let
    R = 6371,  // Earth's radius in km
    lat1 = [Home Edit.Latitude] * Number.PI / 180,
    lon1 = [Home Edit.Longitude] * Number.PI / 180,
    lat2 = [Clinic Edit.Latitude] * Number.PI / 180,
    lon2 = [Clinic Edit.Longitude] * Number.PI / 180,
    dLat = lat2 - lat1,
    dLon = lon2 - lon1,
    a = Number.Sin(dLat / 2) * Number.Sin(dLat / 2) +
        Number.Cos(lat1) * Number.Cos(lat2) *
        Number.Sin(dLon / 2) * Number.Sin(dLon / 2),
    c = 2 * Number.Atan2(Number.Sqrt(a), Number.Sqrt(1 - a)),
    distance = R * c
in
    distance
```

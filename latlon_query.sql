--Step 4 (optional, only needed if you're using files that already have lat/long)
--The next step will check for nulls in lat/long. Also checks for lat/long that shifted since last time based on address. 
--It does not check lat/long of new policies. 
--create table of distinct policies from last quarter with lat, long, street, city, and postal code
CREATE VIEW my_address_check AS
SELECT DISTINCT LocationID, ContractID, Street, City, PostalCode, Area, Latitude, Longitude, LOB, BuildingValue, OtherValue, ContentsValue, TimeElementValue
    FROM [2020Q4_ImportFiles_AIR]..[T2020Q4_AIR_012_Advance_FFWT_TOHU]  
--join it to table of policies from this quarter
CREATE VIEW my_temp_policy_match AS
SELECT a.ContractID, a.LocationID AS CurrentQuarterID, b.LocationID AS PreviousQuarterID, a.Latitude AS CurrentQuarterLat, b.Latitude AS PreviousQuarterLat, a.Longitude AS CurrentQuarterLon,
        b.Longitude AS PreviousQuarterLon, a.Street,  a.City, a.PostalCode, a.Area, a.LOB as CurrentLOB, b.LOB AS  PreviousLOB,
        (a.BuildingValue + a.OtherValue + a.ContentsValue + a.TimeElementValue) AS ValueCurrent, 
        (b.BuildingValue + b.OtherValue + b.ContentsValue + b.TimeElementValue) AS ValuePrevious
        FROM [2021Q1_ImportFiles_AIR]..[T2021Q1_AIR_012_Advance_FFWT_TOHU] a
LEFT JOIN my_address_check b 
ON (a.ContractID = b.ContractID AND a.Street = b.Street AND a.City = b.City and a.Area = b.Area)
--count nulls this quarter vs last quarter
SELECT COUNT(*) FROM my_temp_policy_match WHERE CurrentQuarterLat IS NULL OR CurrentQuarterLon IS NULL
SELECT COUNT(*) FROM my_temp_policy_match WHERE PreviousQuarterLat IS NULL OR PreviousQuarterLon IS NULL
--create temp table with unequal latlon
CREATE VIEW my_unequal_latlon AS (
SELECT *, geography::Point(CurrentQuarterLat, CurrentQuarterLon, 4326) AS CurrentPoint, 
          geography::Point(PreviousQuarterLat, PreviousQuarterLon, 4326) AS PastPoint
FROM my_temp_policy_match WHERE CurrentQuarterLat<>PreviousQuarterLat OR CurrentQuarterLon<>PreviousQuarterLon 
                          AND PreviousQuarterLat IS NOT NULL AND CurrentQuarterLat IS NOT NULL AND PreviousQuarterLon IS NOT NULL AND CurrentQuarterLon IS NOT NULL)
--check distance
WITH t AS (
    SELECT *, CurrentPoint.STDistance(PastPoint) as dist FROM my_unequal_latlon)
SELECT * FROM t 
ORDER BY dist DESC
DROP VIEW my_address_check
DROP VIEW my_temp_policy_match
DROP VIEW my_unequal_latlon

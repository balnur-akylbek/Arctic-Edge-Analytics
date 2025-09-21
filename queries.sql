-- Show first 10 skaters with details
SELECT * FROM scraped_skater_details
LIMIT 10;

-- Events sorted by date
SELECT "Event", "Level", "Gender", "Event_Date"
FROM scraped_event_details
ORDER BY "Event_Date" ASC;

-- Average number of skaters per event level
SELECT e."Level", COUNT(s."skater_detail_id") AS skater_count
FROM scraped_skater_details s
JOIN scraped_event_details e 
    ON s."Event_Index" = e."Event_Index"
GROUP BY e."Level";


-- Count of skaters per region
SELECT e."Region", COUNT(s."skater_detail_id") AS skater_count
FROM scraped_skater_details s
JOIN scraped_event_details e 
    ON s."Event_Index" = e."Event_Index"
GROUP BY e."Region";
 
-- Min and Max technical scores by event
SELECT e."Event", MIN(t."PanelScores_Technical") AS min_score, MAX(t."PanelScores_Technical") AS max_score
FROM scraped_technical_scores t
JOIN scraped_event_details e 
    ON t."Event_Index" = e."Event_Index"
GROUP BY e."Event";

 

-- Average component score by event
SELECT e."Event", AVG(c."PanelScores_PC") AS avg_component_score
FROM scraped_component_scores c
JOIN scraped_event_details e 
    ON c."Event_Index" = e."Event_Index"
GROUP BY e."Event";


-- Compare technical and component scores by level
SELECT e."Level", 
       AVG(t."PanelScores_Technical") AS avg_technical, 
       AVG(c."PanelScores_PC") AS avg_component
FROM scraped_skater_details s
JOIN scraped_event_details e ON s."Event_Index" = e."Event_Index"
JOIN scraped_technical_scores t ON s."Event_Index" = t."Event_Index" AND s."skater_detail_id" = t."Skater_Placement"
JOIN scraped_component_scores c ON s."Event_Index" = c."Event_Index" AND s."skater_detail_id" = c."Skater_Placement"
GROUP BY e."Level";
 

-- Number of officials by country/state
SELECT o."Official_StateOrCountry", COUNT(o."Event_Index") AS officials_count
FROM scraped_official_details o
GROUP BY o."Official_StateOrCountry"
ORDER BY officials_count DESC;


-- Regions with their states/countries
SELECT e."Region", l."Official_StateOrCountry"
FROM scraped_event_details e
JOIN supplementaldata_officiallocations l 
    ON e."Event_Index" = l."id";


-- Average GOE score by event
SELECT e."Event", AVG(t."GOE") AS avg_goe
FROM scraped_technical_scores t
JOIN scraped_event_details e 
    ON t."Event_Index"= e."Event_Index"
GROUP BY e."Event";


import psycopg2
import pandas as pd

# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="dv_db",
    user="postgres",          # замени на своего пользователя
    password="your_password", # укажи пароль
    host="127.0.0.1",
    port="5432"
)

queries = {
    "first_10_skaters": """
        SELECT * FROM scraped_skater_details
        LIMIT 10;
    """,
    "events_by_date": """
        SELECT "Event", "Level", "Gender", "Event_Date"
        FROM scraped_event_details
        ORDER BY "Event_Date" ASC;
    """,
    "avg_skaters_per_level": """
        SELECT e."Level", COUNT(s."skater_detail_id") AS skater_count
        FROM scraped_skater_details s
        JOIN scraped_event_details e 
            ON s."Event_Index" = e."Event_Index"
        GROUP BY e."Level";
    """,
    "skaters_per_region": """
        SELECT e."Region", COUNT(s."skater_detail_id") AS skater_count
        FROM scraped_skater_details s
        JOIN scraped_event_details e 
            ON s."Event_Index" = e."Event_Index"
        GROUP BY e."Region";
    """,
    "min_max_technical_scores": """
        SELECT e."Event", MIN(t."PanelScores_Technical") AS min_score, MAX(t."PanelScores_Technical") AS max_score
        FROM scraped_technical_scores t
        JOIN scraped_event_details e 
            ON t."Event_Index" = e."Event_Index"
        GROUP BY e."Event";
    """,
    "avg_component_score": """
        SELECT e."Event", AVG(c."PanelScores_PC") AS avg_component_score
        FROM scraped_component_scores c
        JOIN scraped_event_details e 
            ON c."Event_Index" = e."Event_Index"
        GROUP BY e."Event";
    """,
    "compare_scores_by_level": """
        SELECT e."Level", 
               AVG(t."PanelScores_Technical") AS avg_technical, 
               AVG(c."PanelScores_PC") AS avg_component
        FROM scraped_skater_details s
        JOIN scraped_event_details e ON s."Event_Index" = e."Event_Index"
        JOIN scraped_technical_scores t ON s."Event_Index" = t."Event_Index" AND s."skater_detail_id" = t."Skater_Placement"
        JOIN scraped_component_scores c ON s."Event_Index" = c."Event_Index" AND s."skater_detail_id" = c."Skater_Placement"
        GROUP BY e."Level";
    """,
    "officials_by_country": """
        SELECT o."Official_StateOrCountry", COUNT(o."Event_Index") AS officials_count
        FROM scraped_official_details o
        GROUP BY o."Official_StateOrCountry"
        ORDER BY officials_count DESC;
    """,
    "regions_with_states": """
        SELECT e."Region", l."Official_StateOrCountry"
        FROM scraped_event_details e
        JOIN supplementaldata_officiallocations l 
            ON e."Event_Index" = l."id";
    """,
    "avg_goe_by_event": """
        SELECT e."Event", AVG(t."GOE") AS avg_goe
        FROM scraped_technical_scores t
        JOIN scraped_event_details e 
            ON t."Event_Index"= e."Event_Index"
        GROUP BY e."Event";
    """
}

# Выполнение всех запросов
for name, query in queries.items():
    print(f"\n=== {name} ===")
    df = pd.read_sql(query, conn)
    print(df.head(15))   # покажем первые строки результата
    df.to_csv(f"{name}.csv", index=False)

conn.close()

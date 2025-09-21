# ❄️ Arctic Edge Analytics — Figure Skating Insights

## 🏢 Company Overview
**Arctic Edge Analytics** is a sports data company specializing in figure skating statistics and data visualization.  
✨ Our mission is to uncover key trends in competitions, analyze athlete performance, and deliver insights for coaches, federations, and fans.  

---

## 📊 Project Overview
This project focuses on analyzing official figure skating competition data.  
The database captures details about events, judging scores, skater performances, and regional information.  

Main areas of analytics:
- 📌 Number of competitions by region  
- ⛸️ Average skater age by level  
- 🏅 Highest technical and component scores  
- 🌍 Judges’ distribution by state/country  
- 📈 Trends in participation and results over time  

---

## 🗂️ ER Diagram
<img width="819" height="558" alt="image" src="https://github.com/user-attachments/assets/aa0582a5-646e-495c-92cc-67699475082f" />


The database contains 6 related tables:  
- `scraped_event_details` — event details (date, level, category, region)  
- `scraped_official_details` — judges (name, city, state/country)  
- `scraped_component_scores` — program component scores (J1–J9, panel score)  
- `scraped_skater_details` — skaters (name, age, gender, level)  
- `scraped_technical_scores` — technical scores (GOE, elements, total)  
- `supplementaldata_officiallocations` — reference table for regions and states/countries  

---

## 🛠️ Tools & Resources
- **PostgreSQL** — relational database  
- **Python** (`psycopg2`, `SQLAlchemy`) — query execution and analysis  
- **Apache Superset** — data visualization  
- **GitHub** — code and documentation hosting  
- **Dataset** — scraped competition data (officials, skaters, scores, events)  

---

## 🚀 Instructions

### 1. Clone the repository
```bash
git clone https://github.com/balnur-akylbek/ice-skating-analytics
cd ice-skating-analytics

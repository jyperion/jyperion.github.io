import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def fetch_scholar_stats():
    url = "https://scholar.google.co.in/citations?user=TkuE3UgAAAAJ&hl=en"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract citation stats
        stats = {}
        stats_table = soup.find('table', {'id': 'gsc_rsb_st'})
        if stats_table:
            rows = stats_table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 3:  # Make sure we have all columns
                    metric = cols[0].text.strip()
                    all_time = cols[1].text.strip()
                    since_2019 = cols[2].text.strip()
                    stats[metric] = all_time
                    stats[f"{metric}_recent"] = since_2019

        # Get total number of publications
        pub_count = len(soup.find_all('tr', {'class': 'gsc_a_tr'}))
        stats['Publications'] = str(pub_count)
        
        # Add last updated timestamp
        stats['last_updated'] = datetime.utcnow().isoformat()
        
        return stats
    except Exception as e:
        print(f"Error fetching scholar stats: {e}")
        return None

def update_research_page(stats):
    if not stats:
        return False
        
    try:
        with open('publications.html', 'r', encoding='utf-8') as file:
            content = file.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Update citation metrics
        metrics_div = soup.find('div', {'class': 'citation-metrics'})
        if metrics_div:
            # Update Total Citations
            total_citations = metrics_div.find('div', {'class': 'metric-card'})
            if total_citations:
                all_time = total_citations.find('div', {'class': 'metric-total'}).find('span', {'class': 'number'})
                since_2019 = total_citations.find('div', {'class': 'metric-recent'}).find('span', {'class': 'number'})
                if all_time and since_2019:
                    all_time.string = stats.get('Citations', '0')
                    # You'll need to extract the "Since 2019" value from the Google Scholar page

            # Update h-index
            h_index = metrics_div.find_all('div', {'class': 'metric-card'})[1]
            if h_index:
                all_time = h_index.find('div', {'class': 'metric-total'}).find('span', {'class': 'number'})
                since_2019 = h_index.find('div', {'class': 'metric-recent'}).find('span', {'class': 'number'})
                if all_time and since_2019:
                    all_time.string = stats.get('h-index', '0')
                    # You'll need to extract the "Since 2019" value

            # Update i10-index
            i10_index = metrics_div.find_all('div', {'class': 'metric-card'})[2]
            if i10_index:
                all_time = i10_index.find('div', {'class': 'metric-total'}).find('span', {'class': 'number'})
                since_2019 = i10_index.find('div', {'class': 'metric-recent'}).find('span', {'class': 'number'})
                if all_time and since_2019:
                    all_time.string = stats.get('i10-index', '0')
                    # You'll need to extract the "Since 2019" value

        # Write updated content back to file
        with open('publications.html', 'w', encoding='utf-8') as file:
            file.write(str(soup))
            
        return True
    except Exception as e:
        print(f"Error updating publications page: {e}")
        return False

if __name__ == "__main__":
    stats = fetch_scholar_stats()
    print(stats)
    if stats:
        success = update_research_page(stats)
        if success:
            print("Successfully updated research page with new stats")
        else:
            print("Failed to update research page")
    else:
        print("Failed to fetch scholar stats")

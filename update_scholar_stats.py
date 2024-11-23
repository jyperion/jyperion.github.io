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
                if len(cols) >= 2:
                    metric = cols[0].text.strip()
                    all_time = cols[1].text.strip()
                    stats[metric] = all_time

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
        with open('research.html', 'r', encoding='utf-8') as file:
            content = file.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Update stats in the page
        stats_div = soup.find('div', {'id': 'scholar-stats'})
        if not stats_div:
            # Create stats section if it doesn't exist
            stats_div = soup.new_tag('div', id='scholar-stats')
            stats_div['class'] = 'stats-container'
            
            # Find the main content div and insert stats at the beginning
            main_content = soup.find('div', {'class': 'content'})
            if main_content:
                main_content.insert(0, stats_div)
        
        # Clear existing stats
        stats_div.clear()
        
        # Add title
        title = soup.new_tag('h2')
        title.string = 'Research Impact'
        stats_div.append(title)
        
        # Create stats grid
        grid = soup.new_tag('div', attrs={'class': 'stats-grid'})
        
        for metric, value in stats.items():
            if metric != 'last_updated':
                stat_card = soup.new_tag('div', attrs={'class': 'stat-card'})
                
                value_elem = soup.new_tag('div', attrs={'class': 'stat-value'})
                value_elem.string = value
                
                label_elem = soup.new_tag('div', attrs={'class': 'stat-label'})
                label_elem.string = metric
                
                stat_card.append(value_elem)
                stat_card.append(label_elem)
                grid.append(stat_card)
        
        stats_div.append(grid)
        
        # Add last updated info
        last_updated = soup.new_tag('p', attrs={'class': 'last-updated'})
        last_updated.string = f"Last updated: {datetime.fromisoformat(stats['last_updated']).strftime('%Y-%m-%d %H:%M UTC')}"
        stats_div.append(last_updated)
        
        # Write updated content back to file
        with open('research.html', 'w', encoding='utf-8') as file:
            file.write(str(soup))
            
        return True
    except Exception as e:
        print(f"Error updating research page: {e}")
        return False

if __name__ == "__main__":
    stats = fetch_scholar_stats()
    if stats:
        success = update_research_page(stats)
        if success:
            print("Successfully updated research page with new stats")
        else:
            print("Failed to update research page")
    else:
        print("Failed to fetch scholar stats")

# Personal Portfolio Website

## Overview
This is my personal portfolio website hosted on GitHub Pages, showcasing my academic background, research work, industry experience, and publications. The website automatically updates its research statistics daily by fetching data from Google Scholar.

## Features
- Responsive Design
- Modern UI/UX with smooth animations
- Automatic daily updates of research metrics from Google Scholar
- Comprehensive sections for:
  - Education
  - Industry Experience
  - Research Work
  - Publications

## Technologies Used
- HTML5
- CSS3
- JavaScript
- Python (for Google Scholar stats automation)
- GitHub Actions (for automated updates)
- Google Fonts (Inter)
- Font Awesome Icons

## Automated Features
### Google Scholar Stats
- Daily automatic updates of citation metrics
- Displays:
  - Total citations
  - h-index
  - i10-index
  - Publication count
- Updates are performed via GitHub Actions

## Development Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/jyperion/jyperion.github.io.git
   cd jyperion.github.io
   ```

2. Install Python dependencies (for local development):
   ```bash
   pip install -r requirements.txt
   ```

3. Open `index.html` in a web browser to view the site locally

## Repository Structure
- `index.html` - Main landing page
- `research.html` - Research work and publications
- `industry.html` - Industry experience
- `education.html` - Educational background
- `styles.css` - Website styling
- `script.js` - Interactive features
- `update_scholar_stats.py` - Google Scholar stats automation script

## Automated Workflows
- `.github/workflows/update-scholar-stats.yml` - Daily workflow to update research metrics

## Contact
Jyothish Soman
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn Profile]
- GitHub: [Your GitHub Profile]

## License
This project is open source and available under the [MIT License].

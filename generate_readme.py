#!/usr/bin/env python3
"""
Automatically generates a dynamic README.md based on GitHub profile data.
This script fetches your repositories and generates a formatted README with cool styling.
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Any
import os

# Configuration
GITHUB_USERNAME = "hollyntt"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_user_repos() -> List[Dict[str, Any]]:
    """Fetch all repositories for the user."""
    repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
        params = {
            "page": page,
            "per_page": per_page,
            "sort": "updated",
            "direction": "desc"
        }
        headers = {}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            break
        
        data = response.json()
        if not data:
            break
        
        repos.extend(data)
        page += 1
    
    return repos

def categorize_repos(repos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize repositories by status and type."""
    categories = {
        "featured": [],
        "active": [],
        "archived": [],
        "forks": []
    }
    
    for repo in repos:
        # Skip if no activity
        if repo["size"] == 0 and repo["open_issues_count"] == 0:
            continue
        
        # Categorize
        if repo["fork"]:
            categories["forks"].append(repo)
        elif repo["archived"]:
            categories["archived"].append(repo)
        elif repo["stargazers_count"] > 0 or repo["forks_count"] > 0:
            categories["featured"].append(repo)
        else:
            categories["active"].append(repo)
    
    return categories

def get_language_stats(repos: List[Dict[str, Any]]) -> Dict[str, int]:
    """Get statistics on languages used."""
    languages = {}
    for repo in repos:
        if repo["language"] and not repo["archived"] and not repo["fork"]:
            languages[repo["language"]] = languages.get(repo["language"], 0) + 1
    return languages

def format_repo_item(repo: Dict[str, Any]) -> str:
    """Format a single repository item."""
    name = repo["name"]
    url = repo["html_url"]
    description = repo["description"] or "No description"
    language = repo["language"] or "Unknown"
    stars = repo["stargazers_count"]
    forks = repo["forks_count"]
    
    item = f"| **[{name}]({url})** | {description} | {language}"
    
    if stars > 0 or forks > 0:
        item += f" | ⭐ {stars} | 🍴 {forks}"
    else:
        item += f" | - | -"
    
    item += " |\n"
    return item

def generate_readme(repos: List[Dict[str, Any]]) -> str:
    """Generate the README content with cool styling."""
    categories = categorize_repos(repos)
    languages = get_language_stats(repos)
    
    # Sort by stars
    featured = sorted(categories["featured"], key=lambda x: x["stargazers_count"], reverse=True)
    active = sorted(categories["active"], key=lambda x: x["updated_at"], reverse=True)[:8]
    
    total_repos = len([r for r in repos if not r['fork']])
    total_stars = sum(r['stargazers_count'] for r in repos if not r['fork'])
    total_forks = sum(r['forks_count'] for r in repos if not r['fork'])
    
    readme = f"""<h1 align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=35&duration=3000&pause=1000&color=FFD700&center=true&vCenter=true&width=600&lines={GITHUB_USERNAME};Developer+%7C+Creator;VRChat+Enthusiast;Building+Cool+Stuff" alt="Typing SVG" />
</h1>

<div align="center">

![Profile views](https://komarev.com/ghpvc/?username={GITHUB_USERNAME}&color=FFD700&style=flat-square&label=Profile+Views)
![GitHub followers](https://img.shields.io/github/followers/{GITHUB_USERNAME}?style=flat-square&color=FFD700&label=Followers)
![Total Stars](https://img.shields.io/badge/Total%20Stars-{total_stars}-FFD700?style=flat-square)

</div>

---

<div align="center">

### 💻 About Me

Passionate developer creating tools and utilities for the VRChat ecosystem and gaming community. I love building cross-platform solutions and exploring new technologies.

</div>

---

## 📊 GitHub Stats

<div align="center">

[![GitHub stats](https://github-readme-stats.vercel.app/api?username={GITHUB_USERNAME}&show_icons=true&theme=nightowl&hide_border=true&count_private=true&link=https://github.com/{GITHUB_USERNAME})](https://github.com/{GITHUB_USERNAME})

[![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={GITHUB_USERNAME}&theme=nightowl&hide_border=true&layout=compact&link=https://github.com/{GITHUB_USERNAME}?tab=repositories)](https://github.com/{GITHUB_USERNAME}?tab=repositories)

</div>

---

## 🌟 Featured Projects (Top Starred)

<div align="center">

| Project | Description | Language | Stars | Forks |
|---------|-------------|----------|-------|-------|
"""
    
    if featured:
        for repo in featured[:5]:
            readme += format_repo_item(repo)
    
    readme += f"""
</div>

---

## 🚀 Recent Projects

<div align="center">

| Project | Description | Language | Stars | Forks |
|---------|-------------|----------|-------|-------|
"""
    
    if active:
        for repo in active:
            readme += format_repo_item(repo)
    
    readme += f"""
</div>

---

## 🛠️ Tech Stack

<div align="center">

### Languages
"""
    
    # Add language badges
    lang_colors = {
        "C#": "239120",
        "Python": "3776AB",
        "HTML": "E34F26",
        "Lua": "2C2D72",
        "Batch": "4D4D4D",
        "JavaScript": "F7DF1E",
        "TypeScript": "3178C6"
    }
    
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
        color = lang_colors.get(lang, "CCCCCC")
        readme += f'![{lang}](https://img.shields.io/badge/{lang.replace("#", "%23")}-{color}?style=for-the-badge&logo={lang.lower().replace("#", "csharp")}&logoColor=white)\n'
    
    readme += """
### Platforms
![Windows](https://img.shields.io/badge/Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

</div>

---

## 📈 Repository Statistics

<div align="center">

| Metric | Count |
|--------|-------|
| Total Repositories | """ + str(total_repos) + """ |
| Total Stars | """ + str(total_stars) + """ |
| Total Forks | """ + str(total_forks) + """ |
"""
    
    if languages:
        readme += f"| Languages Used | {len(languages)} |\n"
    
    readme += """
</div>

---

## 🎯 Focus Areas

- 🎵 **VRChat Ecosystem** - Building tools for the VRChat community
- 🎮 **Gaming Tools** - Creating utilities for gamers
- 🔧 **Automation** - Solving problems with code
- 💻 **Cross-Platform** - Windows & Linux development
- 🌐 **Open Source** - Sharing knowledge and tools

---

## 📧 Connect With Me

<div align="center">

**Email:** hollynn@kittymail.com

</div>

---

<div align="center">

### 💡 Fun Facts

- 🎮 VRChat enthusiast and active community member
- 💻 Automation and tool development lover
- 🌙 Night owl developer
- 🎵 Passionate about music integration

---

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=3000&pause=500&color=FFD700&center=true&vCenter=true&width=800&lines=Thanks+for+visiting+my+profile!;Feel+free+to+check+out+my+projects;Let's+build+something+awesome+together" alt="Thanks" />

*This README is automatically generated and updates daily!*

</div>
"""
    
    return readme

def main():
    """Main function."""
    print("Fetching your repositories...")
    repos = get_user_repos()
    
    if not repos:
        print("Error: No repositories found or GitHub API issue.")
        return
    
    print(f"Found {len(repos)} repositories.")
    print("Generating awesome README...")
    
    readme_content = generate_readme(repos)
    
    # Write to file
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Cool README.md generated successfully!")
    print(f"Total repositories processed: {len(repos)}")

if __name__ == "__main__":
    main()

import requests
from collections import Counter
from datetime import datetime
from rich.console import Console 
from rich.table import Table
from rich.panel import Panel

console = Console()

console.print(Panel.fit("[bold cyan]GitHub Profile Analyzer Pro[/bold cyan]", title="[bold green]Welcome![/bold green]", border_style="green"))

username =  input("Enter GitHub username: ").strip()
user_url = f"https://api.github.com/users/{username}"
repos_url = f"https://api.github.com/users/{username}/repos"
user_response = requests.get(user_url)

if user_response.status_code != 200:
    console.print("[bold red]User not found![/bold red]")
    exit()

user_data = requests.get(repos_url)
user = user_response.json()
repos = user_data.json()

# --------------------
# Profile Data
# --------------------
name = user.get("name")
bio = user.get("bio")
followers = user.get("followers")
following = user.get("following")
public_repos = user.get("public_repos")
company = user.get("company")
blog = user.get("blog")
location = user.get("location")
avatar_url = user.get("avatar_url")
profile_url = user.get("html_url")

# --------------------
# Account Age
# --------------------
created_at = user.get("created_at")
created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
years_old = (datetime.now() - created_date).days // 365

# --------------------
# Repository Statistics
# --------------------
top_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
top_repos = sorted(repos, key=lambda repo: repo["stargazers_count"], reverse=True)[:5]

# --------------------
# Language Statistics
# --------------------
languages = []

for repo in repos:
    if repo.get("language"):
        languages.append(repo["language"])

language_counter = Counter(languages)

# --------------------
# Developer Score
# --------------------
score = (
    min(public_repos, 50)
    + min(followers, 30)
    + min(top_stars, 20)
)

score = min(score, 100)

if score >= 80:
    level = "Advanced"
elif score >= 50:
    level = "Intermediate"
else:
    level = "Beginner"

# --------------------
# Profile Table
# --------------------

profile_table = Table(
    title="GitHub Profile"
)

profile_table.add_column("Field", style="cyan")
profile_table.add_column("Value", style="green")

profile_table.add_row("Name", str(name))
profile_table.add_row("Username", username)
profile_table.add_row("Bio", str(bio))
profile_table.add_row("Followers", str(followers))
profile_table.add_row("Following", str(following))
profile_table.add_row("Repositories", str(public_repos))
profile_table.add_row("Company", str(company))
profile_table.add_row("Location", str(location))
profile_table.add_row("Website", str(blog))
profile_table.add_row("Account Age", f"{years_old} years")
profile_table.add_row("Total Stars", str(top_stars))
profile_table.add_row("Developer Score", f"{score}/100")
profile_table.add_row("Level", level)

console.print(profile_table)

# --------------------
# Top Repositories
# --------------------

repo_table = Table(
    title="Top Repositories"
)

repo_table.add_column("Repository")
repo_table.add_column("Stars")

for repo in top_repos:
    repo_table.add_row(
        repo["name"],
        str(repo["stargazers_count"])
    )

console.print(repo_table)

# --------------------
# Languages
# --------------------

language_table = Table(
    title="Most Used Languages"
)

language_table.add_column("Language")
language_table.add_column("Repositories")

for language, count in language_counter.most_common():
    language_table.add_row(
        language,
        str(count)
    )

console.print(language_table)

# --------------------
# Links
# --------------------

console.print(
    f"\n[bold yellow]Profile URL:[/bold yellow] {profile_url}"
)

console.print(
    f"[bold yellow]Avatar URL:[/bold yellow] {avatar_url}"
)


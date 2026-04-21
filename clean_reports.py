import os
import subprocess

files_to_remove = [
    'report.md',
    'تقرير_التغييرات.html',
    'المرجع_التقني_الشامل.html',
    'Comprehensive_Technical_Architecture.html',
    'report.html',
    'report.csv',
    'report.json',
    'scan_results_report.html',
    'changes_report.html'
]

# Navigate to the tool directory
os.chdir('/Users/mohadreamer/0x7v11co')

# Update .gitignore
gitignore_content = """
# Ignore cache
__pycache__/
*.pyc
.DS_Store

# Ignore generated reports
report.md
*.html
*.csv
*.json
""".strip()

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write(gitignore_content)

# Remove files from git tracking (so they are deleted from Github)
for file in files_to_remove:
    # Remove from Git
    subprocess.run(['git', 'rm', '--cached', file], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    # Remove from local machine to keep your workspace clean
    try:
        if os.path.exists(file):
            os.remove(file)
    except:
        pass

# Add the tracked changes to Git and commit
subprocess.run(['git', 'add', '.gitignore'])
subprocess.run(['git', 'commit', '-m', 'Remove personal scan reports to keep repository clean'])

print("Cleanup completed successfully.")

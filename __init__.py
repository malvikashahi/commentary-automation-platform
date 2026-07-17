# Run these from project root to create all __init__.py files
cd "C:\Users\shahmal\OneDrive - acuitykp\Documents\TEMPLE COMMENTARY UI\commentary_platform"

# Create __init__.py in every package folder
New-Item -ItemType File -Path "backend\__init__.py" -Force
New-Item -ItemType File -Path "backend\routers\__init__.py" -Force
New-Item -ItemType File -Path "backend\services\__init__.py" -Force
New-Item -ItemType File -Path "backend\models\__init__.py" -Force
New-Item -ItemType File -Path "backend\core\__init__.py" -Force
New-Item -ItemType File -Path "frontend\__init__.py" -Force
New-Item -ItemType File -Path "frontend\pages\__init__.py" -Force
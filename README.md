README.md

# Defect Prediction CI/CD (RF + Flask)

Train:

py -m venv .venv
..venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/train.py --data data/dataset.csv

Serve:

$env:FLASK_APP="src/app.py"
flask run -p 5000

Predict (PowerShell):

$body = @{ instances = @(@{ la=1; ld=2; nd=3; ns=1; nf=2; ent=0.5; ndev=1; nuc=1; age=10; aexp=2; asexp=1; arexp=1 }) } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/predict
-ContentType "application/json" -Body $body

# run locally
python -m app.main

# run production
gunicorn app.main:app

# run stress test
locust -f locustfile.py --host https://bestellen.scoutingwateringen.nl
sanity check: 10 users, 2 rampup
realistic: 50 users, 5 rampup

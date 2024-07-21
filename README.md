# For running the script every day add this on cronjob config
aws_access_key_id=***
aws_secret_access_key=***
region_name=***

0 * * * * python3 /home/rajiv/Documents/python/heathcheck-ses-script/main.py

# To debug the cron job
0 * * * * python3 /home/rajiv/Documents/python/heathcheck-ses-script/main.py >> /home/rajiv/your_script.log 2>&1

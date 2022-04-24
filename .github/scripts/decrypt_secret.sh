 #!/bin/sh
    
# Decrypt the file
mkdir $GITHUB_WORKSPACE/secrets
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output $GITHUB_WORKSPACE/strava_calendar_summary_utils/config.py strava_calendar_summary_utils/config.py.gpg
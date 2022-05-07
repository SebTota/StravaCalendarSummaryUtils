import setuptools

setuptools.setup(
    name='strava_calendar_summary_utils',
    version='0.0.19',
    author='Sebastian Tota',
    author_email='seb001@protonmail.com',
    description='The Utils package for the Strava Calendar Summary Application',
    url='',
    packages=setuptools.find_packages(),
    install_requires=['google-cloud-logging', 'google-cloud-pubsub', 'google-api-python-client', 'google-auth', 'stravalib', 'strava_calendar_summary_data_access_layer'],
    dependency_links=['https://github.com/SebTota/StravaCalendarSummaryUtils/tarball/master#egg=strava_calendar_summary_data_access_layer']
)
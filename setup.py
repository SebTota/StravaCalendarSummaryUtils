import setuptools

setuptools.setup(
    name='strava_calendar_summary_utils',
    version='0.0.12',
    author='Sebastian Tota',
    author_email='seb001@protonmail.com',
    description='The Utils package for the Strava Calendar Summary Application',
    url='',
    packages=setuptools.find_packages(),
    install_requires=['google-cloud-logging', 'google-cloud-pubsub', 'strava_calendar_summary_data_access_layer'],
    dependency_links=['git+https://github.com/SebTota/StravaCalendarSummaryDataAccessLayer.git#egg=strava_calendar_summary_data_access_layer']
)
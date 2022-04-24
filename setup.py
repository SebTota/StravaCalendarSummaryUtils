import setuptools

setuptools.setup(
    name='strava_calendar_summary_utils',
    version='0.0.1',
    author='Sebastian Tota',
    author_email='seb001@protonmail.com',
    description='The Utils package for the Strava Calendar Summary Application',
    url='',
    packages=['strava_calendar_summary_utils'],
    install_requires=['google-cloud-logging', 'git+https://github.com/SebTota/StravaCalendarSummaryDataAccessLayer.git']
)
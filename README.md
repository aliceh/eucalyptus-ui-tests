eucalyptus-ui-tests
===================

Selenium test suite for the Eucalyptus Console web UI


****************
*Prerequisites:*
****************

Python (tested with 2.7 but 2.6 should also work)
Selenium for Python (easy_install selenium)
A Sauce Labs account (http://www.saucelabs.com)
A user account on the cloud with access key that is NOT in the eucalyptus account.
Sauce Connect (this is only needed if testing an install on a private network)
Instructions for installing/running Sauce Connect:
https://saucelabs.com/docs/sauce-connect

********
*Setup:*
********

Before running the test suite, one must modify certain settings in settings.py.
Most of these settings need only be changed once if your cloud information has
not changed from your previous run.

One exception to this rule is:

default_capabilities['build']

This must be changed before each test run as it is used in by the Sauce Labs
interface to group tests from a particular test run. Any string can be used
here but it is recommended to use the date and time that the test run is being
initiated for archival purposes.

**********
*Running:*
**********

Launching the entire test suite is as easy as:

python runAll.py

One may run individual tests as well:

python <test_name>.py

**********
*Results:*
**********

Results from the test are sent to stdout/stderr but detailed results including
video and screenshots can be accessed via http://www.saucelabs.com.

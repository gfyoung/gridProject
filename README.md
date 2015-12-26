[![Build Status](https://travis-ci.org/gfyoung/gridProject.svg?branch=master)](https://travis-ci.org/gfyoung/gridProject)

# gridProject
Website that collects and displays data from Off the Grid SF

# Before you run the project
* As this code is provided solely for reference and is not being run anywhere to the best of the author's knowledge, any "private" information such as authentication tokens and secret keys (e.g. `settings.py`) have been made public. Should this code be used for a personal website or usage beyond private development, you will have to <b>reinitialize</b> the project so that any such information will be kept hidden!
* Make sure that you have authenticated access to the Facebook API. Otherwise, the website will display no data. Once you do have authenticated access, make sure to change the OAuth token in `vendorUtil.py` to the token you have been assigned!
* <b>NB:</b> The current OAuth token provided in `vendorUtil.py` is void and will not give you access to any data.

# Running the website locally (for dev. work)
* Fork and clone this repository
* Move to your gridProject/gridSite directory
* From there, run the following command: `python manage.py runserver`
  * If there are issues running this command, try changing the port number by adding `<Port Number>` to the end of the command
  * You can also change the IP address by adding `<IP Address>:<Port Number>` to the end of the command
  * Please refer to https://docs.djangoproject.com/en/1.9/ref/django-admin/ for more information otherwise
    * Note that this documentation is for Django 1.9, so make sure that you change the version number in the URL depending on which version of Django you are using

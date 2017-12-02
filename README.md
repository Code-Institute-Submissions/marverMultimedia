# Marver Webcast ON-DEMAND Platform

This Project has been created to give organization the possibility of easily and efficiently deliver video(and multimedia) content to
users, this platform gives the organization the opportunity to host and share On-Demand videos whilst also providing other informational
capabilities like document download, agenda points, chapters, speakers, Support, etc.

The Project is divided into two Django Applications:

#### Events Manager

- Application in charge of the creation, editing and publishing of Events, Login, Registration and Service Subscription

#### Events Display

- Application in charge of Display, Organize ad Share On-Demand video webcasts

## Features

#### Existing Features

- Ability to implement and manage service subscription payment model via Stripe
- Ability for users to register and obtain their own login details based on their subscription
- Ability to create and instantly publish Webcast Events that are unique per single user
- Ability to edit the Webcast Events information and upload large video file size(directly to Amazon S3)
- Ability to create Speaker Information that includes Bio, Picture, etc.
- Ability to create Agenda points
- Ability to upload new downloadable assets assigned to the specific Webcast event(re-usable for other webcasts also)
- Ability to select part of video as Thumbnail for Webcast Event Display
- Ability to extract various parts of the video as image chapter thumbnail for provisioning into the Webcast Player and to enable more targeted video navigation
- Ability to submit feedback per single Webcast which is stored in a database for later reporting usage
- Ability to submit support requests per single Webcast which are stored in a database for later reporting usage
- Ability to submit Star based rating per single Webcast which is stored in a database for later reporting usage

## Getting Started

##### This project has been built on Python version 2.7 however certain adjustment have been applied to make sure is compatible with Python 3.6 due to Heroku Deployment

1. Firstly you will need to clone this repository by running the ```git clone https://github.com/Diomede81/marverMultimedia.git``` command
2. After the cloning process has ended please make sure that(if you are using a Windows Environment) you have **python** and **pip(which comes pre-installed with Python)** installed - Python comes pre-installed with Linux and MacOS

    1. You can get **Python** by the download page [here](https://www.python.org/downloads/)
    2. Once you've installed Python you'll need to run the following command to install the Virtual Environment package:

       `pip install virtualenv # this may require sudo on Mac/Linux`
    3. After the successfull installation of virtualenv please activate the environment by following this
        [guide](https://virtualenv.pypa.io/en/stable/userguide/#usage)
    4. To complete the packages installation, type the following command in order to install all the necessary
        dependencies for this application, these are stored in the provided requirements.txt file
        please ensure that you are located in the root project folder when running this command
        `pip install -r requirements.txt`

2. Within the Settings folder, open the file named config.py and add the information related to your project(Database details, AWS Security details, Etc.)
before you go further as the project will not work without at least a database configured(you can utilize MySQL lite which can be downloaded [here](https://www.sqlite.org/)
3. Once all of the dependency packages have been installed and the config file have been populated with all the necessary information, please test the Django deployment by typing the following command(ensure you are in the project root folder before running it)
    1. `python manage.py runserver --settings=settings.dev`
    2. This will start the server in development mode and serve the static files from your local static folder
4. If you would like to test the staging mode(the final version before production) please ensure that you have configured your AWS S3 bucket and have run the following command
    1.  `python manage.py collectstatic --settings=settings.staging`
    2.  This will upload automatically to the S3 Bucket all the files necessary for the correct functionality of the site
6. The project will now run on [localhost](http://127.0.0.1:8000) unless otherwise stated on the terminal
7. Make changes to the code and if you think it belongs in here then just submit a pull request


## Running the tests

The Application has been extensively tested with multiple Operative Systems and multiple browser types

**Javascript Testing**:

 Javascript testing has been performed manually via testing of different scenarios in multiple browsers, the utilization of
 a testing suite has not been used as most of the Javascript functions are utilized to modify DOM elements and could easily be tested manually

**Python Testing**:

  Django integrated testing suite has been utilized to test that each view would successfully connect to a database and provide back the correct information and HTTP messages

  Each Application's views has veeb tested using the above method and successfully provide the required information and HTTP messages


### Tests

The below example of view test will receive an image and ensure that the necessary information are saved into the database for later retrieval

An Example:

```

    def test_thumbnail_upload(self):
        img = BytesIO(b'myImage')
        img.name = 'webcast.jpg'

        thumbnail_upload_test = self.client.post('/thumbnail_upload/',data={
            'webcast_id' : 1,
            'webcast_image' : img
        })

        self.assertEqual(thumbnail_upload_test.status_code,200)
```


## Deployment



The application has been deployed using the following:

 - Heroku to manage the Django Web Server & WSGI Support
 - AWS RDS to manage the MySQL database
 - AWS S3 to manage the serving of static and media files
 - GMAIL to manage the automated mail responses


For deployment instruction on Heroku please visit [Here](https://devcenter.heroku.com/categories/python)
For Deployment instruction on AWS please visit [Here](https://aws.amazon.com/documentation/gettingstarted/)


## Built With


* HTML5/CSS3 - The languages used for the pages design
* [Bootstrap 3.3](https://getbootstrap.com/docs/3.3/) - The responsive design development Framework Used
* JAVASCRIPT - The language used to build the interactivity of the web page elements
* [JQuery](https://jquery.com/) - The Library used to enhance the interactivity of the web page elements for cross-browser successful implementation
* [PYTHON](https://www.python.org/) - The Language utilized to manage the Server Side connections with Database and relevant services
* [Django](https://www.djangoproject.com/) - The Python Framework utilized to create a structured, stable and efficient application based on the Python language
* [JetBrains PyCharm](https://www.jetbrains.com/pycharm/) - The IDE used to develop and test the application

### More Information about build libraries

The following library has been also used to enhance the user experience:

#### [BootStrap-Timepicker](https://jdewit.github.io/bootstrap-timepicker):
- This library has been utilized to implement date-picker for web browser that do not have a native support for time picker

#### Jquery-UI:

- This specific library has been used to implement a date picker for browsers that do not natively support one

#### [S3-Direct](https://github.com/bradleyg/django-s3direct):

- This library has been used to implement the upload of video files directly to AWS S3 in order to bypass the Web-Server and limit load on operations

#### [Boto3](http://boto3.readthedocs.io/en/latest/):

- Boto 3 has been used to implement the link between the Django application and AWS S3 in order to enable the serving of static
files and upload of media files to the S3 Bucket.


## Versioning

I have used [Git](https://git-scm.com/) & [GitHub](https://github.com/)( for versioning.

## Author

* **Luca Licata** - [GitHub](https://github.com/Diomede81) - [Linkedin](www.linkedin.com/in/luca-licata-26637641
)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Many Thanks to my Mentor **Theo Despoudis** [GitHub](https://github.com/theodesp) for all the support with ensuring that this application's code would be up to high standards
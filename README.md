# Marver Webcast ON-DEMAND Platform

This Project has been created to give organization that communicate information and messages via video to
store the videos and provide the users with a simple to use platform for video replay, document download, Speaker info

The Project is divided into two Django Applications:

#### Events Manager

- Application in charge of the creation, editing and publishing of Events, Login, Registration and Subscription

#### Events Display

- Application in charge of Storage, organization, replay of On-Demand video events

## Features

#### Existing Features

- Ability to implement subscription payment model via Stripe
- Ability to create Webcast Events that are unique per single user, but that are readily published ot the platform
- Ability to edit the Webcast Events information and upload large video file size(directly to Amazon S3)
- Ability to create Speaker Information that includes Bio, Picture, etc.
- Ability to create Agenda points
- Ability to upload new downloadable assets assigned to the specific Webcast event(re-usable for other webcasts also)
- Ability to select part of video as Thumbnail for more attracting display
- Ability to select various parts of the video as chapter thumbnail for provision into the Webcast Player

## Getting Started

##### This project has been built on Python version 2.7 however certain adjustment have been applied to make sure is compatible with Python 3.6 due to Heroku Deployment

1. Firstly you will need to clone this repository by running the ```git clone https://github.com/Diomede81/marverMultimedia.git``` command
2. After you've done that please make sure that(if you are using a Windows Environment) you have **python** and **pip(which comes pre-installed with Python)** installed - Python comes pre-installed with Linux and MacOS

    1. You can get **Python** by the donwload page [here](https://www.python.org/downloads/)
    2. Once you've installed Python you'll need to run the following command to install the Virtual Environment package:

       `pip install virtualenv # this may require sudo on Mac/Linux`

3. Once **npm** and **bower** are installed, you'll need to install all of the dependencies in *package.json* and *bower.json*
  ```
  npm install

  bower install
  ```
4. After those dependencies have been installed you'll need to make sure that you have **http-server** installed. You can install this by running the following: ```npm install -g http-server # this also may require sudo on Mac/Linux```
5. Once **http-server** is installed run ```http-server -c-1```
6. The project will now run on [localhost](http://127.0.0.1:8080)
7. Make changes to the code and if you think it belongs in here then just submit a pull request


## Running the tests

Jasmine/Karma testing suite have been used to test the user action of adding items to the basket and eventual basket calculation about
prices and quantities

Jasmine/Karma(if you follow the installation procedure correctly) will be installed with NPM/Bower packages and ready to use

if you have any trouble installing please visit the this [link](https://karma-runner.github.io/1.0/intro/installation.html)

### Tests

The Tests have been designed to verify correct functionality of the services that will take care of the shopping basket
and other APIs(I.e. the API that will retrieve list of addresses from postcode provided)

An Example:

```

// Factory responsible for adding wines to the basket

    describe('.addItemTobasket()', function () {


        var item =
            {
                wine: {

                    id: 4,
                    totalBasket:0
                }

            };

        var basket = null;

        var element = "";

        var quantity = 2;

        var addItemToBasketDomSpy

        beforeEach(function(){

            addItemToBasketDomSpy = spyOn(DomManipulation,'addItemToBasketDom').and.returnValue(2);
            addItemToBasketDomSpy2 = spyOn(DomManipulation,'makeBasketIconAppearDisappear').and.returnValue(2);

        });


        it('should Exist', inject(function (BasketService) {

            expect(BasketService.addItemTobasket(item,element,quantity,basket)).toEqual([{id:4, totalBasket:2}]);
            expect(addItemToBasketDomSpy).toHaveBeenCalledWith(element);
            expect(addItemToBasketDomSpy2).toHaveBeenCalledWith('appear');
            expect(addItemToBasketDomSpy).toHaveBeenCalledTimes(1);

        }))

    });

```


## Deployment

The application is ready to be deployed on a live web server, just copy the files in the designated Web-Server Folder and the site should be loading successfully

## Built With


* HTML5/CSS3 - The languages used for the pages design
* [Bootstrap 3.3](https://getbootstrap.com/docs/3.3/) - The responsive design development Framework Used
* JAVASCRIPT - The language used to build the interactivity of the web page elements
* [JQuery](https://jquery.com/) - The Library used to enhance the interactivity of the web page elements for cross-browser successful implementation
* [AngularJS](https://angularjs.org/) - The Javascript framework used for implementing local-storage, page-routing
* [NPM](https://www.npmjs.com/) - Dependency Management
* [Bower](https://bower.io/) - Dependency Management
* [Jasmine](https://jasmine.github.io/) - The testing framework used
* [Karma](https://karma-runner.github.io/1.0/index.html) - The test runner used
* [JetBrains Webstorm](https://www.jetbrains.com/webstorm/) - The IDE used to develop and test the application

## Versioning

I have used [Git](https://git-scm.com/) & [GitHub](https://github.com/)( for versioning.

## Author

* **Luca Licata** - [GitHub](https://github.com/Diomede81) - [Linkedin](www.linkedin.com/in/luca-licata-26637641
)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Many Thanks to my Mentor **Theo Despoudis** [GitHub](https://github.com/theodesp) for all the support with ensuring that this application's code would be up to high standards
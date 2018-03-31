# Farmstar
!README NOT COMPLETE!
Farm management web framework including GPS tracking of machines and task assignment. Designed to run on raspberry pi's however can run on any hardware.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python3 for your OS.

GPS tacking via a serial interface.
	Primarily designed for the ublox NEO-M8 for the rasberry pi, however should work with any serial GPS device.
	Can be emulated from a phone through bluetooth, tested with 'Bluetooth GPS Output' app.

Django web framework
```
pip3 install Django
```
A whole bunch of other python modules
```
pip install awholebunchofshit
```

### Installing

Download this git and extract
Open terminal / cmd
Change to the project directory
Run django server;
If only testing localy:
```
python3 manage.py runserver 
```

If accessing on LAN:
```
python3 manage.py runserver your.local.ip.address:port
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc


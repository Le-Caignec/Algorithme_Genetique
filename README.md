<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#results">Results</a></li>
    <li><a href="#improvement">Improvement</a></li>

  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


The objective of this project is to implement the genetic algorithm to create a program from a list of proposed activities with the following constraints: 
the activities have different opening hours
the program can be spread over several days
travel time should be reduced as much as possible
maximize the number of activities on the list included in the program
the price paid must be minimized
it is necessary to increase the margin realized by the site


### Built With

the technologies used
* [Pyhthon 3.6](https://www.python.org/downloads/release/python-360/)

* [MariaDb](https://mariadb.com/kb/en/installing-mariadb-msi-packages-on-windows/)



<!-- GETTING STARTED -->
## Getting Started
The data is available from a mariadb database filled using the sql scripts provided by booktrip. You must first have installed [mariadb](https://mariadb.org/download/) on the PC, and created a database in which you executed the sql scripts with the "source" command. 



The functions in connect.py allow you to directly request activities based on dictionaries.

### Prerequisites

To connect to the database using the functions in the database folder, you need to :
* have installed the python package mariadb ( for example : "pip install mariadb")
* have filled the config.ini file in the database folder with :
* the name of the database in which the data were deposited
* the name and password to access the database 
* the port of the PC on which the base is running (normally 3306).


### Installation
0. First npm
  ```sh
  npm update mpn 
  ```
1. After installing [Python](https://www.python.org/downloads/release/python-360/) and [MariaDB](https://mariadb.com/kb/en/installing-mariadb-msi-packages-on-windows/)  
2. Clone the repo
   ```sh
   git clone https://github.com/HRemu/PRI/
   ```
3. Install packages
   ```sh
   npm install: random ,math, datetime, matplotlib.pyplot,	mariadb, folium, webbrowser, configparser, database,json

   ```
4. Configure `config`fille in database
   ```sh
   host: localhost, database name, user, password,port 
   ```



<!-- USAGE EXAMPLES -->
## Results

We were able to implement a first complete version of the genetic algorithm. Although it does not take into account all the criteria and constraints of our problem, it already allows us to display a first solution.
	First of all, the algorithm allows to create schedules spread over a given number of days, taking into account annual periods, opening hours and a calculation of travel times.
	In addition, intersections and mutations respect this system and allow to obtain successive generations. For the moment, these generations do not significantly improve the results. However, on average the individuals improve, which indicates that the algorithm does have a beneficial effect on the individuals created.


<!-- ROADMAP -->
## Improvement 

The solution we have implemented is not complete. First of all, for the choice of activities the program does not take into account the days of the week when the activity is available. Activities without a specified duration are not yet removed, and are currently treated as having a default duration. Changing this can be done quickly when checking the duration of the activity, but will not be necessary if the filtering is done correctly before the selection of activities by the customer.

Similarly, when developing a program, we do not allow for a meridian break between activities. This pause is sometimes present because of the activity schedules, but it is not automatic. Moreover, the calculation of the current score does not take into account the daytime division and will calculate the distance between two activities located one night apart. This calculation of the score for each schedule must be repeated, especially once the program is complete, in order to determine the optimal parameters.
  
There are also some functions that still have problems. These are trade_mutation in mutation.py and multi_intersection in crossover.py. Both of these functions return errors and are currently not used.


<!-- CONTRIBUTING -->
## Contributing

* [ACHARD Jocelyn](jocelyn.achard@telecom-st-etienne.fr)
* [DUBUISSON Isidore](dubuisson.isidore@gmail.com)
* [HUGUENOT Rémi](remi.huguenot@telecom-st-etienne.fr)
* [KAMISSOKHO Yaya](yaya.kamissokho@gmail.com)
* [TEFAATAU Given](given.tefaatau@telecom-st-etienne.fr)




<!-- LICENSE -->
## License

BOOKTRIP.FR SAS





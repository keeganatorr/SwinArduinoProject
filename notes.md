Light Sensor (Analog)

https://learn.sparkfun.com/tutorials/temt6000-ambient-light-sensor-hookup-guide/all

Ultrasonic Sensor (Digital)

https://www.jaycar.com.au/medias/sys_master/images/images/9886470897694/XC4442-manualMain.pdf


## Installing mysql/mariadb on linux

pacman -S mariadb

mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
systemctl enable mariadb.service
systemctl start mariadb.service

## Installing mysql/mariadb on rpi

pacman -S mariadb-server


### In MySQL

// on desktop
grant all privileges on temperature_db.* to ''@'localhost';


// on pi
grant all privileges on temperature_db.* to 'pi'@'localhost';


```
mysql
ERROR 1698 (28000): Access denied for user ' pi' @ ' localhost '
```

We will enter as admin and execute the following:

```
sudo mysql
CREATE USER ' pi' @ ' localhost ' ;
CREATE DATABASE temperature_db;
GRANT ALL PRI VILEGES ON temperature_db.* TO ' pi' @ ' localhost ' ;
exit
```

We created the temparature_db database, the username pi without password, and we granted per-
missions to pi to edit the database. We will open again mysql as the pi user to create a table in the
temperature_db database:

```
mysql
USE temperature_db;
CREATE TABLE tempLog ( tempId int(11) AUTO_INCREMENT NOT NULL,
temperature VARCHAR(20) NOT NULL, PRIMARY KEY (TempId) );
DESCRIBE tempLog ;
exit
```

The final step is to modify your previous code to store data in the database. Your final code should be
similar to the code shown in Figure 4. However, you need to modify it in order to store all the data
being received via serial bus. WARNING: The code shown in Figure 4 imports MySQLdb, you need to
import pymysql. Please check PyMySQL user guide provided in the resources section to modify your
code accordingly.
You can check if the data is being stored in the database from mysql:
```
mysql
USE temperature_db;
SELECT * FROM tempLog;
```

## mine

create table tempLog (tempId int(11) auto_increment not null, time varchar(40) not null, temperature varchar(20) not null, temp2 varchar(20) not null, primary key (tempId));






# todo

- add interrupts
- add light
- add US
- add open LED
- add close LED
- edit light trigger
- edit US trigger
- force open door
- clear DB

display table of
    [time of trigger, light value, US value]
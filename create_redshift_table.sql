create table weather_api_table(psf varchar(70),
                              cloud int, condition varchar(20),country varchar(30),humidity int,
                              last_updated_time varchar(50),latitude float, local_time varchar(20),longitude float,
                              name varchar(20),precip_mm float,pressure_mb float,region varchar(20),temp_c float,
                              wind_dir varchar(20),wind_mph float);
copy weather_api_table from 'dynamodb://weather-dynamodb-table'
credentials 'aws_access_key_id=<access_key>;aws_secret_access_key=<secret_key>'
readratio 50;
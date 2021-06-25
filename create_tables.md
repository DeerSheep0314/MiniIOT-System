```sql
create database miniIOT;
use miniIOT;

CREATE TABLE PUser(
							userName								VARCHAR(100) PRIMARY KEY,
							eMail    								VARCHAR(100),
							passWD									VARCHAR(256),
							isAdministrator							bit(1)#1 for Ad and 0 for User
)
;
CREATE TABLE Device (
							alert									TINYINT,#1 for Alert and 1 for Normal
							id      								char(10),
							info        							VARCHAR(50) ,
							lat     								DOUBLE,
							lng     								DOUBLE,
							timestamp								BIGINT PRIMARY KEY,
                            value                                   TINYINT
)
```


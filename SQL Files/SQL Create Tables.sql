CREATE TABLE AuditoriumMembers (
MemberID int PRIMARY KEY NOT NULL,
Fname varchar(20) NOT NULL,
Lname varchar(20) NOT NULL,
DateOfBirth date NOT NULL,
MemberType int NOT NULL,
Email varchar(60) NOT NULL,
PhoneNum varchar(10),
Passw varchar(100) NOT NULL);

CREATE TABLE AuditoriumPerformances (
PerformanceID int PRIMARY KEY NOT NULL,
PerformanceName varchar(30) NOT NULL,
Genre varchar(30) NOT NULL,
PicturePath varchar(max) NOT NULL,
Descr varchar(1000) NOT NULL,
Rating varchar(5) NOT NULL,
Duration time NOT NULL);

CREATE TABLE AuditoriumShowings (
ShowingID int PRIMARY KEY NOT NULL,
ShowingDate date NOT NULL,
ShowingTime time NOT NULL,
PerformanceID int FOREIGN KEY REFERENCES AuditoriumPerformances(PerformanceID) NOT NULL);

CREATE TABLE AuditoriumBookings (
BookingID int PRIMARY KEY NOT NULL,
MemberID int FOREIGN KEY REFERENCES AuditoriumMembers(MemberID) NOT NULL,
ShowingID int FOREIGN KEY REFERENCES AuditoriumShowings(ShowingID) NOT NULL,
Seat varchar(3) NOT NULL,
Cost float NOT NULL);
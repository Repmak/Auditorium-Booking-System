import pyodbc
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def connect():
    try:
        cnxn = pyodbc.connect("DRIVER={SQL Server}; Server=localhost\SQLEXPRESS; Database=master; Trusted_Connection=True;")  # CONNECTION STRING.
        connected = True   # SETS connected TO True IF THE PREVIOUS LINE OF CODE WORKED.
        cursor = cnxn.cursor()  # cursor WILL BE USED TO RETRIEVE A RESULT FROM AN SQL STATEMENT.
    except:
        connected, cursor, cnxn = False, '', ''  # SETS connected TO False AND cursor AND cnxn TO EMPTY STRINGS.
    return connected, cursor, cnxn


def loadperformances(membertype):
    connected, cursor, cnxn = connect()  # CONNECTS TO DATABASE.
    showings = []  # showings AND performances DECLARED AS ARRAYS.
    performances = []
    if not connected:  # IF NOT CONNECTED TO DATABASE, DO NOT BOTHER TRYING TO RETRIEVE DATA.
        pass
    else:
        sqlstatement = "SELECT * FROM AuditoriumShowings ORDER BY ShowingDate"  # RETRIEVE ALL SHOWINGS.
        cursor.execute(sqlstatement)
        showings = cursor.fetchall()
        showings = [tuple(row) for row in showings]

        sqlstatement = "SELECT * FROM AuditoriumPerformances"  # RETRIEVE ALL DETAILS OF PERFORMANCES.
        cursor.execute(sqlstatement)
        performances = cursor.fetchall()
        performances = [tuple(row) for row in performances]

        if membertype == 0:  # CALCULATES REVENUE FOR STAFF AND ALL RETRIEVED SHOWINGS ARE LEFT IN THE showings ARRAY.
            sqlstatement = "SELECT ShowingId, Cost FROM AuditoriumBookings"  # RETRIEVES Cost and ShowingID. THESE WILL BE USED TO CALCULATE REVENUE FOR EACH SHOWING.
            cursor.execute(sqlstatement)
            individualcosts = cursor.fetchall()
            for i in range(0, len(showings)):  # FOR LOOP STARTED TO ITERATE THROUGH ALL SHOWINGS of showings.
                showingrevenue = 0  # showingrevenue SET TO 0 AFTER EVERY ITERATION OF THE FOR LOOP.
                for k in range(0, len(individualcosts)):  # FOR LOOP USED TO ITERATE THROUGH individualcosts.
                    if individualcosts[k][0] == showings[i][0]:  # IF ShowingID from showings MATCHES ShowingID FROM individualcosts, ADD cost TO THE showingrevenue.
                        showingrevenue = showingrevenue + int(individualcosts[k][1])
                    else:  # OTHERWISE, PASS.
                        pass
                tempshowing = list(showings[i])
                tempshowing.append(showingrevenue)  # APPENDS SHOWING REVENUE TO TEMPORARY ARRAY.
                showings[i] = tempshowing  # REPLACES ORIGINAL SUB ARRAY WITH TEMPORARY ARRAY.
        else:  # REMOVES SHOWINGS WHICH HAVE DATES IN PAST FOR STUDENTS AND PARENTS.
            validshowings = []  # validshowings DECLARED AS ARRAY.
            currentdate = datetime.datetime.now()  # FINDS CURRENT DATE AND TIME.
            for i in range(0, len(showings)):  # FOR LOOP USED TO ITERATE THROUGH ALL SHOWINGS.
                year = int(showings[i][1][:4])  # FORMATTING DATE AND TIME OF SHOWING SO THAT THEY CAN BE COMPARED.
                month = int(showings[i][1][5:7])
                day = int(showings[i][1][8:10])
                hour = int(showings[i][2][:2])
                minute = int(showings[i][2][3:5])
                dateandtime = datetime.datetime(year, month, day, hour, minute)
                if dateandtime < currentdate:  # IF SHOWING DATE AND TIME IS SMALLER THAN CURRENT DATE AND TIME, PASS.
                    pass
                else:  # OTHERWISE, APPEND THE SHOWING SUB ARRAY TO validshowings.
                    validshowings.append(showings[i])
            showings = validshowings  # SET showings TO validshowings.

        sqlstatement = "SELECT ShowingId, Seat FROM AuditoriumBookings"  # RETRIEVE ShowingID AND Seat FROM BOOKINGS.
        cursor.execute(sqlstatement)
        individualseats = cursor.fetchall()
        for i in range(0, len(showings)):  # FOR LOOP USED FOR ITERATE THROUGH ALL SHOWINGS.
            numseats = 0  # numseats SET TO 0 AFTER EVERY ITERATION.
            for k in range(0, len(individualseats)):
                if individualseats[k][0] == showings[i][0]:  # IF ShowingID from showings MATCHES ShowingID FROM individualseasts, ADD 1 TO numseats.
                    numseats = numseats + 1
                else:
                    pass
            seatsrem = 200 - numseats  # seatsrem IS EQUAL TO 200 TAKE AWAY numseats
            tempshowing = list(showings[i])
            tempshowing.append(seatsrem)  # seatsrem APPENDED TO TEMPORARY ARRAY.
            showings[i] = tempshowing  # REPLACE ORIGINAL SUB ARRAY TO TEMPORARY ARRAY.
        cnxn.close()  # CLOSES CONNECTION.
    return showings, performances  # RETURNS showings AND performances.


def loadseats(showingid):
    connected, cursor, cnxn = connect()  # CONNECTS TO DATABASE.
    seatlayout = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"  # STATE OF EACH SEAT STORED AS 0S AND 1S.
    if not connected:  # IF NOT CONNECTED TO DATABASE, DO NOT BOTHER TRYING TO RETRIEVE DATA.
        pass
    else:
        sqlstatement = "SELECT Seat FROM AuditoriumBookings WHERE ShowingID = '" + showingid + "'"  # WILL RETRIEVE ALL BOOKING RECORDS WITH ShowingID THAT WAS PASSED IN AS PARAMETER.
        cursor.execute(sqlstatement)
        individualseats = cursor.fetchall()
        cnxn.close()
        for i in range(0, len(individualseats)):  # ITERATES THROUGH ALL SUB ARRAYS OF individualseats.
            index = int(individualseats[i][0])  # FINDS INDEX OF SEAT AND SETS IT TO i.
            firstpart = seatlayout[:index - 1]  # firstpart SET TO VALUES OF seatlayout FROM INDEXES 0 TO i TAKE AWAY 1.
            secondpart = seatlayout[index: 200]  # secondpart SET TO VALES OF seatlayout FROM INDEXES i TO 200.
            seatlayout = firstpart + "1" + secondpart  # seatlayout SET TO firstpart, 1 AND secondpart JOINED TOGETHER.
    return seatlayout  # RETURNS seatlayout.


def logindetails(email, password):
    connected, cursor, cnxn = connect()  # CONNECTS TO DATABASE.
    memberid = None
    membertype = None
    if not connected:  # IF NOT CONNECTED TO DATABASE, DO NOT BOTHER TRYING TO RETRIEVE DATA.
        pass
    else:
        sqlstatement = "SELECT MemberID, Email, Passw, Membertype FROM AuditoriumMembers"  # SELECTS MemberID, Email, Passw AND MemberType.
        cursor.execute(sqlstatement)
        logindetails = cursor.fetchall()
        for i in range(0, len(logindetails)):  # ITERATES THROUGH ALL SUB ARRAYS OF logindetails.
            if email == logindetails[i][1] and password == logindetails[i][2]:  # IF ENTERED CREDENTIALS MATCH CREDENTIALS OF SUB ARRAY, PROCEED WITH NEXT LINES OF CODE.
                memberid = logindetails[i][0]  # SET memberid TO THE MemberID OF THE SUB ARRAY.
                membertype = logindetails[i][3]  # SET membertype TO THE MemberType OF THE SUB ARRAY.
            else:  # OTHERWISE, PASS.
                pass
        cnxn.close()  # CLOSES CONNECTION.
    return memberid, membertype  # RETURNED memberid AND membertype.


def confirmationinfo(performanceid, showingid, memberid):
    connected, cursor, cnxn = connect()  # CONNECTS TO DATABASE.
    if not connected:  # IF NOT CONNECTED TO DATABASE, DO NOT BOTHER TRYING TO RETRIEVE DATA.
        pass
    else:
        sqlstatement = f"SELECT PerformanceName FROM AuditoriumPerformances WHERE PerformanceID = '{performanceid}'"  # RETRIEVES PERFORMANCE NAME.
        cursor.execute(sqlstatement)
        performancename = cursor.fetchall()
        sqlstatement = f"SELECT ShowingDate, ShowingTime FROM AuditoriumShowings WHERE ShowingID = '{showingid}'"  # RETRIEVES SHOWING DATE AND TIME.
        cursor.execute(sqlstatement)
        showingtimedate = cursor.fetchall()
        sqlstatement = f"SELECT Email, FName FROM AuditoriumMembers WHERE MemberID = '{memberid}'"  # RETRIEVES EMAIL AND FIRST NAME OF USER.
        cursor.execute(sqlstatement)
        memberinfo = cursor.fetchall()
        showingdate = showingtimedate[0]
        showingtime = showingdate[1]
        cnxn.close()  # CLOSES CONNECTION.
        try:
            sendemail(memberinfo[0][0], memberinfo[0][1], performancename[0][0], showingdate[0], showingtime[:5])  # RUNS SUB PROGRAM sendemail. PARAMETERS ARE REQUIRED TO SEND EMAIL TO RECIPIENT, ADDRESS USER BY THEIR NAME AND REITERATE BOOKING INFORMATION.
        except:
            pass
        return performancename[0][0], showingdate[0], showingtime[:5], memberinfo[0][0]  # RETURNS ALL DETAILS THAT WILL BE DISPLAYED ON CONFIRMATION PAGE.


def bookbooking(memberid, showingid, seats, tickets):
    connected, cursor, cnxn = connect()  # CONNECTS TO DATABASE.
    if not connected:  # IF NOT CONNECTED TO DATABASE, DO NOT BOTHER TRYING TO RETRIEVE DATA.
        pass
    else:
        remove = -1  # REMOVE SET TO -1, WILL BE USED LATER ON.
        try:
            sqlstatement = "SELECT BookingID FROM AuditoriumBookings"  # SELECTS BookingID FROM BOOKINGS.
            cursor.execute(sqlstatement)
            highestid = cursor.fetchall()
            newid = highestid[-1][0] + 1  # SETS newid TO THE PREVIOUS LARGEST ID ADD 1.
        except:
            newid = 0  # SETS newid TO 0 IN THE CASE THAT NO RECORDS GET RETRIEVED. THIS MEANS NO RECORDS ARE PRESENT IN AuditoriumBookings.
        while remove != 0:  # ENTERS WHILE LOOP WHILE remove NOT EQUAL TO 0.
            seatnum = seats[0:seats.find(",")]  # FINDS INDEX OF FIRST COMMA IN seats. SETS seatnum TO INDEX 0 TO INDEX OF FIRST COMMA.
            ticket = tickets[0:tickets.find(",")]  # FINDS INDEX OF FIRST COMMA IN tickets. SETS ticket TO INDEX 0 TO INDEX OF FIRST COMMA.
            if ticket == 'u':  # FINDS COST OF SEAT DEPENDING OF TICKET SELECTED.
                cost = 5
            elif ticket == 'a':
                cost = 10
            else:
                cost = 0
            sqlstatement = f"INSERT INTO AuditoriumBookings VALUES ('{newid}', '{memberid}', '{showingid}', '{seatnum}', '{cost}')"  # INSERT ALL REQUIRED VALUES FOR THE BOOKING.
            cursor.execute(sqlstatement)
            cnxn.commit()  # COMMITS CHANGES TO THE DATABASE.
            newid = newid + 1  # newid INCREMENTED BY 1.
            remove = len(seats) - len(seatnum) - 1  # remove WILL SERVE AS THE INDEX OF WHERE TO TRUNCATE seats.
            seats = seats[-remove:]  # seats WILL HAVE seatnum AND COMMA AFTER seatnum REMOVED.
            tickets = tickets[2:]  # 2 FIRST CHARACTERS (TICKET TYPE AND COMMA) OF tickets REMOVED.
        cnxn.close()  # CLOSES CONNECTION.


def sendemail(email, name, performancename, showingdate, showingtime):
    msg = MIMEMultipart()
    msg['Subject'] = "Your Collyer's booking confirmation"  # SUBJECT OF EMAIL.
    msg['From'] = "EMAIL"  # SENDER OF EMAIL.
    msg['To'] = email  # RECEIVER OF EMAIL.
    text = MIMEText(f"Hi {name},\n\nWe're pleased to say your seats have been booked to view {performancename}, playing in the Duckering Hall on {showingdate} at {showingtime}. \n\nWe look forward to seeing you there!")
    msg.attach(text)  # BODY OF EMAIL
    svr = smtplib.SMTP("smtp.office365.com", 587)  # DEFINES CLIENT SESSION OBJECT.
    svr.ehlo()  # IDENTIFY DOMAIN NAME OF HOST.
    svr.starttls()  # USES SECURE CONNECTION TO SEND EMAIL.
    svr.login("EMAIL", "PASSWORD")  # LOGIN DETAILS FOR SENDER.
    svr.sendmail("EMAIL", email, msg.as_string())  # SENDS EMAIL.
    svr.quit()  # CLOSES CONNECTION.

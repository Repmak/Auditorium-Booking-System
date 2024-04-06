import Auditorium_Functions
import json
from flask import Flask, render_template, request, redirect


app = Flask(__name__)  # CREATES FLASK APPLICATION.


@app.route('/')  # DEFAULT URL, WILL RUN ONCE PROGRAM IS RUN.
def login():
    if invalidcounter == 0:  # invalidcounter WILL BE USED TO CHECK IF INVALID DETAILS HAVE BEEN ENTERED. SET TO 0 BY DEFAULT AS NO DETAILS HAVE BEEN ENTERED YET.
        return render_template('login.html')  # WILL ONLY RETURN login.html IF NO INVALID DETAILS HAVE BEEN ENTERED PREVIOUSLY.
    else:
        return render_template('login.html', invalidloginmsg="Invalid details entered")  # WILL RETURN login.html AND invalidloginmsg SINCE invalidcounter NOT EQUAL TO 0.


@app.route('/noconnection')  # THIS URL WILL BE USED IN THE CASE THAT A WEBPAGE CAN'T BE LOADED DUE TO SERVER BEING DOWN OR WRONG CONNECTION STRING.
def noconnection():
    return render_template('noconnection.html')  # WILL RETURN noconnection.html.


@app.route("/selectperformance", methods=["POST", "GET"])  # POST AND GET REQUESTS USED TO CHECK IF USER HAS LOGGED IN OR NOT.
def selectperformance():
    global invalidcounter  # invalidcounter SET TO GLOBAL SO THAT IT CAN BE CHANGED AND ACCESSED BY OTHER PARTS OF PROGRAM IF INVALID LOGIN DETAILS HAVE BEEN ENTERED.
    if request.method == "POST":  # CODE BELOW WILL BE RUN IF SITE HAS BEEN ACCESSED USING A POST REQUEST.
        try:
            memberid, membertype = Auditorium_Functions.logindetails(request.form.get("email"), request.form.get("password"))  # VERIFIES IF CREDENTIALS ENTERED FROM login.html ARE VALID. LOGIN CREDENTIALS ARE PASSED IN AS PARAMETERS.
            memberinfo = [memberid, membertype]
            showings, performances = Auditorium_Functions.loadperformances(membertype)  # LOADS SHOWINGS AND PERFORMANCES. membertype PASSED IN FOR REVENUE AND ALL SHOWINGS FOR STAFF.
        except:  # IF NO CONNECTION, REDIRECTED TO noconnection.html.
            return redirect('/noconnection')  # WILL RETURN noconnection.html.
        if memberid is None:  # memberid WILL BE EMPTY IF NO RECORD IS FOUND WITH ENTERED LOGIN DETAILS.
            invalidcounter = invalidcounter + 1  # INVALID DETAILS ENTERED, SO invalidcounter INCREMENTED.
            return redirect('/')  # REDIRECTED TO LOGIN PAGE.
        else:
            invalidcounter = 0  # invalidcounter SET BACK TO 0, DETAILS ARE VALID.
            return render_template('step1.html', jsshowings=json.dumps(showings), showings=showings, jsperformances=json.dumps(performances), performances=performances, memberinfo=memberinfo)  # RETURNS step1.html WITH ALL REQUIRED DATA.
    else:  # CODE BELOW WILL BE RUN IF SITE HAS BEEN ACCESSED USING A GET REQUEST.
        return redirect('/')  # REDIRECTED TO LOGIN PAGE.


@app.route('/selectseatstickets', methods=["POST", "GET"])  # POST AND GET REQUESTS USED TO CHECK IF USER HAS LOGGED IN OR NOT.
def selectseatstickets():
    if request.method == "POST":  # CODE BELOW WILL BE RUN IF SITE HAS BEEN ACCESSED USING A POST REQUEST.
        memberid = request.form.get('htmltopython1memberid')  # memberid, membertype, performanceid AND showingid RETURNED FROM HTML FORM.
        membertype = request.form.get('htmltopython1membertype')
        performanceid = request.form.get('htmltopython1performanceid')
        showingid = request.form.get('htmltopython1showingid')
        try:
            seatarray = Auditorium_Functions.loadseats(showingid)  # LOADS seatarray USING THE PARAMETER showingid.
            return render_template('step2.html', jsseatarray=json.dumps(seatarray), memberid=memberid, membertype=membertype, performanceid=performanceid, showingid=showingid)  # RETURNS step2.html WITH ALL REQUIRED DATA.
        except:  # IF NO CONNECTION, REDIRECTED TO noconnection.html.
            return redirect('/noconnection')  # WILL RETURN noconnection.html.
    else:  # CODE BELOW WILL BE RUN IF SITE HAS BEEN ACCESSED USING A GET REQUEST.
        return redirect('/')  # REDIRECTED TO LOGIN PAGE.


@app.route('/seatsbooked', methods=["POST", "GET"])
def seatsbooked():
    if request.method == "POST":  # CODE BELOW WILL BE RUN IF SITE HAS BEEN ACCESSED USING A POST REQUEST.
        memberid = request.form.get('htmltopython2memberid')  # memberid, performanceid, showingid, tickets AND seats RETURNED FROM HTML FORM.
        performanceid = request.form.get('htmltopython2performanceid')
        showingid = request.form.get('htmltopython2showingid')
        tickets = str(request.form.get('htmltopython2tickets'))
        seats = str(request.form.get('htmltopython2seats'))
        try:
            performancename, showingdate, showingtime, email = Auditorium_Functions.confirmationinfo(performanceid, showingid, memberid)  # performanceid, showingid AND memberid PASSED IN AS PARAMETERS TO RETIREVE DETAILS FOR CONFIRMATION PAGE, EMAIL AND TO BOOK RECORDS.
            Auditorium_Functions.bookbooking(memberid, showingid, seats, tickets)  # memberid, showingid, seats AND tickets PASSED IN AS PARAMETERS TO BOOK RECORDS.
            return render_template('step3.html', seats=seats, tickets=tickets, performancename=performancename, showingdate=showingdate, showingtime=showingtime, email=email)  # RETURNS step3.html WITH ALL REQUIRED DATA.
        except:  # IF NO CONNECTION, REDIRECTED TO noconnection.html.
            return redirect('/noconnection')  # WILL RETURN noconnection.html.
    else:  # CODE BELOW WILL BE RUN IF SITE HAS BEEN ACCESSED USING A GET REQUEST.
        return redirect('/')  # REDIRECTED TO LOGIN PAGE.


if __name__ == "__main__":  # EXECUTES FILE WHEN RUN
    invalidcounter = 0  # SETS invalidcounter TO 0 BY DEFAULT
    app.run(debug=True)

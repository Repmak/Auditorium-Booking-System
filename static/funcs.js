var seatarray = []
var ticketarray = []
var convertedseatarray = []
var lastclick = -1
var today = new Date();
today = today.getFullYear() + '/' + String(today.getMonth() + 1).padStart(2, '0') + '/' + String(today.getDate()).padStart(2, '0');  /* CURRENT DATE. */
const alphabet = ['J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']  /* ALPHABET USED FOR CONVERTING SEAT NUMBERS TO A LETTER AND NUMBER. THIS ARRAY ISN'T USED IN THIS FILE, HOWEVER IT IS ACCESSED FROM step2.html. */


function showingselection(){  /* IF nextstepbutton1 HAS THE CLASS nextstepnotallowed ADDED, DENY SUBMIT REQUEST. */
    if (document.getElementById("nextstepbutton1").className === "nextstepnotallowed"){
        return false;
    }
    else{
        return true;
    }
}


function ticketnum(){  /* IF LENGTHS OF ticketarray AND seatarray MATCH, AND ticketarray DOESN'T HAVE LENGTH 0, ACCEPT SUBMIT REQUEST. */
    if (ticketarray.length === seatarray.length && ticketarray.length != 0){
        return true;
    }
    else{
        return false;
    }
}


function totalcost(array){
    let total = 0;
    for (let i = 0; i < array.length; i++){  /* ITERATES THROUGH ticketarray TO CALCULATE total. */
        if (array[i] === "u"){  /* £5 ADDED TO total IF TICKET TYPE IS u. */
            total = total + 5;
        }
        else if (array[i] === "a"){  /* £10 ADDED TO total IF TICKET TYPE IS a. */
            total = total + 10;
        }
    }
    return total  /* total RETURNED TO SUB PROGRAM TO BE DISPLAYED. */
}


function ticketcounter(array, membertype){
    let u18o65counter = 0;
    let adultcounter = 0;
    let staffcounter = 0;
    for (let i = 0; i < array.length; i++){  /* ITERATES THROUGH ticketarray TO CALCULATE NUMBER OF EACH TICKET TYPE SELECTED. */
        if (array[i] == 'u'){
            u18o65counter = u18o65counter + 1;
        }
        else if (array[i] == 'a'){
            adultcounter = adultcounter + 1;
        }
        else {
            staffcounter = staffcounter + 1;
        }

    }
    document.getElementById("u18o65counter").innerHTML = u18o65counter + "x";  /* SETS APPROPRIATE ELEMENT TO ITS COUNTER. */
    document.getElementById("adultcounter").innerHTML = adultcounter + "x";
    if (membertype == 0){  /* IF membertype EQUALS 0, UPDATE STAFF COUNTER AS WELL. */
        document.getElementById("staffcounter").innerHTML = staffcounter + "x";
    }
}


function ticketclick(ticket, membertype) {
    if (ticket.substring(ticket.length - 4) === "plus") {  /* CHECKS IF THE ELEMENT CLICKED HAS AN ID ENDING IN "plus". */
        if (ticketarray.length < seatarray.length){  /* ALLOWS ticket TO BE ADDED TO ticketarray ONLY IF LENGTH OF ticketarray IS SMALLER THAN LENGTH OF seatarray. */
            ticketarray.push(ticket.substring(0, 1));  /* ADDS ticket TO ticketarray. */
        }
    }
    else {
        let index = ticketarray.indexOf(ticket.substring(0, 1));  /* FINDS IF ticket IS IN ticketarray. WILL RETURN THE POSITION OF ticket IF FOUND. */
        if (index > -1) {  /* ALLOWS TICKET TO BE REMOVED IF FOUND */
            ticketarray.splice(index, 1);  /* REMOVES ticket FROM ticketarray. */
        }
    }
	document.getElementById("numticketsselected").innerHTML = ticketarray.length + "/" + seatarray.length;  /* UPDATES NUMBER OF TICKETS SELECTED. */
	let total = totalcost.call(this, ticketarray);  /* CALLS totalcost TO FIND TOTAL COST. */
	ticketcounter.call(this, ticketarray, membertype);  /* CALLS ticketcounter TO AMOUNT OF EACH TICKET SELECTED. */
	document.getElementById("total").innerHTML = "Total: £" + total;  /* SETS total TO THE ELEMENT DISPLAYING TOTAL COST. */
	if (ticketarray.length === 0 || ticketarray.length != seatarray.length){  /* ADDS CLASS nextstepnotallowed IF THE LENGTH OF ticketarray IS 0 OR IF THE LENGTHS OF BOTH ARRAYS AREN'T THE SAME. */
		document.getElementById("nextstepbutton2").classList.remove("nextstep");
		document.getElementById("nextstepbutton2").classList.add("nextstepnotallowed");
	}
	else{  /* OTHERWISE, ADDS CLASS nextstep. */
		document.getElementById("nextstepbutton2").classList.remove("nextstepnotallowed");
		document.getElementById("nextstepbutton2").classList.add("nextstep");
	}
	document.getElementById("htmltopython2seats").value = seatarray + ",";  /* UPDATES HIDDEN FORMS (WHICH WILL BE USED TO TRANSFER DATA BACK TO PYTHON). */
	document.getElementById("htmltopython2tickets").value = ticketarray + ",";  /* UPDATES HIDDEN FORMS (WHICH WILL BE USED TO TRANSFER DATA BACK TO PYTHON). */
}


function seatclick(seatnum, membertype) {
	let checked = document.getElementById(seatnum).checked;
	let seatclasslist = document.getElementById(seatnum + "span").className;
	if (seatclasslist === "seatunavailable"){  /* CHECK IF SEAT IS UNAVAILABLE. */
	    document.getElementById(seatnum).checked = false;  /* DENY SEAT TO BE CHECKED SINCE IT IS UNAVAILABLE. */
	}
	else {  /* OTHERWISE, PERMIT SEAT TO BE CHECKED/UNCHECKED. */
	    if (checked){  /* SEAT HAS BEEN CHECKED. */
	        document.getElementById(seatnum + "span").classList.remove("seatavailable");
		    document.getElementById(seatnum + "span").classList.add("seatchecked");  /* ADD seatchecked CLASS TO SEAT. */
		    seatarray.push(seatnum);
		    if (seatarray.length > 8){  /* ENSURES THAT THE NUMBER OF SEATS SELECTED DOESN'T EXCEED 8. */
		        document.getElementById(seatarray[0]).checked = false;  /* IF NUMBER OF SEATS SELECTED EXCEEDS 8, FIRST SEAT IN seatarray WILL BE REMOVED. */
		        document.getElementById(seatarray[0] + "span").classList.remove("seatchecked");
		        document.getElementById(seatarray[0] + "span").classList.add("seatavailable");  /* ADD seatavailable CLASS TO SEAT THAT WILL BE REMOVED FROM seatarray. */
		        seatarray.splice(0, 1);  /* SEAT REMOVED FROM seatarray. */
		    }
	    }
	    else {  /* SEAT HAS BEEN UNCHECKED. */
	        document.getElementById(seatnum + "span").classList.remove("seatchecked");
	        document.getElementById(seatnum + "span").classList.add("seatavailable");  /* ADD seatavailable CLASS TO SEAT. */
            if (seatarray.length === ticketarray.length){  /* IF THE NUMBER OF SEATS SELECTED MATCHES THE NUMBER OF TICKETS SELECTED, A TICKET MUST BE REMOVED SINCE THE NUMBER OF TICKETS CAN'T EXCEED THE NUMBER OF SEATS SELECTED. */
                ticketarray.splice(-1, 1);  /* REMOVES LAST TICKET FROM ticketarray. */
                let total = totalcost.call(this, ticketarray);  /* RECALCULATES TOTAL COST. */
                ticketcounter.call(this, ticketarray, membertype);  /* RECALCULATES THE NUMBER OF TICKETS SELECTED. */
                document.getElementById("total").innerHTML = "Total: £" + total;  /* SETS total TO BE DISPLAYED. */
            }
            seatarray.splice(seatarray.indexOf(seatnum), 1);  /* SEAT CAN NOW BE UNCHECKED. IT IS REMOVED FROM THE ARRAY. */
	    }
		if (ticketarray.length === 0 || ticketarray.length != seatarray.length){  /* ADDS CLASS nextstepnotallowed IF THE LENGTH OF ticketarray IS 0 OR IF THE LENGTHS OF BOTH ARRAYS AREN'T THE SAME. */
			document.getElementById("nextstepbutton2").classList.remove("nextstep")
			document.getElementById("nextstepbutton2").classList.add("nextstepnotallowed")
		}
		else{  /* OTHERWISE, ADDS CLASS nextstep. */
			document.getElementById("nextstepbutton2").classList.remove("nextstepnotallowed")
			document.getElementById("nextstepbutton2").classList.add("nextstep")
		}
	    document.getElementById("numticketsselected").innerHTML = ticketarray.length + "/" + seatarray.length;  /* UPDATES NUMBER OF TICKETS SELECTED. */
	    document.getElementById("htmltopython2seats").value = seatarray + ",";  /* UPDATES HIDDEN FORMS (WHICH WILL BE USED TO TRANSFER DATA BACK TO PYTHON). */
	    document.getElementById("htmltopython2tickets").value = ticketarray + ",";  /* UPDATES HIDDEN FORMS (WHICH WILL BE USED TO TRANSFER DATA BACK TO PYTHON). */
	}
}


function selector(i, k, showings, performances, memberinfo) {
    if (lastclick === -1){  /* IF lastclick EQUALS -1, THE SUB PROGRAM KNOWS THAT NO SHOWING HAS PREVIOUSLY BEEN SELECTED. THIS IS BECAUSE lastclick WAS SET TO -1 THE START OF THE PROGRAM. */
        document.getElementById("nextstepbutton1").classList.remove("nextstepnotallowed")
        document.getElementById("nextstepbutton1").classList.add("nextstep")  /* ADDS CLASS nextstep SINCE A SHOWING HAS NOW BEEN SELECTED. */
        document.getElementById("showing" + showings[k][0]).classList.add("showingbuttonboxchecked");
        lastclick = showings[k][0];
        document.getElementById("htmltopython1memberid").value = memberinfo[0];  /* UPDATES HIDDEN FORMS (WHICH WILL BE USED TO TRANSFER DATA BACK TO PYTHON). */
        document.getElementById("htmltopython1membertype").value = memberinfo[1];  /* UPDATES HIDDEN FORMS (WHICH WILL BE USED TO TRANSFER DATA BACK TO PYTHON). */
    }
    else if (lastclick === showings[k][0]){
        //
    }
    else{
        document.getElementById("showing" + lastclick).classList.remove("showingbuttonboxchecked");  /* REMOVES showingbuttonboxchecked CLASS FROM PREVIOUSLY SELECTED SHOWING. */
        document.getElementById("showing" + showings[k][0]).classList.add("showingbuttonboxchecked");  /* ADDS showingbuttonboxchecked CLASS TO SELECTED SHOWING. */
        lastclick = showings[k][0];  /* UPDATES lastclick TO ID OF NEW SHOWING. */
    }
	document.getElementById("name").innerHTML = performances[i][1];  /* UPDATES name, genre, dateandtime, etc TO DETAILS OF SELECTED PERFORMANCE. */
	document.getElementById("genre").innerHTML = "Genre: " + performances[i][2];
	document.getElementById("dateandtime").innerHTML = "Date and time: " + showings[k][1] + " at " + showings[k][2].substring(0, 5);
	document.getElementById("descr").innerHTML = performances[i][4];
	document.getElementById("rating").innerHTML = "Rating: " + performances[i][5];
	document.getElementById("duration").innerHTML = "Duration: " + performances[i][6].substring(0, 8);
    document.getElementById("image").src = performances[i][3];
    if (memberinfo[1] === 0) {  /* UPDATES revenue IF USER IS A STAFF. */
        document.getElementById("revenue").innerHTML = "Revenue: £" + showings[k][4];
        document.getElementById("seatsrem").innerHTML = "Number of seats remaining: " + showings[k][5];
        var showingdate = showings[k][1].substring(0, 4) + "/" + showings[k][1].substring(5, 7) + "/" + showings[k][1].substring(8, 10)
        if (showingdate < today){  /* CHECKS IF SELECTED SHOWING HAS ALREADY BEEN PLAYED. */
            document.getElementById("nextstepbutton1").classList.remove("nextstep")
            document.getElementById("nextstepbutton1").classList.add("nextstepnotallowed")  /* IF SHOWING DATE IS IN PAST, ADD CLASS nextstepnotallowed to nextstepbutton1. */
        }
        else {
            document.getElementById("nextstepbutton1").classList.remove("nextstepnotallowed")
            document.getElementById("nextstepbutton1").classList.add("nextstep")  /* OTHERWISE, ADD CLASS nextstep to nextstepbutton1. */
        }
    }
    else{  /* NOT MEMBER OF STAFF. */
        document.getElementById("seatsrem").innerHTML = "Number of seats remaining: " + showings[k][4];
    }
    document.getElementById("htmltopython1performanceid").value = performances[i][0];  /* UPDATES HIDDEN FORMS (WHICH WILL BE USED TO TRANSFER DATA BACK TO PYTHON). */
    document.getElementById("htmltopython1showingid").value = showings[k][0];  /* UPDATES HIDDEN FORMS (WHICH WILL BE USED TO TRANSFER DATA BACK TO PYTHON). */
}

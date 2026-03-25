import re
import requests
import whois
from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "changeme-local-dev-key"

AREA_CODES = {
    # Alabama
    "205": "Birmingham, AL", "251": "Mobile, AL", "256": "Huntsville, AL", "334": "Montgomery, AL",
    # Alaska
    "907": "Alaska (statewide)",
    # Arizona
    "480": "Scottsdale/Tempe, AZ", "520": "Tucson, AZ", "602": "Phoenix, AZ",
    "623": "West Phoenix, AZ", "928": "Flagstaff/Yuma, AZ",
    # Arkansas
    "479": "Fort Smith, AR", "501": "Little Rock, AR", "870": "Jonesboro, AR",
    # California
    "209": "Stockton/Modesto, CA", "213": "Los Angeles, CA", "279": "Sacramento, CA",
    "310": "Los Angeles (West), CA", "323": "Los Angeles, CA", "341": "Oakland, CA",
    "408": "San Jose, CA", "415": "San Francisco, CA", "424": "Los Angeles (West), CA",
    "442": "Palm Springs, CA", "510": "Oakland, CA", "530": "Sacramento (North), CA",
    "559": "Fresno, CA", "562": "Long Beach, CA", "619": "San Diego, CA",
    "626": "Pasadena, CA", "628": "San Francisco, CA", "650": "San Mateo, CA",
    "657": "Orange County (North), CA", "661": "Bakersfield, CA", "669": "San Jose, CA",
    "707": "Santa Rosa, CA", "714": "Orange County, CA", "747": "San Fernando Valley, CA",
    "760": "Palm Springs/San Bernardino, CA", "805": "Santa Barbara/Oxnard, CA",
    "818": "San Fernando Valley, CA", "831": "Monterey/Santa Cruz, CA",
    "858": "San Diego (North), CA", "909": "San Bernardino, CA", "916": "Sacramento, CA",
    "925": "Walnut Creek, CA", "949": "Irvine/Newport Beach, CA", "951": "Riverside, CA",
    # Colorado
    "303": "Denver, CO", "719": "Colorado Springs, CO", "720": "Denver, CO",
    "970": "Fort Collins/Grand Junction, CO",
    # Connecticut
    "203": "New Haven/Bridgeport, CT", "475": "New Haven/Bridgeport, CT",
    "860": "Hartford, CT", "959": "Hartford, CT",
    # Delaware
    "302": "Delaware (statewide)",
    # Florida
    "239": "Fort Myers/Naples, FL", "305": "Miami, FL", "321": "Orlando (East), FL",
    "352": "Gainesville, FL", "386": "Daytona Beach, FL", "407": "Orlando, FL",
    "448": "Orlando, FL", "561": "West Palm Beach, FL", "689": "Orlando, FL",
    "727": "St. Petersburg, FL", "754": "Fort Lauderdale, FL", "772": "Port St. Lucie, FL",
    "786": "Miami, FL", "813": "Tampa, FL", "850": "Tallahassee/Pensacola, FL",
    "863": "Lakeland, FL", "904": "Jacksonville, FL", "941": "Sarasota, FL",
    "954": "Fort Lauderdale, FL",
    # Georgia
    "229": "Albany, GA", "404": "Atlanta, GA", "470": "Atlanta, GA",
    "478": "Macon, GA", "678": "Atlanta, GA", "706": "Columbus/Augusta, GA",
    "762": "Columbus/Augusta, GA", "770": "Atlanta (Suburbs), GA", "912": "Savannah, GA",
    # Hawaii
    "808": "Hawaii (statewide)",
    # Idaho
    "208": "Idaho (statewide)", "986": "Boise, ID",
    # Illinois
    "217": "Springfield, IL", "224": "Chicago (North Suburbs), IL",
    "309": "Peoria, IL", "312": "Chicago, IL", "331": "Aurora, IL",
    "618": "East St. Louis, IL", "630": "Naperville/Aurora, IL",
    "708": "Chicago (South Suburbs), IL", "773": "Chicago, IL",
    "779": "Rockford, IL", "815": "Rockford/Joliet, IL", "847": "Chicago (North Suburbs), IL",
    "872": "Chicago, IL",
    # Indiana
    "219": "Gary/Hammond, IN", "260": "Fort Wayne, IN", "317": "Indianapolis, IN",
    "463": "Indianapolis, IN", "574": "South Bend, IN", "765": "Muncie/Lafayette, IN",
    "812": "Evansville, IN", "930": "Evansville, IN",
    # Iowa
    "319": "Cedar Rapids, IA", "515": "Des Moines, IA", "563": "Davenport, IA",
    "641": "Mason City, IA", "712": "Sioux City, IA",
    # Kansas
    "316": "Wichita, KS", "620": "Dodge City, KS", "785": "Topeka, KS",
    "913": "Kansas City, KS",
    # Kentucky
    "270": "Bowling Green, KY", "364": "Bowling Green, KY", "502": "Louisville, KY",
    "606": "Ashland, KY", "859": "Lexington, KY",
    # Louisiana
    "225": "Baton Rouge, LA", "318": "Shreveport, LA", "337": "Lafayette, LA",
    "504": "New Orleans, LA", "985": "Houma/Thibodaux, LA",
    # Maine
    "207": "Maine (statewide)",
    # Maryland
    "240": "Rockville/Bethesda, MD", "301": "Rockville/Bethesda, MD",
    "410": "Baltimore, MD", "443": "Baltimore, MD", "667": "Baltimore, MD",
    # Massachusetts
    "339": "Boston (Suburbs), MA", "351": "Lowell, MA", "413": "Springfield, MA",
    "508": "Worcester, MA", "617": "Boston, MA", "774": "Worcester, MA",
    "781": "Boston (North/South Suburbs), MA", "857": "Boston, MA",
    "978": "Lowell/Lawrence, MA",
    # Michigan
    "231": "Traverse City, MI", "248": "Pontiac/Troy, MI", "269": "Kalamazoo, MI",
    "313": "Detroit, MI", "517": "Lansing, MI", "586": "Macomb County, MI",
    "616": "Grand Rapids, MI", "734": "Ann Arbor, MI", "810": "Flint, MI",
    "906": "Upper Peninsula, MI", "947": "Pontiac/Troy, MI", "989": "Saginaw, MI",
    # Minnesota
    "218": "Duluth, MN", "320": "St. Cloud, MN", "507": "Rochester, MN",
    "612": "Minneapolis, MN", "651": "St. Paul, MN", "763": "Minneapolis (Suburbs), MN",
    "952": "Bloomington/Eden Prairie, MN",
    # Mississippi
    "228": "Biloxi/Gulfport, MS", "601": "Jackson, MS", "662": "Tupelo, MS",
    "769": "Jackson, MS",
    # Missouri
    "314": "St. Louis, MO", "417": "Springfield, MO", "573": "Columbia, MO",
    "636": "St. Louis (West), MO", "660": "Sedalia, MO", "816": "Kansas City, MO",
    "975": "Kansas City, MO",
    # Montana
    "406": "Montana (statewide)",
    # Nebraska
    "308": "Grand Island, NE", "402": "Omaha, NE", "531": "Omaha, NE",
    # Nevada
    "702": "Las Vegas, NV", "725": "Las Vegas, NV", "775": "Reno, NV",
    # New Hampshire
    "603": "New Hampshire (statewide)",
    # New Jersey
    "201": "Jersey City/Hackensack, NJ", "551": "Jersey City/Hackensack, NJ",
    "609": "Trenton, NJ", "640": "Trenton, NJ", "732": "New Brunswick, NJ",
    "848": "New Brunswick, NJ", "856": "Camden, NJ", "862": "Newark, NJ",
    "908": "Elizabeth, NJ", "973": "Newark, NJ",
    # New Mexico
    "505": "Albuquerque, NM", "575": "Las Cruces, NM",
    # New York
    "212": "New York City (Manhattan), NY", "315": "Syracuse, NY",
    "332": "New York City (Manhattan), NY", "347": "New York City (Brooklyn/Queens/Bronx/Staten Island), NY",
    "516": "Nassau County (Long Island), NY", "518": "Albany, NY",
    "585": "Rochester, NY", "607": "Binghamton, NY", "631": "Suffolk County (Long Island), NY",
    "646": "New York City (Manhattan), NY", "680": "Syracuse, NY",
    "716": "Buffalo, NY", "718": "New York City (Brooklyn/Queens/Bronx/Staten Island), NY",
    "838": "Albany, NY", "845": "Poughkeepsie, NY", "914": "Yonkers/White Plains, NY",
    "917": "New York City, NY", "929": "New York City (Brooklyn/Queens/Bronx/Staten Island), NY",
    "934": "Suffolk County (Long Island), NY",
    # North Carolina
    "252": "Rocky Mount, NC", "336": "Greensboro, NC", "704": "Charlotte, NC",
    "743": "Greensboro, NC", "828": "Asheville, NC", "910": "Fayetteville, NC",
    "919": "Raleigh, NC", "980": "Charlotte, NC", "984": "Raleigh, NC",
    # North Dakota
    "701": "North Dakota (statewide)",
    # Ohio
    "216": "Cleveland, OH", "220": "Newark/Zanesville, OH", "234": "Akron, OH",
    "330": "Akron/Youngstown, OH", "380": "Columbus, OH", "419": "Toledo, OH",
    "440": "Cleveland (West), OH", "513": "Cincinnati, OH", "567": "Toledo, OH",
    "614": "Columbus, OH", "740": "Zanesville/Athens, OH", "937": "Dayton, OH",
    # Oklahoma
    "405": "Oklahoma City, OK", "539": "Tulsa, OK", "580": "Lawton, OK",
    "918": "Tulsa, OK",
    # Oregon
    "458": "Eugene, OR", "503": "Portland, OR", "541": "Eugene/Bend, OR",
    "971": "Portland, OR",
    # Pennsylvania
    "215": "Philadelphia, PA", "267": "Philadelphia, PA", "272": "Scranton, PA",
    "412": "Pittsburgh, PA", "445": "Philadelphia, PA", "484": "Allentown, PA",
    "570": "Scranton/Wilkes-Barre, PA", "610": "Allentown/Reading, PA",
    "717": "Harrisburg, PA", "724": "Pittsburgh (West), PA", "814": "Erie, PA",
    "835": "Allentown, PA", "878": "Pittsburgh, PA",
    # Rhode Island
    "401": "Rhode Island (statewide)",
    # South Carolina
    "803": "Columbia, SC", "843": "Charleston, SC", "854": "Charleston, SC",
    "864": "Greenville, SC",
    # South Dakota
    "605": "South Dakota (statewide)",
    # Tennessee
    "423": "Chattanooga, TN", "615": "Nashville, TN", "629": "Nashville, TN",
    "731": "Jackson, TN", "865": "Knoxville, TN", "901": "Memphis, TN",
    "931": "Clarksville, TN",
    # Texas
    "210": "San Antonio, TX", "214": "Dallas, TX", "254": "Waco, TX",
    "281": "Houston (Suburbs), TX", "325": "Abilene, TX", "346": "Houston, TX",
    "361": "Corpus Christi, TX", "409": "Beaumont, TX", "430": "Tyler, TX",
    "432": "Midland/Odessa, TX", "469": "Dallas, TX", "512": "Austin, TX",
    "682": "Fort Worth, TX", "713": "Houston, TX", "726": "San Antonio, TX",
    "737": "Austin, TX", "806": "Lubbock/Amarillo, TX", "817": "Fort Worth, TX",
    "830": "San Antonio (West), TX", "832": "Houston, TX", "903": "Tyler, TX",
    "915": "El Paso, TX", "936": "Conroe/Huntsville, TX", "940": "Wichita Falls, TX",
    "956": "Laredo/McAllen, TX", "972": "Dallas, TX", "979": "Bryan/College Station, TX",
    # Utah
    "385": "Salt Lake City, UT", "435": "St. George/Provo, UT", "801": "Salt Lake City, UT",
    # Vermont
    "802": "Vermont (statewide)",
    # Virginia
    "276": "Bristol, VA", "434": "Charlottesville, VA", "540": "Roanoke, VA",
    "571": "Northern Virginia, VA", "703": "Northern Virginia, VA",
    "757": "Norfolk/Virginia Beach, VA", "804": "Richmond, VA", "826": "Richmond, VA",
    "948": "Norfolk/Virginia Beach, VA",
    # Washington
    "206": "Seattle, WA", "253": "Tacoma, WA", "360": "Olympia/Bellingham, WA",
    "425": "Bellevue/Redmond, WA", "509": "Spokane, WA", "564": "Olympia/Bellingham, WA",
    # West Virginia
    "304": "West Virginia (statewide)", "681": "West Virginia (statewide)",
    # Wisconsin
    "262": "Racine/Kenosha, WI", "414": "Milwaukee, WI", "534": "Eau Claire, WI",
    "608": "Madison, WI", "715": "Eau Claire/Wausau, WI", "920": "Green Bay, WI",
    # Wyoming
    "307": "Wyoming (statewide)",
    # Washington D.C.
    "202": "Washington, D.C.",

    # --- CANADA ---
    # Alberta
    "403": "Calgary, AB", "587": "Alberta (overlay)", "780": "Edmonton, AB",
    "825": "Alberta (overlay)",
    # British Columbia
    "236": "British Columbia (overlay)", "250": "Victoria/Interior, BC",
    "604": "Vancouver, BC", "672": "British Columbia (overlay)", "778": "British Columbia (overlay)",
    # Manitoba
    "204": "Winnipeg, MB", "431": "Winnipeg, MB",
    # New Brunswick
    "506": "New Brunswick (statewide)",
    # Newfoundland and Labrador
    "709": "Newfoundland and Labrador",
    # Nova Scotia
    "782": "Nova Scotia (overlay)", "902": "Nova Scotia",
    # Ontario
    "226": "London/Windsor, ON", "249": "Sault Ste. Marie, ON",
    "289": "Hamilton/Niagara, ON", "343": "Ottawa, ON", "365": "Hamilton/Niagara, ON",
    "416": "Toronto, ON", "437": "Toronto, ON", "519": "London/Windsor, ON",
    "548": "London/Windsor, ON", "613": "Ottawa, ON", "647": "Toronto, ON",
    "705": "Sudbury/Barrie, ON", "742": "Kitchener/Waterloo, ON",
    "807": "Thunder Bay, ON", "905": "Hamilton/Niagara, ON",
    # Prince Edward Island
    "782": "Prince Edward Island / Nova Scotia (overlay)",
    # Quebec
    "263": "Montreal, QC", "354": "Quebec City, QC", "367": "Quebec City, QC",
    "418": "Quebec City, QC", "438": "Montreal, QC", "450": "Montreal (Suburbs), QC",
    "514": "Montreal, QC", "579": "Montreal (Suburbs), QC",
    "581": "Quebec City, QC", "819": "Sherbrooke/Gatineau, QC",
    "873": "Sherbrooke/Gatineau, QC",
    # Saskatchewan
    "306": "Saskatchewan (statewide)", "639": "Saskatchewan (overlay)",
    # Northwest Territories, Nunavut, Yukon
    "867": "Northwest Territories / Nunavut / Yukon",
}


def is_ip_address(value):
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", value))


def is_domain(value):
    return bool(re.match(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", value))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "areacode":
            ac_query = request.form.get("area_code", "").strip()
            if not ac_query.isdigit() or len(ac_query) != 3:
                session["ac"] = {"query": ac_query, "error": "Please enter a valid 3-digit area code."}
            elif ac_query in AREA_CODES:
                session["ac"] = {"query": ac_query, "result": AREA_CODES[ac_query]}
            else:
                session["ac"] = {"query": ac_query, "error": f"Area code {ac_query} was not found."}

        elif action == "domain":
            domain_query = request.form.get("domain_query", "").strip().lower()
            if not is_domain(domain_query):
                session["domain"] = {"query": domain_query, "error": "Please enter a valid domain (e.g. google.com)."}
            else:
                try:
                    w = whois.whois(domain_query)
                    registrar = w.registrar or "N/A"
                    creation = w.creation_date
                    if isinstance(creation, list):
                        creation = creation[0]
                    creation_str = creation.strftime("%B %d, %Y") if creation else "N/A"
                    session["domain"] = {"query": domain_query, "result": {"domain": domain_query, "registrar": registrar, "created": creation_str}}
                except Exception:
                    session["domain"] = {"query": domain_query, "error": f"Could not retrieve WHOIS data for '{domain_query}'."}

        elif action == "ip":
            ip_query = request.form.get("ip_query", "").strip()
            if not is_ip_address(ip_query):
                session["ip"] = {"query": ip_query, "error": "Please enter a valid IP address (e.g. 8.8.8.8)."}
            else:
                try:
                    resp = requests.get(f"http://ip-api.com/json/{ip_query}", timeout=5)
                    data = resp.json()
                    if data.get("status") == "success":
                        session["ip"] = {"query": ip_query, "result": {
                            "ip": ip_query,
                            "city": data.get("city", "N/A"),
                            "region": data.get("regionName", "N/A"),
                            "country": data.get("country", "N/A"),
                            "isp": data.get("isp", "N/A"),
                            "org": data.get("org", "N/A"),
                            "lat": data.get("lat", "N/A"),
                            "lon": data.get("lon", "N/A"),
                        }}
                    else:
                        session["ip"] = {"query": ip_query, "error": f"Could not get geolocation for {ip_query}."}
                except Exception:
                    session["ip"] = {"query": ip_query, "error": "Failed to reach geolocation service. Check your internet connection."}

        elif action == "clear":
            session.clear()

    ac = session.get("ac", {})
    domain = session.get("domain", {})
    ip = session.get("ip", {})

    return render_template(
        "index.html",
        ac_result=ac.get("result"), ac_error=ac.get("error"), ac_query=ac.get("query", ""),
        domain_result=domain.get("result"), domain_error=domain.get("error"), domain_query=domain.get("query", ""),
        ip_result=ip.get("result"), ip_error=ip.get("error"), ip_query=ip.get("query", ""),
    )


@app.route("/api", methods=["POST"])
def api():
    action = request.form.get("action")

    if action == "areacode":
        query = request.form.get("area_code", "").strip()
        if not query.isdigit() or len(query) != 3:
            return jsonify({"error": "Please enter a valid 3-digit area code."})
        elif query in AREA_CODES:
            return jsonify({"result": AREA_CODES[query]})
        else:
            return jsonify({"error": f"Area code {query} was not found."})

    elif action == "domain":
        domain_query = request.form.get("domain_query", "").strip().lower()
        if not is_domain(domain_query):
            return jsonify({"error": "Please enter a valid domain (e.g. google.com)."})
        try:
            w = whois.whois(domain_query)
            registrar = w.registrar or "N/A"
            creation = w.creation_date
            if isinstance(creation, list):
                creation = creation[0]
            creation_str = creation.strftime("%B %d, %Y") if creation else "N/A"
            return jsonify({"domain": domain_query, "registrar": registrar, "created": creation_str})
        except Exception:
            return jsonify({"error": f"Could not retrieve WHOIS data for '{domain_query}'."})

    elif action == "ip":
        ip_query = request.form.get("ip_query", "").strip()
        if not is_ip_address(ip_query):
            return jsonify({"error": "Please enter a valid IP address (e.g. 8.8.8.8)."})
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip_query}", timeout=5)
            data = resp.json()
            if data.get("status") == "success":
                return jsonify({
                    "ip": ip_query,
                    "city": data.get("city", "N/A"),
                    "region": data.get("regionName", "N/A"),
                    "country": data.get("country", "N/A"),
                    "isp": data.get("isp", "N/A"),
                    "org": data.get("org", "N/A"),
                    "lat": data.get("lat", "N/A"),
                    "lon": data.get("lon", "N/A"),
                })
            else:
                return jsonify({"error": f"Could not get geolocation for {ip_query}."})
        except Exception:
            return jsonify({"error": "Failed to reach geolocation service."})

    return jsonify({"error": "Invalid request."})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

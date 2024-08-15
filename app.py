from flask import Flask, jsonify, Response, make_response, request
import requests
import uuid
import base64
from bs4 import BeautifulSoup
import re
import html
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

VCsessions = {}

@app.route("/api/v1/getCaptcha", methods=["POST"])
def getCaptcha():
    try:
        captcha = "https://vcourts.gov.in/virtualcourt/securimage/securimage_show.php"
        stateCode = request.json.get("stateCode")
        session = requests.Session()
        id = str(uuid.uuid4())

        idx = stateCode.find("~")
        v_token = stateCode[idx + 1:]

        initialPostData = {
            "x": "setStateCode",
            "state_code": stateCode,
            "vajax": "Y",
            "v_token": "",
        }

        response = session.post(
            "https://vcourts.gov.in/virtualcourt/indexajax.php", data=initialPostData
        )

        response = session.get(captcha)
        captchaBase64 = base64.b64encode(response.content).decode("utf-8")

        # # For Testing Purpose only

        # imageString = f'<img src="data:image/png;base64,{captchaBase64}" alt="captcha">'
        # with open('captcha.html','w') as f:
        #     f.write(imageString)   
        #     f.close()

        # #

        VCsessions[id] = {
            "session": session,
            "v_token": v_token
        }

        json_response = {
            "sessionId": id,
            "image": "data:image/png;base64," + captchaBase64,
        }

        return jsonify(json_response)
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching captcha"})
    

@app.route("/api/v1/getChallanDetails", methods=["POST"])
def getChallanDetails():
    try:
        sessionId = request.json.get("sessionId")
        vehicleNo = request.json.get("vehicleNo")
        captcha = request.json.get("captcha")

        user = VCsessions.get(sessionId)

        session = user['session']
        if session is None:
            return jsonify({"error": "Invalid session id"})

        vehiclePostData = {
            "x": "fetchpolicecases",
            "challan_no": "",
            "vehicle_no": vehicleNo,
            "vajax": "Y",
            "v_token": user['v_token'],
            "fcaptcha_code": captcha,
        }

        responseAfterCapctha = session.post(
            "https://vcourts.gov.in/virtualcourt/admin/mobilesearchajax.php",
            data=vehiclePostData,
        )

        soup = BeautifulSoup(responseAfterCapctha.text, 'html.parser')

        viewBtns = soup.find_all('a', class_='viewDetlink')
        onclickTexts = [viewBtn.get('onclick') for viewBtn in viewBtns]

        challanFetchingData = []
        
        for i in range(len(onclickTexts)):
            pattern = re.compile(r"'(.*?)'")
            values = pattern.findall(onclickTexts[i])
            
            data = {
                "ciNo": values[0],
                "partyNo": values[1],
                "efilNo": values[2],
                "archieveFlag":values[3]
            }

            challanFetchingData.append(data)
        
        challans = []
        for i in range(len(challanFetchingData)):

            challanPostData = {
                "cino": challanFetchingData[i]['ciNo'],
                "party_no": challanFetchingData[i]['partyNo'],
                "efilno": challanFetchingData[i]['efilNo'],
                "archive_flag": challanFetchingData[i]['archieveFlag'],
                "vajax": "Y",
                "v_token": user['v_token']
            }
        
            responseAfterData = session.post(
                "https://vcourts.gov.in/virtualcourt/admin/case_history_partywise.php",
                data=challanPostData,
            )
            htmlString = responseAfterData.text
            cleaned_html_string = htmlString.replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\\', '')
            cleaned_html_string = html.unescape(cleaned_html_string)
            
            soup2 = BeautifulSoup(cleaned_html_string, 'html.parser')
            tables = soup2.find_all('table')

            index = 0
            if(len(tables)==3):
                index = 1
            
            partyDetailsTbody = tables[index].find_all('tbody')
            offenceTbody = tables[index+1].find_all('tbody')

            partyDetailsTrows = partyDetailsTbody[0].find_all('tr')
            statusDetailsTrows = partyDetailsTbody[1].find_all('tr')
            offenceTrows = offenceTbody[0].find_all('tr')
            offenceTdata = offenceTrows[0].find_all('td')

            challanNumber = partyDetailsTrows[3].find_all('td')[1].get_text()
            challanDate = partyDetailsTrows[4].find_all('td')[1].get_text()
            partyName = partyDetailsTrows[5].find_all('td')[1].get_text()
            placeOfOffence = partyDetailsTrows[6].find_all('td')[1].get_text()
            districtName = partyDetailsTrows[7].find_all('td')[1].get_text()

            recievedDate = statusDetailsTrows[0].find_all('td')[1].get_text()
            verifiedDate = statusDetailsTrows[1].find_all('td')[1].get_text()
            allocatedDate = statusDetailsTrows[2].find_all('td')[1].get_text()

            offenceCode = offenceTdata[0].get_text()
            offence = offenceTdata[1].get_text()
            act = offenceTdata[2].get_text()
            section = offenceTdata[3].get_text()
            fine = offenceTdata[4].get_text()

            challan = {
                "partyName": partyName,
                "challanNumber": challanNumber,
                "challanDate": challanDate,
                "amount": fine,
                "placeOfOffence": placeOfOffence,
                "district": districtName,
                "status": {
                    "recievedDate": recievedDate,
                    "verifiedDate": verifiedDate,
                    "allocatedDate": allocatedDate
                },
                "offenceDetails": {
                    "offenceCode":offenceCode,
                    "offence":offence,
                    "act": act,
                    "section": section
                }
            }
            challans.append(challan)

        
        return jsonify({"numberOfChallans":len(challans), "challans": challans})
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching Challan Details"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host='0.0.0.0', port=5001)

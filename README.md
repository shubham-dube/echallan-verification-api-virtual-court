# Virtual Court eChallan API

This API fetches e-challan data for a vehicle with registration number from virtual court website for easy verification of e-challans

## Table of Contents

- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)
- [Endpoints](#EndPoints)
- [State Codes](#StateCodes)
- [Support](#Support)
- [Contribution](#Contribution)

## Features

- It Maintains session information for handling dynamic captcha url.
- Send vehicle number and captcha code to check e-Challan details.
- Return eChallan details in a structured JSON format.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shubham-dube/echallan-verification-api-virtual-court.git
   cd echallan-verification-api-virtual-court
   
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate # On Linux use `source venv/bin/activate`
   
3. Install the dependencies:
   ```bash
   pip install flask requests uuid base64 bs4 re html

4. Run the Application:
   ```bash
   python app.py
 *The API will be available at http://127.0.0.1:5000 .*
 
## Usage
- Show States to select for the user and when user selects state, send its state code to the backend.
- Show the captcha recieved to the user and two inputs to enter captcha and vehicle number
- Send the vehicle number entered and captcha along with the session id recieved.
- You will get all the challans which are in virtual court for that vehicle in that state.
  
## EndPoints

### Fetching Captcha Using State Code

**Endpoint:** `/api/v1/getCaptcha`

**Method:** `POST`

**Description:** `This Endpoint selects the state on which you want to search and sends that state-code to the backend`

**Request Body:**
```json
{
  "stateCode": "85~HRCV01"
}
```
*State Codes are given at the last with State Names*

**Response**
```json
{
  "sessionId": true,
  "image": 'data:image/png;base64, captchaBase64 '
}
```
**Status Codes**
- 200 OK : `Captcha Recieved for the Given State Code`

### Get Vehicle Challan Details

**Endpoint:** `/api/v1/getChallanDetails`

**Method:** `POST`

**Description:** `Submits the vehicle number and captcha given to the website and extract or scrap further challan data`

**Request Body:**
```json
{
  "sessionId": "OBTAINED ON FETCHING CAPTCHA",
  "vehicleNo": "HR55AB1234",
  "captcha": "your_captcha_here"
}
```
**Response**
```json
{
  "numberOfChallans": "NumberOfChallan",
  "challans": [
          {
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
        ]
}
```
**Status Codes**
- 200 OK : `Data Retrieved Successfuly`
  
## State Codes and Departments
Here are the state codes and their corresponding department names that you can use with the API:

| State Code            | Department Name                                  |
|-----------------------|--------------------------------------------------|
| 6~ASVC01              | Assam (Assam Traffic Department)                 |
| 27~CHVC01             | Chandigarh (VIRTUAL COURT CHANDIGARH)            |
| 18~CGVC01             | Chhattisgarh (Traffic Department)                |
| 26~DLVC02             | Delhi (Notice Department)                        |
| 26~DLVC01             | Delhi (Traffic Department)                       |
| 17~GJVC01             | Gujarat (Transport Department)                   |
| 17~GJVC02             | Gujarat (Traffic Department)                     |
| 14~HRVC01             | Haryana (Traffic Department)                     |
| 5~HPVC01              | Himachal Pradesh (Traffic Department)            |
| 12~JKVC02             | Jammu and Kashmir (Kashmir Traffic Department)   |
| 12~JKVC01             | Jammu and Kashmir (Jammu Traffic Department)     |
| 3~KAVC01              | Karnataka (Traffic Department)                   |
| 4~KLVC02              | Kerala (Police Department)                       |
| 4~KLVC01              | Kerala (Transport Department)                    |
| 23~MPVC01             | Madhya Pradesh (Traffic Department)              |
| 1~MHVC01              | Maharashtra (Pune Traffic Department)            |
| 1~MHVC03              | Maharashtra (Maharashtra Transport Department)   |
| 25~MNVC02             | Manipur (MANIPUR VIRTUAL COURT (TRANSPORT))      |
| 25~MNVC01             | Manipur (MANIPUR VIRTUAL COURT (TRAFFIC))        |
| 21~MLVC01             | Meghalaya (Meghalaya Traffic Department)         |
| 11~ODVC01             | Odisha (Odisha Traffic CTC-BBSR Commissionerate) |
| 9~RJVC01              | Rajasthan (Rajasthan Traffic Department)         |
| 10~TNVC01             | Tamil Nadu (Traffic Department)                  |
| 20~TRVC01             | Tripura (Traffic Department)                     |
| 15~UKVC02             | Uttarakhand (Transport Department)               |
| 15~UKVC01             | Uttarakhand (Traffic Department)                 |
| 13~UPVC01             | Uttar Pradesh (Traffic Department)               |
| 16~WBVC01             | West Bengal (Traffic Department)                 |


## Support
For Support Contact me at itzshubhamofficial@gmail.com
or Mobile Number : `+917687877772`

## Contribution

We welcome contributions to improve this project. Here are some ways you can contribute:

1. **Report Bugs:** If you find any bugs, please report them by opening an issue on GitHub.
2. **Feature Requests:** If you have ideas for new features, feel free to suggest them by opening an issue.
3. **Code Contributions:** 
    - Fork the repository.
    - Create a new branch (`git checkout -b feature-branch`).
    - Make your changes.
    - Commit your changes (`git commit -m 'Add some feature'`).
    - Push to the branch (`git push origin feature-branch`).
    - Open a pull request.

4. **Documentation:** Improve the documentation to help others understand and use the project.
5. **Testing:** Write tests to improve code coverage and ensure stability.

Please make sure your contributions adhere to our coding guidelines and standards.

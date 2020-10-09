import json, datetime, os, uuid
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

#This allows for requests to be made from "localhost"
CORS(app, resources = {
    r"/*": {
        "origins": "localhost"
    }
})

app.config["CORS HEADERS"] = "Content-Type"

#Data filename
jsonDataFileName = "BikesEdit.json"

# Flask route for front end to gather all id's and names to create dropdowns
@app.route('/')
@cross_origin()
def get_ids():
    with open('./BikesEdit.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
        tempArray = []
        for i in file_data:
            tempArray.append({"id":i,"name":file_data[i]["name"]})
    return jsonify(tempArray)

#For the front end to retreive data about specifc product/component
@app.route('/product/<id_>')
@cross_origin()
def stock_data_id(id_):
    # Additionally, we're now loading the JSON file's data into file_data 
    # every time a request is made to this endpoint
    with open('./BikesEdit.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    # We can then find the data for the requested date and send it back as json
    # return json.dumps(file_data[id])
    return jsonify(file_data[id_])

#Function for updating database
@app.route('/update/<id_>/<date_>/<new_stock>', methods=["POST"])
@cross_origin()
def updateData(id_,date_,new_stock):
    print(id_,date_,new_stock)
    receivedDate = datetime.datetime.strptime(date_, "%Y-%m-%d")
    formattedDate = receivedDate.strftime("%d/%m/%Y")
    with open(jsonDataFileName, 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
        record = file_data[id_]["stockRecord"]
        for row in record:
            if row["date"] == formattedDate:
                row["stock"] = new_stock
                break
        file_data[id_]["stockRecord"] = record
        #Code below here makes a new json datafile, 
        #adds the recently edited data,
        #and replaces the old file
        tempfile = os.path.join(os.path.dirname(jsonDataFileName), str(uuid.uuid4()))
        with open(tempfile, 'w') as f:
            json.dump(file_data, f, indent=4)
            os.replace(tempfile, jsonDataFileName)
    return(jsonify(success=True))



def upToDate():
    #This is just for adding new days of data to each product record,
    #So that it appears up to date.
    today = datetime.datetime.today()
    with open(jsonDataFileName, 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
        #For each component in the list
        for p_id in file_data:
            #Get the inventory info
            record = file_data[p_id]["stockRecord"]
            #Find what the latest date is
            lastDate = datetime.datetime.strptime(record[-1]["date"], "%d/%m/%Y")
            lastStock = record[-1]["stock"]
            #If it was before today...
            while (today - lastDate).days > 0 :
                #Add the next day..
                lastDate = lastDate + datetime.timedelta(days=1)
                newDateString = lastDate.strftime("%d/%m/%Y")
                #And give its inventory 3 more than the last day..
                newStock = str(int(lastStock)+3)
                lastStock = newStock
                record.append({"date":newDateString,"stock":newStock})
            file_data[p_id]["stockRecord"] = record
        tempfile = os.path.join(os.path.dirname(jsonDataFileName), str(uuid.uuid4()))
        with open(tempfile, 'w') as f:
            json.dump(file_data, f, indent=4)
            os.replace(tempfile, jsonDataFileName)

if __name__ == '__main__':
    upToDate()
    app.run(host='0.0.0.0', port=5000,debug=True)
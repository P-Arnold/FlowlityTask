import csv
import json

#CSV Header fieldnames
fieldnames = (
    "Date","ID","Name","Stock"
)

with open('./BikesEdit.csv', 'r') as csvfile:
    with open('./BikesEdit.json', 'w') as jsonfile:
        # Skip over headers
        next(csvfile)
        reader = csv.DictReader(csvfile, fieldnames)
        #Container for final data for JSON
        final_data = {}
        for row in reader:
            #If the current ID is not listed, create a space for it
            if not row["ID"] in final_data :
                final_data[row["ID"]] = {
                    #Give its name
                    "name": row["Name"],
                    #And an empty array for the inventory/date objects
                    "stockRecord": [],
                }
            final_data[row["ID"]]["stockRecord"].append({"date":row["Date"],"stock":row["Stock"]})
        json.dump(final_data, jsonfile)
        jsonfile.write('\n')

questionnaireID = "QQ000"
session = "ABCD"

results = [("P01", "P00TXT"), ("P00", "P01A1")]

data ={
            "questionnaireID" : questionnaireID,
            "session" : session,
            "answers": [
            ]
        }

""" for i in range(2):
    data["answers"].append({"qID" : results[i][0],"ans" : results[i][1]}) 
data["answers"] = sorted(data["answers"], key=lambda x: x["qID"])
 """

for result in range(len(results)):
    data["answers"].append({"qID" : results[result][0],"ans" : results[result][1]}) 
data["answers"] = sorted(data["answers"], key=lambda x: x["qID"])
print("\n")
print(data)
print("\n")

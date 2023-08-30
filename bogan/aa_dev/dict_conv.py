d1 = {"plays": {"@username": "Kreijeck", "play": [1, 2, 3, 4]}}
d2 = {"plays": {"@username": "Kreijeck", "play": [5, 6, 7]}}

li = [d1, d2]

combined = {}
for i in li:
  if combined == {}:
    combined = i
  else:
    i["@username"] = "Thomas"
    combined["plays"]["play"] +=i["plays"]["play"]

print(combined)

# if "play" in d1["plays"].keys():
#     print("it exists")

# if "plays" in d1.keys():
#     print("plays exist")

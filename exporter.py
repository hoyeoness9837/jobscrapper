import csv

def save_to_file(jobs):
  #mode=w writes it over everytime
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Location", "Link"])
  for job in jobs:
    #.values will get the values in dictionary{}
    #dict-value to list[] type
    writer.writerow(list(job.values()))
  return
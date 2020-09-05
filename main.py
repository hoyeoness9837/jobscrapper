from flask import Flask, render_template, request, redirect, send_file
from soscrapper import get_jobs as get_so_jobs
from indscrapper import get_jobs as get_indeed_jobs
from exporter import save_to_file

app = Flask("JobScrapper3")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        savedJobs = db.get(word)
        if savedJobs:
            jobs = savedJobs
        else:
            indeed_jobs = get_indeed_jobs(word)
            so_jobs = get_so_jobs(word)
            jobs = indeed_jobs + so_jobs
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv", mimetype='application/x-csv', attachment_filename='scrapped_jobs.csv', as_attachment=True)
    except:
        return redirect("/")


app.run(host="127.0.0.1", port=3000)

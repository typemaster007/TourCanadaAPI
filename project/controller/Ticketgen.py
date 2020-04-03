__author__ = "Amogh Adithya"

from flask import Flask, render_template, url_for, flash, redirect, send_file
import sys

# sys.path.insert(0, './project/model')
#from project.model.forms import  TicketForm
from project import app
from datetime import datetime as d

a = d.now()
#string = "2015-03-14  18:45:00.000"
dt_date = str(a.strftime("%d-%b-%Y"))
dt_time = str(a.strftime("%H:%M:%S"))
dt_mon = str(a.strftime("%b"))
dt_yr = str(a.strftime("%Y"))
dt_day = str(a.strftime("%d"))


@app.route("/ticketgen", methods=['GET', 'POST'])
def ticketgen():
    #form = TicketForm()
    
    return render_template('ticket.html', title='ticket', value = dt_mon, value2 = dt_yr, value3 = dt_day, val4 = dt_date, timeval = dt_time)

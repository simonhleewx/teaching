#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import numpy as np

server = ECMWFDataServer()

# The control forecast (cf; ensemble member 0) and the perturbed forecast (pf; members 1–10)
# are stored separately and need to be retrieved separately (with the argument 'type').

# Data natively stored as gribs but can be converted server side to netcdf with the "format" argument.

# Variables are coded (under 'param') -- full database: https://codes.ecmwf.int/grib/param-db/
# but note only a subset available on S2S database.

# Hindcasts are generated every Monday and Thursday.

# S2S native resolution is 1.5 degrees. 

# Most of this script can be generated on the ECMWF Public Datasets service and then
# customised here.

## VARIABLES ##
level_get = "10" # level in hPa
param_get = "131/156" # variables to download


## GET DATES ##
first_fcst =datetime(2024,11,11) # first forecast date to get
last_fcst = datetime(2025,3,31) # last forecast to get
ndays = (last_fcst-first_fcst).days # days between

datelist = [] # store string format dates of the realtime forecast
hdatelist = [] # store string format dates of the hindcasts

# loop through to get the dates
for d in np.arange(2,ndays+1,2):
    next_date = first_fcst+timedelta(days=int(d))
    for y in range(1,21):
        hdatelist.append((next_date-relativedelta(years=y)).strftime("%Y-%m-%d")) # hindcast dates, prev 20 y
        datelist.append(datetime.strftime(next_date,"%Y-%m-%d")) # corresponding real time


## LOOP TO DOWNLOAD

for i in range(len(hdatelist)):

    date_get = datelist[i] # realtime forecast date
    hdate_get = hdatelist[i] # hindcast date (can take range date_get-1, date_get-20)

    print("RT DATE:",date_get)
    print("HC DATE:",hdate_get)


    server.retrieve({
        "class": "s2",
        "dataset": "s2s",
        "date": date_get,
        "expver": "prod",
        "hdate": hdate_get,
        "levelist": level_get,
        "levtype": "pl",
        "model": "glob",
        "origin": "ecmf",
        "param": param_get,
        "step": "0/24/48/72/96/120/144/168/192/216/240/264/288/312/336/360/384/408/432/456/480/504/528/552/576/600/624/648/672/696/720/744/768/792/816/840/864/888/912/936/960/984/1008/1032/1056/1080/1104",
        "stream": "enfh",
        "time": "00:00:00",
        "type": "cf",
        "format": "netcdf",
        "area": [90, -180, 0, 180],
        "target": "ecmwf_uz10_nhem_"+str(hdate_get)+"_hc_cf.nc"
    })

    server.retrieve({
        "class": "s2",
        "dataset": "s2s",
        "date": date_get,
        "expver": "prod",
        "hdate": hdate_get,
        "levelist": level_get,
        "levtype": "pl",
        "model": "glob",
        "number": "1/2/3/4/5/6/7/8/9/10",
        "origin": "ecmf",
        "param": param_get,
        "step": "0/24/48/72/96/120/144/168/192/216/240/264/288/312/336/360/384/408/432/456/480/504/528/552/576/600/624/648/672/696/720/744/768/792/816/840/864/888/912/936/960/984/1008/1032/1056/1080/1104",
        "stream": "enfh",
        "time": "00:00:00",
        "type": "pf",
        "format": "netcdf",
        "area": [90, -180, 0, 180],
        "target": "ecmwf_uz10_nhem_"+str(hdate_get)+"_hc_pf.nc"
    })

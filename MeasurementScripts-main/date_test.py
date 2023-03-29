from datetime import datetime, timedelta     

matlab_datenum_base = datetime(1,1,1,0,0,0)
def datenum(d):
    return (now - matlab_datenum_base + timedelta(days=2)).total_seconds()/86400 + 365

now = datetime.now()
print(now)
dn = datenum(now)
print(dn)
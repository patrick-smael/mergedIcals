from flask import Flask, Response
import requests
from icalendar import Calendar, Event
from waitress import serve

app = Flask(__name__)

def get_ical_data(url):
    response = requests.get(url)
    ical_data = response.text
    return ical_data

def merge_ical_data(url1, url2, url3):
    cal1 = Calendar.from_ical(get_ical_data(url1))
    cal2 = Calendar.from_ical(get_ical_data(url2))
    cal3 = Calendar.from_ical(get_ical_data(url3))

    merged_cal = Calendar()
    merged_cal.add('prodid', '-//Calendar//calendar.smile-productions.nl//')
    merged_cal.add('version', '2.0')

    for cal in [cal1, cal2, cal3]:
        for event in cal.walk('VEVENT'):
            merged_cal.add_component(event)

    return merged_cal.to_ical()

@app.route('/mergedcalendars.ics')
def merged_cal():
    url1 = 'Calendar1'
    url2 = 'Calendar2'
    url3 = 'Calendar3'

    ical_data = merge_ical_data(url1, url2, url3)

    response = Response(ical_data, mimetype='text/calendar')
    response.headers.set('Content-Disposition', 'attachment', filename='merged_cal.ics')
    return response

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=porthere)

from . import main
from .. import db
from flask import render_template, url_for, redirect
from flask.ext.login import login_required, request
from ..models import Workday, BaseSchedule, Schedule
from datetime import time, date
# from .forms import Form


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')


@main.route('/base-schedule', methods=['GET', 'POST'])
@login_required
def base_schedule():
    data = request.get_json()

    if data:
        index = data['index']
        start = data['values'][0]
        lunch_start = data['values'][1]
        lunch_end = data['values'][2]
        end = data['values'][3]

    else:
        return render_template('main/base_schedule.html')

    return ''


@main.route('/summary')
@login_required
def summary():
    schedule = {
        'id': 5,
        'approved': False,
        'user_id': 10,
        'work_period_id': 2,
        'deviations': [{
            'id': 38,
            'schedule_id': 5,
            'date': date(year=2016, month=5, day=11),
            'start': time(hour=8, minute=30),
            'lunch_start': time(hour=11),
            'lunch_end': time(hour=12),
            'end': time(hour=16, minute=25)
        }],
        'base_schedule': {
            'id': 1,
            'schedule_id': 5,
            'workdays': [{
                'id': 7,
                'index': 0,
                'start': time(hour=8),
                'lunch_start': time(hour=11, minute=30),
                'lunch_end': time(hour=12, minute=30),
                'end': time(hour=16)
            }, {
                'id': 8,
                'index': 1,
                'start': time(hour=7),
                'lunch_start': time(hour=11),
                'lunch_end': time(hour=12),
                'end': time(hour=15)
            }, {
                'id': 9,
                'index': 2,
                'start': time(hour=10),
                'lunch_start': time(hour=11, minute=30),
                'lunch_end': time(hour=12, minute=30),
                'end': time(hour=17)
            }, {
                'id': 10,
                'index': 3,
                'start': time(hour=9),
                'lunch_start': time(hour=11, minute=30),
                'lunch_end': time(hour=12, minute=30),
                'end': time(hour=16, minute=30)
            }, {
                'id': 11,
                'index': 4,
                'start': time(hour=6, minute=50),
                'lunch_start': time(hour=11),
                'lunch_end': time(hour=12),
                'end': time(hour=14, minute=30)
            }]
        }
    }

    def calculate_day_positions(day):
        """Calculate css-percentages for a given day to position it in view.

        Used to position different times relative to the length of a workday
        NOTE: Hardcoded. A future improvement could be to use global config-variables 
        to calculate workday_start and workday_end
        """
        workday_start = 360
        workday_end = 1080
        minutes_per_percent = (workday_end - workday_start) / 100

        def calculate_percent(time):
            """Calculate percentage for a given time in a workday."""
            return ((day[time].hour * 60 + day[time].minute) - workday_start) / minutes_per_percent

        return {
            'start': calculate_percent('start'),
            'lunch_start': calculate_percent('lunch_start'),
            'lunch_end': calculate_percent('lunch_end'),
            'end': calculate_percent('end')
        }

    schedule_positions = []

    for day in schedule['base_schedule']['workdays']:
        day_names = ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lördag', 'Söndag']
        new_day = calculate_day_positions(day)
        new_day['name'] = day_names[day['index']]
        schedule_positions.append(new_day)

    deviation_positions = []

    for day in schedule['deviations']:
        new_day = calculate_day_positions(day)
        new_day['date'] = day['date']
        deviation_positions.append(new_day)

    print(schedule_positions, deviation_positions)

    return render_template('main/summary.html',
                            schedule_positions=schedule_positions,
                            deviation_positions=deviation_positions,
                            schedule=schedule)

    # 2. create a template to present and allow user to edit fake data
    # 3. On update to fake data, send POST-request back to this route. (jquery post)
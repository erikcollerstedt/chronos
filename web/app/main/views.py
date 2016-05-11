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


@main.route('/summary', methods=['GET', 'POST'])
@login_required
def summary():
    data = request.get_json()

    if data:
        print(data)

    else:
        # 1. create fake schedule
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
                    'index': 0,
                    'start': time(hour=7),
                    'lunch_start': time(hour=11),
                    'lunch_end': time(hour=12),
                    'end': time(hour=15)
                }, {
                    'id': 9,
                    'index': 0,
                    'start': time(hour=10),
                    'lunch_start': time(hour=11, minute=30),
                    'lunch_end': time(hour=12, minute=30),
                    'end': time(hour=17)
                }, {
                    'id': 10,
                    'index': 0,
                    'start': time(hour=9),
                    'lunch_start': time(hour=11, minute=30),
                    'lunch_end': time(hour=12, minute=30),
                    'end': time(hour=16, minute=30)
                }, {
                    'id': 11,
                    'index': 0,
                    'start': time(hour=6, minute=50),
                    'lunch_start': time(hour=11),
                    'lunch_end': time(hour=12),
                    'end': time(hour=14, minute=30)
                }]
            }
        }

        return render_template('main/summary.html', schedule=schedule)

    return ''

    # 2. create a template to present and allow user to edit fake data
    # 3. On update to fake data, send POST-request back to this route. (jquery post)
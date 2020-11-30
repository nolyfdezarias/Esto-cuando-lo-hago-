from typing import List, Dict
from pprint import pprint
from datetime import date, timedelta
import re, json


class ActivitiesOrgParser:
    def __init__(self, filename: str):
        with open(filename, 'r') as fd:
            lines = fd.readlines()
        self.lines: List[str] = lines
        self._clean_lines()
        self.dict_dates = {}

    def parse(self):
        "Parses the file to a list of activities"
        self._parse_json(self._parse())
        return self.dict_dates
    
    def save_to_json(self, filename):
        "Saves the last parsed activities to a json"
        pprint(self.dict_dates)
        for week, dates in self.dict_dates.items():
            with open(f'{filename}/{week}.json', 'w+') as fp:
                json.dump(dates, fp)
            

    def _parse(self):
        activities = self._process_activities()
        timestamp = r'<(?P<date>\d{4}-\d\d-\d\d) \w{3}.?( (?P<time>\d\d:\d\d)(-(?P<end_time>\d\d:\d\d))?)?.*>'
        time_interval = timestamp.replace(r'.*', r'.*\+(?P<n>\d+)(?P<type>[dwmy])')
        self.regex = {
            'date': re.compile(timestamp),
            'time_interval': re.compile(time_interval)
        }
        return activities

    def _process_activities(self):
        "Process activities to leave them in a format: activity_name, activity_dates"
        activities = self._split_activities()
        return list(filter(lambda act: len(act[1]) > 0, activities))    # Keep only those with at least one date

    def _clean_lines(self):
        "Return lines stripped and potential activities and dates only"
        new_lines = []
        first_activity = False
        for line in self.lines:
            line = line.strip()
            if first_activity and line.startswith('<') or line.startswith('*'):
                first_activity = True
                new_lines.append(line)
        self.lines = new_lines

    def _split_activities(self):
        "Given the list of lines returns an activity list with the activities names and dates"
        activities: List[List[str]] = []                # Saves a list with a tuple name and dates
        for i in range(len(self.lines)):
            line = self.lines[i]
            if line.startswith('<'):
                last_activity = activities[-1]
                last_activity[1].append(line)
            elif line.startswith('*'):
                activities.append([line, []])
        return activities
        
    def _parse_json(self, activities):
        for act_name, act_dates in activities:
            act_name = act_name.strip(' *')
            json_dates = self._get_json_dates(act_dates)
            for d in json_dates.values():
                for day in d:
                    day.update({'name': act_name})
            self._update_dates(json_dates)

    def _update_dates(self, dates: dict):
        for week, days in dates.items():
            for day in days:
                self._update_dict(self.dict_dates, week, day)

    def _get_json_dates(self, act_dates):
        json_dates = {}
        for act_date in act_dates:
            if '--' in act_date:
                d1, d2 = act_date.split('--')
                d1 = self.regex['date'].search(d1).groupdict()
                d2 = self.regex['date'].search(d2).groupdict()
                try:
                    json_dates.update(self._get_all_dates(d1, d2))
                except ValueError:
                    continue
            else:
                d = self.regex['date'].search(act_date)
                if d is not None:
                    d_ti = self.regex['time_interval'].search(act_date)
                    if d_ti is not None:
                        d = d_ti
                    day = date.fromisoformat(d['date'])
                    week = self._get_week(day)
                    self._update_dict(json_dates, week, d.groupdict())
        return json_dates

    @staticmethod
    def _get_week(day: date):
        "Gets the week number of a date (the year is also codified"
        year, week, _ = day.isocalendar()
        return f'{year}-{week}'

    @staticmethod
    def _update_dict(dictionary: dict, key, value):
        "Gets the week number of a date (the year is also codified"
        try:
            dictionary[key].append(value)
        except KeyError:
            dictionary[key] = [value]

    @staticmethod
    def _get_all_dates(d1, d2):
        "Gets all the dates from d1 to d2"
        start_date = date.fromisoformat(d1['date'])
        end_date = date.fromisoformat(d2['date'])
        delta = timedelta(days=1)
        dates = {}

        current_date = start_date
        while current_date <= end_date:
            week = ActivitiesOrgParser._get_week(current_date)
            d = dict(d1)
            d.update({'date': str(current_date)})
            ActivitiesOrgParser._update_dict(dates, week, d)
            current_date += delta

        return dates


if __name__ == '__main__':
    parser = ActivitiesOrgParser('activities.org')
    activitdies = parser.parse()
    parser.save_to_json('jsons')

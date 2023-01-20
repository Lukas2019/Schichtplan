import random
from tabulate import tabulate
from datetime import datetime, timedelta


class ShiftPlan:
    def __init__(self, start_date, end_date, num_shifts_per_day, people):
        self.start_date = start_date
        self.end_date = end_date
        self.num_shifts_per_day = num_shifts_per_day
        self.people = people

    def create_schedule(self):
        """Erstellt den Schichtplan als Dictionary.

        Returns:
          schedule: Schichtplan (Dictionary)
        """
        # Zähler für eindeutige Identifikatoren
        counter = {name: 1 for name in self.people}

        # Schichtplan erstellen
        schedule = {}
        current_date = self.start_date
        while current_date <= self.end_date:
            shifts = ["" for _ in range(self.num_shifts_per_day)]
            for i, name in enumerate(self.people):
                shifts[i % self.num_shifts_per_day] = "/{}_{}".format(name,
                                                                      counter[
                                                                          name])
                counter[name] += 1
            schedule[current_date] = shifts
            current_date += timedelta(days=1)

        return schedule

    def render_schedule_table(self):
        """Rendert den Schichtplan als Markdown-Tabelle mit eindeutigen Identifikatoren.

        Returns:
          markdown_table: Markdown-Tabelle (String)
        """
        # Spaltenüberschriften der Tabelle
        columns = ["Datum"] + ["Schicht {}".format(i + 1) for i in
                               range(self.num_shifts_per_day)]

        # Inhalt der Tabelle
        rows = []
        for date, shifts in self.current_schedule.items():
            rows.append([date] + shifts)

        # Markdown-Tabelle erstellen
        markdown_table = tabulate(rows, headers=columns, tablefmt="pipe")

        return markdown_table

    def render_schedule(self):
        """Rendert den Schichtplan als Markdown-Liste.

        Returns:
          markdown_list: Markdown-Liste (String)
        """
        # Inhalt der Liste
        items = []
        for date, shifts in self.current_schedule.items():
            items.append(date)
            for shift in shifts:
                items.append("- {}".format(shift))

        # Markdown-Liste erstellen
        markdown_list = "\n".join(items)

        return markdown_list

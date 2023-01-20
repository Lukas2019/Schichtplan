import random
from prettytable import PrettyTable
from datetime import datetime, timedelta


def main():
    # Liste der Personen, die in den Schichten arbeiten sollen
    people = ["Lukas", "Jan", "Elias"]

    # Anzahl der Schichten pro Tag
    num_shifts_per_day = 3

    # Startdatum für den Schichtplan (im Format "YYYY-MM-DD")
    start_date = "2023-03-21"

    # Anzahl der Tage, die nach dem Startdatum generiert werden sollen
    delta_days = 5

    # Initialises the shiftplan
    shiftplan = ShiftPlan(start_date, delta_days, num_shifts_per_day, people)

    # Schichtplan erstellen
    schedule = shiftplan.create_schedule()

    # Schichtplan ausgeben
    for date, shifts in schedule.items():
        print(f"{date}: {shifts}")

    # Schichtplan rendern und ausgeben
    print(shiftplan.render_schedule(schedule))

    identifier = "/Lukas_3"
    name, counter = shiftplan.prase_identifier(identifier)
    print(name)  # Ausgabe: "Lukas"
    print(counter)  # Ausgabe: 3
    key, pos = shiftplan.get_key_and_pos(schedule, name, counter)
    print(key, pos)

    comand = "/Lukas_1 Übernehmen"
    shiftplan.user_input(comand, 'Jan')
    comand = "/Jan_2 Kann nicht"

    shiftplan.set_date_format("german")

    print(shiftplan.white_dict)
    print(shiftplan.black_dict)


class ShiftPlan:
    DATE_FORMATS_CAUSES = {
        "iso": "%Y-%m-%d",
        "german": "%d.%m.%Y",
        "us": "%m/%d/%Y"
    }
    def __init__(self, start_date, delta_days, num_shifts_per_day, people):
        self.start_date = start_date
        self.delta_days = delta_days
        self.num_shifts_per_day = num_shifts_per_day
        self.people = people
        self.current_schedule = self.create_schedule()
        scheule_with_listes = self.creat_scheule_with_listes
        self.black_dict = scheule_with_listes
        self.white_dict = scheule_with_listes

    def create_schedule(self):
        """Erstellt einen Schichtplan für den angegebenen Zeitraum, wobei jeder Tag
        die angegebene Anzahl an Schichten hat und die Schichten zufällig unter den angegebenen
        Personen aufgeteilt werden.

        Args:
          people: Liste der Personen, die in den Schichten arbeiten sollen
          num_shifts_per_day: Anzahl der Schichten pro Tag
          start_date: Startdatum für den Schichtplan (im Format "YYYY-MM-DD")
          delta_days: Anzahl der Tage, die nach dem Startdatum generiert werden sollen

        Returns:
          schedule: Schichtplan-Dictionary, in dem der Schichtplan gespeichert ist (Struktur siehe Beispiel)
        """
        # Schichtplan-Dictionary, in dem der Schichtplan gespeichert wird
        schedule = {}

        # Startdatum wird in ein datetime-Objekt umgewandelt
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")

        # Der Schichtplan wird für jeden Tag im angegebenen Zeitraum erstellt
        current_date = start_date
        for i in range(self.delta_days):
            date_str = current_date.strftime("%Y-%m-%d")
            schedule[current_date.strftime("%Y-%m-%d")] = random.choices(
                self.people,
                k=self.num_shifts_per_day)
            current_date += timedelta(days=1)
        self.current_schedule = schedule
        return schedule

    def set_date_format(self, format_cause):
        """Setzt das Datumsformat für den Schichtplan.

        Args:
          format_cause: Formatierungsgrund (String)

        Returns:
          None
        """
        if format_cause in self.DATE_FORMATS_CAUSES:
            self.date_format = self.DATE_FORMATS_CAUSES[format_cause]
        else:
            try:
                self.date_format = format_cause
                print(datetime.strptime("2020-01-01", self.date_format))
            except ValueError:
                raise ValueError("Ungültiges Datumsformat")

    @property
    def creat_scheule_with_listes(self):
        """Erstellt einen Schichtplan , der mit listen gfüllt ist, sodass
        er für den black and white-dicht verwendet werden kann.

        Args:
          people: Liste der Personen, die in den Schichten arbeiten sollen
          num_shifts_per_day: Anzahl der Schichten pro Tag
          start_date: Startdatum für den Schichtplan (im Format "YYYY-MM-DD")
          delta_days: Anzahl der Tage, die nach dem Startdatum generiert werden sollen

        Returns:
          schedule_with_listes: Schichtplan-Dictionary, in dem der Schichtplan gespeichert ist (Struktur siehe Beispiel)
        """
        # Schichtplan-Dictionary, in dem der Schichtplan gespeichert wird
        schedule_with_listes = {}

        # Startdatum wird in ein datetime-Objekt umgewandelt
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")

        # Der Schichtplan wird für jeden Tag im angegebenen Zeitraum erstellt
        current_date = start_date
        for i in range(self.delta_days):
            schedule_with_listes[current_date.strftime("%Y-%m-%d")] = [[] for _
                                                                       in range(
                    self.num_shifts_per_day)]
            current_date += timedelta(days=1)
        self.current_schedule = schedule_with_listes
        return schedule_with_listes

    def rm_from_schedule(self, key, pos, name):
        self.black_dict[key][pos].append(name)
        if name in self.white_dict[key][pos]:
            self.white_dict[key][pos].remove(name)
        person = [item for item in self.people if
                  item not in self.black_dict[key][pos]]
        if len(person) == 0:
            raise Exception("No one wants this shift.")


    def replace_schedule(self, key, pos, name):
        if name in self.black_dict[key][pos]:
            self.black_dict[key][pos].remove(name)
        white_list = self.white_dict[key][pos]
        if len(white_list) > 1:
            # todo: add question where or not user wants to be added
            # self.white_dict[key][pos].append(name)
            raise Exception(
                f"{white_list[0]} already whants to thake this shift")
        else:
            self.current_schedule[key][pos] = name
        self.white_dict[key][pos].append(name)
        if not name in self.people:
            self.people.append(name)

    def render_schedule(self, schedule=None):
        """Rendert einen Schichtplan als Markdown-Tabelle mit eindeutigen Identifikatoren.

        Args:
          schedule: Schichtplan (Dictionary)

        Returns:
          markdown_table: Markdown-Tabelle (String)
        """
        if not schedule:
            schedule = self.current_schedule

        # Zähler für eindeutige Identifikatoren
        counter = {name: 1 for name in self.people}

        # Spaltenüberschriften der Tabelle
        columns = ["Datum"] + ["Schicht {}".format(i + 1) for i in
                               range(self.num_shifts_per_day)]
        table = PrettyTable(columns)

        # Inhalt der Tabelle
        for date, shifts in schedule.items():
            row = [date] + ["/{}_{}".format(name, counter[name]) for name in
                            shifts]
            table.add_row(row)

            # Zähler für jeden Namen erhöhen
            for name in shifts:
                counter[name] += 1

        # Markdown-Tabelle erstellen
        markdown_table = table.get_string()

        return markdown_table

    def prase_identifier(self, identifier):
        """Zerlegt einen Identifikator in den Personennamen und den Zählerwert.

        Args:
          identifier: Identifikator (String)

        Returns:
          name: Personenname (String)
          counter: Zählerwert (Integer)
        """
        # Namen und Zählerwert aus Identifikator extrahieren
        name, counter = identifier[1:].split("_")
        counter = int(counter)

        return name, counter

    def execute_command(self, identifier, command, usr):
        """Führt einen Befehl für den angegebenen Identifier aus.

        Args:
          identifier: Identifier (String)
          command: Befehl (String)
        """
        name, counter = self.prase_identifier(identifier)
        key, pos = self.get_key_and_pos(self.current_schedule, name, counter)

        if command == "kannnicht":
            self.rm_from_schedule(key, pos, name)

        elif command == "übernehmen":
            self.replace_schedule(key, pos, name)

    def parse_input(self, input_str: str):
        """Analysiert die Eingabe und extrahiert Befehl und Identifikator.

        Args:
          input_str: Eingabe (String)

        Returns:
          command: Befehl (String)
          identifier: Identifikator (String)
        """
        # Eingabe in Worte splitten
        words = input_str.split()

        # Befehl ist das letzte Wort
        command = words[-1]

        # Identifikator ist alles bis auf das letzte Wort
        identifier = " ".join(words[:-1])

        return command, identifier

    def user_input(self, msg: str, usr):
        command, identifier = self.parse_input(msg)
        command = command.lower().replace(" ", "")
        self.execute_command(identifier, command, usr)
        # self.update_schedule
        self.render_schedule()


    def get_key_and_pos(self, schedule, name, num):
        """Gibt den Schlüssel und die Position des Schlüssels im Schichtplan zurück.
        Args:
          schedule: Schichtplan (Dictionary)
          name: Name der Person (String)
          num: Nummer des Schichts (Integer)

        Returns:
          key: Schlüssel des Schichtplans (String)
          pos: Position im Schichtplan (Integer)
        """
        # creat counter for name
        couter = {name: 0 for name in self.people}

        for key, shifts in schedule.items():
            for pos, shift in enumerate(shifts):
                couter[name] += 1
                if shift == name and couter[name] == num:
                    return key, pos
        return None, None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

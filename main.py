import random
from prettytable import PrettyTable
from datetime import datetime, timedelta


def main():
    # Liste der Personen, die in den Schichten arbeiten sollen
    people = ["Lukas", "Jan", "Elias"]

    # Anzahl der Schichten pro Tag
    num_shifts_per_day = 5

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
    print(shiftplan.render_list(schedule))

    identifier = "/Lukas_3"
    name, counter = shiftplan.prase_identifier(identifier)
    print(name)  # Ausgabe: "Lukas"
    print(counter)  # Ausgabe: 3
    key, pos = shiftplan.get_key_and_pos(schedule, name, counter)
    print(key, pos)

    # comand = "/Lukas_1 Übernehmen"
    # shiftplan.user_input(comand, 'Jan')
    # comand = "/Jan_2 Kann nicht"
    # shiftplan.user_input(comand, 'Jan')
    shiftplan.user_input("/Lukas_3_kann", 'Lukas')

    # print(shiftplan.white_dict)
    # print(shiftplan.black_dict)
    print(shiftplan.render_schedule(schedule))


class ShiftPlan:
    DATE_FORMATS_CAUSES = {
        "iso": "%Y-%m-%d",
        "german": "%d.%m.%Y",
        "us": "%m/%d/%Y"
    }

    def __init__(self, start_date, delta_days, num_shifts_per_day, people,
                 date_format="iso"):
        self.changed_schift = []
        self.start_date = start_date
        self.delta_days = delta_days
        self.num_shifts_per_day = num_shifts_per_day
        self.people = people
        self.set_date_format(date_format, start_date)
        self.current_schedule = self.create_schedule()
        scheule_with_listes = self.creat_placeholder_scheule_with_listes
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
            schedule[current_date.strftime(self.date_format)] = random.choices(
                self.people,
                k=self.num_shifts_per_day)
            current_date += timedelta(days=1)
        self.current_schedule = schedule
        return schedule

    def set_date_format(self, format_cause, start_date):
        """Setzt das Datumsformat für den Schichtplan.

        Args:
          format_cause: Formatierungsgrund (String)

        Returns:
          None
        """
        if format_cause in self.DATE_FORMATS_CAUSES:
            date_format = self.DATE_FORMATS_CAUSES[format_cause]
        else:
            try:
                date_format = format_cause
                datetime.strptime("2020-01-01", self.date_format)
            except ValueError:
                raise ValueError("Ungültiges Datumsformat")
        try:
            datetime.strptime(start_date, date_format)
        except ValueError:
            raise ValueError("Das Startdatum entspricht nicht dem "
                             "angegebenen Datumsformat({})".format(
                date_format))
        else:
            self.date_format = date_format

    @property
    def creat_placeholder_scheule_with_listes(self):
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
        start_date = datetime.strptime(self.start_date, self.date_format)

        # Der Schichtplan wird für jeden Tag im angegebenen Zeitraum erstellt
        current_date = start_date
        for i in range(self.delta_days):
            schedule_with_listes[current_date.strftime(self.date_format)] = [[]
                                                                             for
                                                                             _
                                                                             in
                                                                             range(
                                                                                 self.num_shifts_per_day)]
            current_date += timedelta(days=1)
        self.current_schedule = schedule_with_listes
        return schedule_with_listes

    def remove_from_schedule(self, key, pos, name):
        self.black_dict[key][pos].append(name)
        if name in self.white_dict[key][pos]:
            self.white_dict[key][pos].remove(name)
        person = [item for item in self.people if
                  item not in self.black_dict[key][pos]]
        if len(person) == 0:
            raise Exception("No one wants this shift.")
        self.current_schedule[key][pos] = random.choice(person)
        self.changed_schift = [key, pos, person]

    def replace_in_schedule(self, key, pos, name):
        '''
        Ersetzt name in der Liste an der Stelle pos im Dictionary an der
        Stelle key, sodass der Name nicht mehr in der Liste ist und nicht
        mehr gesetzt werden kann.
        :param key:
        :param pos:
        :param name:
        :return:
        '''
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

    def generate_identfier(self, schedule=None):
        """Erstellt einen eindeutigen Identifikator für jedes einzelne
        Element
        Args:
            schedule_cp: Schichtplan-Dictionary, in dem der Schichtplan gespeichert ist (Struktur siehe Beispiel)
        :return: dictionary mit den identifikatoren
        """

        if schedule == None:
            schedule = self.current_schedule
        schedule_cp = \
            {date: shifts.copy() for date, shifts in
             schedule.items()}

        counter = {name: 0 for name in self.people}

        for key, value in schedule_cp.items():
            date = datetime.strptime(key, self.date_format).strftime(
                self.date_format)
            for i, name in enumerate(value):
                schedule_cp[date][i] = f"/{name}_{counter[name]}"
                counter[name] += 1
        return schedule_cp

    def render_schedule(self, schedule=None, list=False):
        """Rendert einen Schichtplan als Markdown-Tabelle mit eindeutigen Identifikatoren.

        Args:
          schedule: Schichtplan (Dictionary)

        Returns:
          markdown_table: Markdown-Tabelle (String)
        """
        if not schedule:
            schedule = self.current_schedule
        idetifier_schedule = self.generate_identfier(schedule)

        # Spaltenüberschriften der Tabelle
        columns = ["Datum"] + ["Schicht {}".format(i + 1) for i in
                               range(self.num_shifts_per_day)]
        table = PrettyTable(columns)

        # Inhalt der Tabelle
        for date, shifts in idetifier_schedule.items():
            row = [date] + shifts
            table.add_row(row)

        # Markdown-Tabelle erstellen
        markdown_table = table.get_string()
        msg = self.creat_change_msg(idetifier_schedule)
        return markdown_table + msg

    def render_list(self, schedule=None):
        """Rendert einen Schichtplan als Markdown-Liste mit eindeutigen Identifikatoren.
        :args:
            schedule: Schichtplan (Dictionary)
        :return:
            markdown_list: Markdown-Liste (String)
        """
        if not schedule:
            schedule = self.current_schedule
        idetifier_schedule = self.generate_identfier(schedule)
        markdown_list = ""
        for date, shifts in idetifier_schedule.items():
            markdown_list += f"\n* {date}"
            for idetifier in shifts:
                markdown_list += f"\n\t* {idetifier}"
        return markdown_list

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

    def execute_command(self, msg, usr):
        """Führt einen Befehl für den angegebenen Identifier aus.

        Args:
          identifier: Identifier (String)
          command: Befehl (String)
        """
        name, counter, command = self.parse_input(msg)
        key, pos = self.get_key_and_pos(self.current_schedule, name, counter)

        if command == "kn":
            self.remove_from_schedule(key, pos, name)


        elif command == "ue":
            self.replace_in_schedule(key, pos, usr)

    def parse_input(self, input_str: str, ):
        """Analysiert die Eingabe und extrahiert Befehl und Identifikator.

        Args:
          input_str: Eingabe (String)

        Returns:
          command: Befehl (String)
          identifier: Identifikator (String)
        """

        # Prüfen, ob es mehr als einen "_" gibt
        if input_str.count("_") > 1:
            words = input_str.split('_')
            command = "".join(input_str.split("_")[2:])
            # Identifikator ist alles bis auf das letzte Wort
            name = words[0][1:]
            counter = int(words[1])
        else:
            # Eingabe in Worte splitten
            words = input_str.split()
            # Befehl ist das letzte Wort
            command = "".join(words[1:])
            # Identifikator ist alles bis auf das letzte Wort
            identifier = words[0]
            # Namen und Zählerwert aus Identifikator extrahieren
            name, counter = identifier[1:].split("_")
            counter = int(counter)

        command = command.lower().replace(" ", "")

        if command == "kannnicht" or command == "kann":
            command = "kn"
        elif command == "übernehmen":
            command = "ue"

        return name, counter, command,

    def user_input(self, msg: str, usr):
        self.execute_command(msg, usr)
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
        couter = 0

        for key, shifts in schedule.items():
            for pos, shift in enumerate(shifts):
                if shift == name:
                    couter += 1
                    if couter == num:
                        return key, pos
        return None, None

    def creat_change_msg(self, idetifier_schedule):
        """Erstellt eine Nachricht mit den Änderungen im Schichtplan."""
        # Änderungen im Schichtplan
        change_msg = ""
        if self.changed_schift:
            key, pos, person = self.changed_schift
            idetifier_new = idetifier_schedule[key][pos]
            person_free = " ".join([f"@{name}" for name in person])
            change_msg = f"\n\n{idetifier_new} wurde neu erstell bitte " \
                         f"prüfe od " \
                         f"du die Schicht übernehmen möchtest. {person_free} \n Vielen Dank"
            return change_msg
        return ""


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

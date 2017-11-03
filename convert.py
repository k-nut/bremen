import csv
import json
import os


BASE_PATH = "/Users/knut/Downloads"


def save_as_json(data, name):
    with open(os.path.join(BASE_PATH, "bremen-{}.json".format(name)), "w") as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)


def jsonify_csv(name):
    collected = {}
    had_dash = False
    current_number = 0
    with open(os.path.join(BASE_PATH, "tabula-Bremen-{}.csv".format(name))) as infile:
        reader = csv.reader(infile)
        for line in reader:
            if line[0] != "":
                current_number = line[0]
                title = line[1]
                if title.endswith("-"):
                    had_dash = True
                    title = title[:-1]
                else:
                    had_dash = False
                collected[current_number] = title
                continue

            if had_dash:
                collected[current_number] += line[1]
            else:
                collected[current_number] += " " + line[1]
    save_as_json(collected, name)


def get_json(name):
    with open(os.path.join(BASE_PATH, "bremen-{}.json".format(name))) as infile:
        return json.load(infile)


def save_data(data):
    with open(os.path.join(BASE_PATH, "haushalt-bremen-enriched.csv"), "w", newline="\n") as outfile:
        headers = data[0].keys()
        writer = csv.DictWriter(outfile, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def enrich_haushalt():
    with open(os.path.join(BASE_PATH, "Haushaltsdaten_2016-2017.csv")) as infile:
        reader = [row for row in csv.DictReader(infile)]
        groups = get_json("gruppen")
        functions = get_json("funktionen")
        for line in reader:
            gruppe = line['Hst.'][5:8]
            funktion = line['FKZ']
            line["Gruppe 3"] = groups.get(gruppe, "N/A")
            line["Gruppe 2"] = groups[gruppe[:2] + "*"]
            line["Gruppe 1"] = groups[gruppe[:1] + "**"]
            line["Funktion 3"] = functions.get(funktion, "N/A")
            line["Funktion 2"] = functions[funktion[:2] + "*"]
            line["Funktion 1"] = functions[funktion[:1] + "**"]
        save_data(reader)


def main():
    jsonify_csv("gruppen")
    jsonify_csv("funktionen")
    enrich_haushalt()


if __name__ == '__main__':
    main()

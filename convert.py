import json
import os

formeln = json.load(open("formeln.json"))
legend = json.load(open("legend.json"))

def get_filename(unformatted):
    unformatted = unformatted.replace(" ", "-")
    unformatted = unformatted.replace("ü", "ue")
    unformatted = unformatted.replace("ä", "ae")
    unformatted = unformatted.replace("ö", "oe")
    unformatted = unformatted.replace("ß", "sz")
    return unformatted

def isNumb(s):
    s = s.replace(",", ".")
    try:
        float(s)
        return True
    except ValueError:
        return False;

def niceParam(param):
    if param == "}": param = ""
    if param == "{": param = ""
    # Remove close } if no open { before
    while param.count("{") < param.count("}"):
        if param[-1] == "}":
            param = param[:-1]
    while param.count("(") < param.count(")"):
        if param[-1] == ")":
            param = param[:-1]
    # Remove potence
    if "^" in param:
        param = param.split("^")[0]
    # Remove numbers from the Legend
    if isNumb(param): return ""
    # Inserte space after \\Delta
    if "Delta" in param:
        param = param.replace("Delta", "Delta ")
    return param;

def stripOperator(formel):
    formel = formel.replace("$", "")
    formel = formel.replace(" ", "")
    formel = formel.replace("=", " ")
    formel = formel.replace("\\cdot"," ")
    formel = formel.replace("\\sqrt{", " ")
    formel = formel.replace("\\frac{", " ")
    formel = formel.replace("\\cfrac{", " ")
    formel = formel.replace("\\ln{", " ")
    formel = formel.replace("}{", " ")
    formel = formel.replace("+", " ")
    formel = formel.replace("-", " ")
    return formel;

def extractParam(formel):
    formel = stripOperator(formel)
    #formel = re.sub(r'( [a-zA-Z0-9])+}', r'\1', formel)

    data = list(filter(None, formel.split(' ')))

    param = []

    for parametre in data:
        parametre = niceParam(parametre)

        if parametre == "":
            continue

        param.append(parametre)

    return param;

def createLegend(formel):
    for param in extractParam(formel):
        if param not in legend:
            legend[param] = {'Display': 1, 'Description': "", 'unit': "", 'value': ""};

def getLegend(formel):
    output = ""
    for param in extractParam(formel):
        print(param + ": " + str(legend[param]["Display"]))
        if param not in legend: continue
        if not legend[param]["Display"]: continue

        output += "$" + param + " $ & " + legend[param]["Description"] + " & $" + legend[param]['unit'] + " $ & $ " + legend[param]['value'] + "$ \\\\ \n";

    return output;

for formel in formeln:
    title = formel["title"]
    subtitle = formel["subtitle"]
    subsubtitle = formel["subsubtitle"]
    main_formular = formel["formeln"][0]
    formular = formel["formeln"]

    createLegend(main_formular)

    file_path = get_filename(title) + '/' + get_filename(subtitle) + '.tex'
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    if 'Aufgabe:' in subsubtitle:
        continue

    with open(file_path, 'a') as f:
        f.write("\\subsubsection{" + subsubtitle + "} \n")
        f.write("\\begin{minipage}{0.45\\textwidth} \n")
        f.write("\\mainformular{" + main_formular + "} \n")
        f.write('\\end{minipage} \n')
        f.write('\\begin{minipage}{0.45\\textwidth} \n \n')
        f.write('\\legende{ \n'+ str(getLegend(main_formular)) + '} \n')
        f.write('\\end{minipage} \n')
        for formel in formular:
            f.write(formel.strip() + ' \\textcolor{lightgray}{\\textbf{---}} ')
            f.write('\n')
        f.write('\n')
        f.close()

jsonarray = json.dumps(legend, indent=4, sort_keys=True)

with open('legend.json', 'w') as f:
    f.write(jsonarray)
    f.close()

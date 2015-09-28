import re
import codecs
import operator

from datetime import datetime


#Guido Zuidhof
#s4160703
# Text Mining, exercise 4

#From exercise 2, splits the input sentence-wise
def process_text(filename="inputnelson.txt"):

    in_file = open(filename,'r')
    full_text = in_file.read()
    in_file.close()

    #Recognize multiple empty lines, used for page numbers and footnotes
    #Place a flag there, to be added again later
    paged = re.sub(r'\n\n',r'_NEWLINE_', full_text)

    #Hyphens at the end of sentences get removed, joining the two parts
    unhyphened = paged.replace('-\n',"")

    #newlines get removed where the next character is not a capital
    collapsed = re.sub(r'\n([^A-Z])',r"\1", unhyphened)

    #Place newlines where < NOT capital, dot, a character, a capital,
    #NOT (OPTIONAL whitespace, a dot) > pattern is present
    rebuilt = re.sub(r'([^A-Z])[.][ ]([A-Z])([^?\s.])', r'\1.\n\2\3', collapsed)

    #Re-add the multiple empty lines
    rebuilt = rebuilt.replace("_NEWLINE_","\n\n")

    return rebuilt

def extract_events(text):
    sentences = text.split("\n")

    #Timeline events
    events = []
    last_year = "0000"

    for sentence in sentences:

        year = re.search(r'\d{4}', sentence)
        month = re.search(r'((Jan|Feb|Mar[^y]|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)', sentence)

        day = re.search(r'[^\d{2}]((\d?\d))[^\d{2}]', sentence) if month else None

        year = year.group(0) if year else None
        month = month.group(0) if month else None
        day = day.group(0) if day and month else None

        if day: #Select only relevant part
            day = re.search(r'(\d?\d)', day).group(0)
            if int(day) > 31: #non-day, some other number
                day = None



        #Use the last seen year
        if year is not None:
            last_year = year

        #Some date was found
        if year or month:

            #For debug purposes
            #print "==\n", sentence, "\n", year, month, day

            #Construct datetime
            dt = None
            if month and day:
                dt = datetime.strptime(day + " " + month + " " + last_year, '%d %B %Y')
                #print month, day, dt
            elif month:
                dt = datetime.strptime(month + " " + last_year, '%B %Y')
            else:
                dt = datetime.strptime(last_year, '%Y')

            events.append((sentence, dt, year, month, day))

    return events

#Prints ISO 8601 format in one column
#The event (text) in the other
def events_to_date_text_tuples(events):
    tups = []
    for event in events:
        text = event[0]
        dt = event[1]
        date_string = str(dt.year)
        if event[3]: #month is known
            date_string += "-"+str(dt.month)

            if event[4]: #day is known
                date_string += "-"+str(dt.day)

        tups.append((date_string,text))

    return tups

#Returns a markdown table from list of tuples
def tuples_to_table(data, header="|Date(ISO8601)|Event|"):
    table = header+"\n"
    table += "|----|---|\n"

    for x1,x2 in data:
        table += "|{0}|{1}|".format(x1,x2) +"\n"
    return table


if __name__ == "__main__":
    text = process_text()

    #Extract events from text
    events = extract_events(text)

    #Sort by datetime
    events.sort(key=operator.itemgetter(1))
    #print events

    event_text_tuples = events_to_date_text_tuples(events)
    #print event_text_tuples
    markdown_table =  tuples_to_table(event_text_tuples)

    out_file = open("table.md", "w")
    out_file.write(markdown_table)
    out_file.close()

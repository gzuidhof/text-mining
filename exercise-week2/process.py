import re
import codecs

def process_text(filename="input.txt"):

    file = open('input.txt','r')
    full_text = file.read().decode('utf8')


    paged = re.sub(r'\n([0-9]+)\n',r'_NEWLINE_\1_NEWLINE_', full_text)

    #Hyphens at the end of sentences get removed, joining the two parts
    unhyphened = paged.replace('-\n',"")
    
    #newlines get removed where the next character is not a capital
    collapsed = re.sub(r'\n([^A-Z])',r"\1", unhyphened)

    #Place newlines where a dot, a character, a capital, 
    #OPTIONAL WHITESPACE, NOT a dot pattern is present
    rebuilt = re.sub(r'[.][ ]([A-Z])([^?\s.])', r'.\n\1\2', collapsed)
    
    rebuilt = rebuilt.replace("_NEWLINE_","\n\n")
    print rebuilt[:10000]    
    
    outfile = codecs.open('out.txt','w','utf-8')
    outfile.write(rebuilt)


if __name__ == "__main__":
    process_text()

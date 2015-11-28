import clam.common.client
import clam.common.data
import clam.common.status
import random
import sys
import time

from credentials import USERNAME, PASSWORD
import requests

#create client, connect to server.
#the latter two arguments are required for authenticated webservices, they can be omitted otherwise


server="http://localhost:8080/frog"
clamclient = clam.common.client.CLAMClient(server)
#clamclient = clam.common.client.CLAMClient("http://webservices-lst.science.ru.nl/frog", USERNAME, PASSWORD)
INPUT_FOLDER = '..\\data\\plaintext\\'
OUTPUT_FOLDER = '..\\data\\frogged\\'

filename = '72099555.txt'
filename_without_extension = filename.split('.')[0]
localfilename=INPUT_FOLDER + filename

#Set a project name (it is recommended to include a sufficiently random naming component here, to allow for concurrent uses of the same client)

project = "lawtopology" + str(random.getrandbits(32))

#Now we call the webservice and create the project (in this and subsequent methods of clamclient, exceptions will be raised on errors).

clamclient.create(project)

#Get project status and specification

data = clamclient.get(project)


#Add one or more input files according to a specific input template. The following input templates are defined,
#each may allow for extra parameters to be specified, this is done in the form of Python keyword arguments to the addinputfile() method, (parameterid=value)
inputtemplate="maininput" #Text document (PlainTextFormat)
#    The following parameters may be specified for this input template:
#        encoding=...  #(StaticParameter) -   Encoding -  The character encoding of the file
#        author=...  #(StringParameter) -   Author -  The author of the document (optional)
#        docid=...  #(StringParameter) -   Document ID -  An ID for the document (optional, used with FoLiA XML output)
#        sentenceperline=...  #(BooleanParameter) -   One sentence per line? -  If set, assume that this input file contains exactly one sentence per line
#        pdfconv=...  #(converter) -    -
#        mswordconv=...  #(converter) -    -
#        latin1=...  #(converter) -    -
#        latin9=...  #(converter) -    -
#inputtemplate="foliainput" #FoLiA XML document (FoLiAXMLFormat)
#    The following parameters may be specified for this input template:

clamclient.addinputfile(project, data.inputtemplate(inputtemplate), localfilename, encoding='utf-8')


#Start project execution with custom parameters. Parameters are specified as Python keyword arguments to the start() method (parameterid=value)
#skip=...  #(ChoiceParameter) -   Skip modules -  Are there any components you want to skip? Skipping components you do not need may speed up the process considerably.
#    valid choices for this parameter:
#    t - Tokeniser
#    m - Multi-Word Detector
#    p - Parser
#    c - Chunker / Shallow parser
#    n - Named Entity Recognition
#    Multiple choices may be combined for this parameter as a comma separated list

data = clamclient.start(project,skip='m,p,c,n')


#Always check for parameter errors! Don't just assume everything went well! Use startsafe() instead of start
#to simply raise exceptions on parameter errors.
if data.errors:
    print >>sys.stderr,"An error occured: " + data.errormsg
    for parametergroup, paramlist in data.parameters:
        for parameter in paramlist:
            if parameter.error:
                print >>sys.stderr,"Error in parameter " + parameter.id + ": " + parameter.error
    #clamclient.delete(project) #delete our project (remember, it was temporary, otherwise clients would leave a mess)
    sys.exit(1)

#If everything went well, the system is now running, we simply wait until it is done and retrieve the status in the meantime
while data.status != clam.common.status.DONE:
    time.sleep(2) #wait 2 seconds before polling status
    data = clamclient.get(project) #get status again
    print >>sys.stderr, "\tRunning: " + str(data.completion) + '% -- ' + data.statusmessage

#Iterate over output files
for outputfile in data.output:

    try:
        outputfile.loadmetadata() #metadata contains information on output template
    except:
        continue

    outputtemplate = outputfile.metadata.provenance.outputtemplate_id

    #You can check this value against the following predefined output templates, and determine desired behaviour based on the output template:
    #if outputtemplate == "mainoutput": #Frog Columned Output (legacy) (TadpoleFormat)
    #if outputtemplate == "foliaoutput": #FoLiA Document (FoLiAXMLFormat)

    #Download the remote file
    if outputtemplate == 'mainoutput':
        frogged_filename = filename_without_extension+'.frog.out'
        url = server+'//'+project+'/output/'+frogged_filename
        r = requests.get(url)
        #print r.content
        with open(OUTPUT_FOLDER+frogged_filename, 'w') as f:
            f.write(r.content)

#delete the project (otherwise it would remain on server and clients would leave a mess)

#clamclient.delete(project)

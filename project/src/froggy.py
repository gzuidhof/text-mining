from __future__ import division
import clam.common.client
import clam.common.data
import clam.common.status
import random
import sys
import time

from credentials import USERNAME, PASSWORD
import requests
import glob
from multiprocessing.pool import ThreadPool

def duration_to_string(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

# Calls frog on all text files
# Uses the CLAM REST api
# Does not seem to work for large sets of files (>1000)

if __name__ == '__main__':
    #create client, connect to server.
    #the latter two arguments are required for authenticated webservices
    server="http://localhost:8080/frog"
    clamclient = clam.common.client.CLAMClient(server)
    #clamclient = clam.common.client.CLAMClient("http://webservices-lst.science.ru.nl/frog", USERNAME, PASSWORD)
    INPUT_FOLDER = '..\\data\\plaintext\\'
    OUTPUT_FOLDER = '..\\data\\frogged\\'

    MANUAL = True


    files = glob.glob(INPUT_FOLDER+'/*.txt')

    #Set project name
    if MANUAL:
        project="manual"
    else:
        project = "law_topology" + str(random.getrandbits(32))
        clamclient.create(project)

    #Now we call the webservice and create the project (in this and subsequent methods of clamclient, exceptions will be raised on errors).


    #Get project status and specification
    data = clamclient.get(project)

    if not MANUAL:
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

        def add_file_to_clam(localfilename):
            clamclient.addinputfile(project, data.inputtemplate(inputtemplate), localfilename, encoding='utf-8')

        print "Adding files to project!"
        pool = ThreadPool(processes=24)
        num_tasks = len(files)
        for i, _ in enumerate(pool.imap_unordered(add_file_to_clam, files), 1):
            sys.stderr.write('\rdone {0:%}'.format(i/num_tasks))
        pool.join()
        pool.close()


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
        #clamclient.delete(project) #delete our project
        sys.exit(1)

    seen = []
    start_time = time.time()

    #If everything went well, the system is now running, we simply wait until it is done and retrieve the status in the meantime
    while data.status != clam.common.status.DONE:
        try:
            time.sleep(2) #wait 2 seconds before polling status
            data = clamclient.get(project) #get status again

            current_filename = data.statusmessage.split(' ')[-1].split('...')[0]
            if current_filename not in seen:
                seen.append(current_filename)


            print '> PROCESSING', current_filename, str(len(seen))+'/'+str(len(files))

            runtime = time.time() - start_time
            per_document_time = runtime/len(seen)
            remaining_time = (len(files)-len(seen))*per_document_time
            total_time = remaining_time+runtime
            print "RUNTIME", duration_to_string(runtime), "("+duration_to_string(per_document_time)+")", 'REMAINING', duration_to_string(remaining_time), 'TOTAL', duration_to_string(total_time)
        except:
            print "Error, but continuing"

    #Iterate over output files
    for outputfile in data.output:

        try:
            outputfile.loadmetadata() #metadata contains information on output template
        except:
            continue #File is a log or error log

        outputtemplate = outputfile.metadata.provenance.outputtemplate_id

        #Download the remote file
        if outputtemplate == 'mainoutput':
            url = str(outputfile)
            frogged_filename = url.split('/')[-1]
            r = requests.get(url)
            with open(OUTPUT_FOLDER+frogged_filename, 'w') as f:
                f.write(r.content)

    #delete the project
    #clamclient.delete(project)

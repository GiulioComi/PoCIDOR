# PocIDOR
A quick-to-edit script for providing Proof of Concept related to Insecure Direct Object Reference vulnerabilities in web application assessments.


Usage: ./IDOR.py [options] <target_url>

    Options:
      -h, --help            show this help message and exit
      -c COOKIE_STRING, --cookie=COOKIE_STRING
                            Set cookies for the request
      -e EXTENSION, --extension=EXTENSION
                            Set extension
      -o FILENAME, --output=FILENAME
                            Set filename output
      -d DIRECTORY, --directory=DIRECTORY
                            Set directory
      -p PROXY, --proxy=PROXY
                            Set proxy
      -u USER_AGENT, --user-agent=USER_AGENT
                            Set User-Agent


Example:
./IDOR.py -c cname:value -o filename -d outDir -p localhost:8080 --user-agent Agente007 https://www.example.target                                                                                          

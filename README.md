# cptdcli-plugin
CPTD CLI plugin 


- Append into manifest at the end of the `community-plugins.json` file with the following format:
    

{  
"name": "example",  
"description": "example",  
"version": "1.0.0",  
"target": "Windows",   <--  add Windows or Linux or MacOs or All 
"entrypoint": "example.py",  
"dependencies": ["example"],  
"author": "example",  
"email": "example@example.com",  
"github": "https://github.com/example/example",   <--  add RAW path your command.zip 
"website": "https://example.com",  
"license": "example.md"  
}
# cptdcli-plugin
CPTD CLI plugin 


- Append into manifest at the end of the `community-plugins.json` file with the following format:
    

{  
"name": "example",  
"description": "short no more than 30 words", 
"long_description":"no more than 150 words",  
"version": "1.0.0",  
"target": "Windows",   <--  add Windows or Linux or MacOs or All   
"entrypoint": "example.py",    
"dependencies": ["example"],    
"author": "example",    
"email": "example@example.com",  
"github": "https://github.com/example/example.zip",   <--  add RAW path your command.zip   
"website": "https://example.com",  
"license": "example.md",   
"documentation":"https://github.com/example/example.md",   <--  add RAW path your command.zip    
}

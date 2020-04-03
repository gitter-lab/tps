## Visualization scripts
**Requirements**

Cytoscape v3.7.1

Anaconda 

other dependencies noted in `minimal_env.yml` file


### Setup

 ***for windows***

Before running the visualization script, edit the run.py file and within the main function. Edit `DIRNAME` and insert the directory that Cytoscape can be found at on your machine. If you do not know where `Cytoscape.exe` is located, you can choose to search the highest directory availible. The script is set to traverse you machines file system starting in the Users directory. 

### Run the Script

From the `visualization_scripts` working direstory of tps call:

`bash activate.sh output.sif "\tps\visualization_scripts\styles.xml"`

Make sure that you use the absolute path to the `styles.xml` file within the visualization_scripts directory.

### Anticipated Issues

The search algorithm takes a long time to executive if the DIRNAME is set high up such as `"C:\Users"`, when tesing this on my machine, sometimes a ConnectionError occurs because the Cytoscape application is unable to establish a connection that the visualiation workflow can use. 

`requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=1234): Max retries exceeded with url: /v1/styles/visualproperties (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000002023707B320>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it',))`

If this happens, run the script again. Because Cytoscape should be open (a current connection is now establsihed) the script should work the second time around. If there are still issues with Cytoscape loading in time, try to edit the DIRNAME to be a lower directory that houses Cytoscape. For example: `"\Documents\Comp_bio\Cytoscape_v3.7.1"` is the directory that houses `Cytoscape.exe`

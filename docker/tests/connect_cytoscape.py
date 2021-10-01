from py2cytoscape import cyrest

def check_cyrest(port):
    print(f"try port {port}")
    cytoscape = cyrest.cyclient(host='localhost', port=port)
    cytoscape.status()

if __name__ == '__main__':
    check_cyrest(1234)
FROM python:3.6

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY connect_cytoscape.py . 

CMD ["python", "./connect_cytoscape.py"]
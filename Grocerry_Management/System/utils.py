import matplotlib.pyplot as plt 
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

from matplotlib.dates import DateFormatter

def get_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.title("Line Chart")
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='Transaction Amount')
    plt.xticks(rotation=45)
    plt.xlabel("Timestamp")
    plt.ylabel("Amount")
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.legend()
    plt.tight_layout()
    graph = get_graph() 
    return graph

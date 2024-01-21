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
    plt.switch_backend('TkAgg')
    plt.figure(figsize=(10, 5))
    plt.title("Professional Line Chart", fontsize=16)
    plt.plot_date(x, y, '-o', color='b', label='Transaction Amount', linewidth=2, markersize=8)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Total Amount", fontsize=12)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().spines['top'].set_color('black')
    plt.gca().spines['right'].set_color('black')
    plt.gca().spines['bottom'].set_color('black')
    plt.gca().spines['left'].set_color('black')
    plt.tick_params(axis='both', which='both', colors='black', labelsize=10)
    plt.legend(fontsize=12)
    plt.tight_layout()
    graph = get_graph()
    return graph

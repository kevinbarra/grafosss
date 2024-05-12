import networkx as nx
from PyQt6 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplWidget(QtWidgets.QWidget):
    """
    A custom widget for matplotlib plots in a PyQt application.
    """

    def __init__(self, parent=None):
        super(MplWidget, self).__init__(parent)
        self.setup_ui()
        self.connect_events()

    def setup_ui(self):
        """
        Set up the UI components and layout.
        """
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def connect_events(self):
        """
        Connect the necessary events for the widget.
        """
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def on_mouse_move(self, event):
        """
        Handle the mouse move event within the matplotlib canvas.
        """
        if event.inaxes:
            x, y = event.xdata, event.ydata
            print(f"Mouse at x={x}, y={y}")

    def update_graph(self, G, pos, node_colors):
        """
        Update the graph drawing on the matplotlib canvas.
        """
        self.axes.clear()
        nx.draw(G, pos, ax=self.axes, with_labels=True, node_color=node_colors, edge_color='black', width=1.0,
                node_size=300)
        self.canvas.draw()


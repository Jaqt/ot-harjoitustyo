from matplotlib.figure import Figure


def create_category_pie_chart(labels, values, transaction_type):
    """Luo ympyräkaavion visualisoimaan käyttäjän tuloja ja menoja. 
    """

    figure = Figure(figsize=(5, 3), dpi=100)
    axes = figure.add_subplot(1, 1, 1)
    axes.pie(values, labels=labels, autopct="%1.1f%%")
    axes.set_title(f"{transaction_type} kategorioittain")
    figure.tight_layout()
    return figure

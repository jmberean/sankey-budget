import plotly.graph_objects as go
import plotly.colors as pc

def create_budget_sankey(
    income_sources,
    expenses,
    title="Budget Sankey Diagram",
    title_color="black",
    layout=None
):
    """..
    Creates a dynamic Sankey diagram to visualize a budget with three verticals:
    Income -> Budget -> Expenses. Each node displays its amount next to its label.

    Parameters:
    - income_sources (dict): Dictionary of income sources and their amounts.
    - expenses (dict): Dictionary of expense categories and their amounts.
    - title (str): Title of the Sankey diagram.
    - title_color (str): Color of the title text.
    - layout (dict): Layout configuration for the Plotly figure.

    Returns:
    - fig (go.Figure): Plotly Figure object representing the Sankey diagram.
    """
    
    # Calculate total income and expenses
    total_income = sum(income_sources.values())
    total_expenses = sum(expenses.values())

    # Validate total income vs expenses
    if total_income < total_expenses:
        discrepancy = total_expenses - total_income
        print(f"Warning: Total expenses (${total_expenses}) exceed total income (${total_income}).")
        print(f"Discrepancy: ${discrepancy}")
    else:
        print(f"Total Income: ${total_income}")
        print(f"Total Expenses: ${total_expenses}")

    # Define nodes: incomes, budget, and expenses
    income_labels = list(income_sources.keys())
    expense_labels = list(expenses.keys())
    budget_label = "Budget"

    # Append amounts to labels
    income_labels_with_amount = [f"{label}\n${amount:,.0f}" for label, amount in income_sources.items()]
    budget_label_with_amount = f"{budget_label}\n${total_income:,.0f}"  # Assuming Budget receives all income
    expense_labels_with_amount = [f"{label}\n${amount:,.0f}" for label, amount in expenses.items()]

    all_labels = income_labels_with_amount + [budget_label_with_amount] + expense_labels_with_amount

    num_income = len(income_labels)
    num_expense = len(expense_labels)

    # Assign unique indices to each node
    label_indices = {label: idx for idx, label in enumerate(all_labels)}

    # Assign colors to income sources
    income_colors_palette = pc.qualitative.Pastel1  # Using Plotly's qualitative color palette for income
    if len(income_labels) > len(income_colors_palette):
        income_colors_palette = income_colors_palette * (len(income_labels) // len(income_colors_palette) + 1)
    income_color_map = {income: income_colors_palette[i] for i, income in enumerate(income_labels)}

    # Assign colors to expenses
    expense_colors_palette = pc.qualitative.Pastel2  # Using Plotly's qualitative color palette for expenses
    if len(expense_labels) > len(expense_colors_palette):
        expense_colors_palette = expense_colors_palette * (len(expense_labels) // len(expense_colors_palette) + 1)
    expense_color_map = {expense: expense_colors_palette[i] for i, expense in enumerate(expense_labels)}

    # Define sources, targets, and values for the Sankey diagram
    sources = []
    targets = []
    values = []
    colors = []

    # Flows from Income Sources to Budget
    for income, amount in income_sources.items():
        sources.append(label_indices[f"{income}\n${amount:,.0f}"])
        targets.append(label_indices[budget_label_with_amount])
        values.append(amount)
        colors.append(income_color_map[income])

    # Flows from Budget to Expenses
    for expense, amount in expenses.items():
        sources.append(label_indices[budget_label_with_amount])
        targets.append(label_indices[f"{expense}\n${amount:,.0f}"])
        values.append(amount)
        colors.append(expense_color_map[expense])

    # Define node positions for fixed arrangement
    node_x = []
    node_y = []

    # Income nodes: x=0
    for _ in income_labels:
        node_x.append(0)
    # Budget node: x=0.5
    node_x.append(0.5)
    # Expense nodes: x=1
    for _ in expense_labels:
        node_x.append(1)

    # Calculate y positions
    # Income nodes: evenly spaced
    income_y_spacing = 1 / (num_income + 1)
    for i in range(num_income):
        node_y.append((i + 1) * income_y_spacing)
    # Budget node: centered
    node_y.append(0.5)
    # Expense nodes: evenly spaced
    expense_y_spacing = 1 / (num_expense + 1)
    for i in range(num_expense):
        node_y.append((i + 1) * expense_y_spacing)

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        arrangement = "fixed",  # Allows manual positioning
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,
            color=["#a6cee3"] * num_income + ["#98df8a"] + ["#ffbb78"] * num_expense,
            x=node_x,
            y=node_y
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=colors,
            hovertemplate='%{source.label} → %{target.label}: $%{value}<extra></extra>'
        )
    )])

    # Prepare layout update dictionary
    layout_update = {
        "title_text": title,
        "title_font": {"size": 24, "color": title_color},
        "font_size": 12,
        "height": 700,
        "width": 1000
    }

    # If a custom layout is provided, merge it into the layout update
    if layout:
        layout_update.update(layout)

    # Update layout
    fig.update_layout(layout_update)

    fig.show()
    return fig

if __name__ == "__main__":
    # === 1. Define Income Sources ===
    income_sources = {
        "Job Salary": 165000,
        "Miranda": 7200.00,
        "Chase Cash Back": 600.00,
        "VMFXX Dividend": 1800.00
    }

    # === 2. Define Expense Categories ===
    expenses  = {
        "Rent": 27120.00,
        "Groceries": 7200.00,
        "Utilities": 4800.00,
        "Transportation": 1620.00,
        "Subscriptions": 393.60,
        "Entertainment": 204.00,
        "Renters Insurance": 136.92
    }

    # === 3. Customize Diagram Appearance ===
    title = "Annual Budget Overview"
    title_color = "black"  # Color of the title text

    # === 4. (Optional) Customize Layout ===
    custom_layout = {
        'paper_bgcolor': "white",
        'plot_bgcolor': "white"
    }

    # === 5. Create and Display the Sankey Diagram ===
    create_budget_sankey(
        income_sources=income_sources,
        expenses=expenses,
        title=title,
        title_color=title_color,
        layout=custom_layout
    )

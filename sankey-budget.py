import plotly.graph_objects as go
import plotly.colors as pc
import streamlit as st

def create_budget_sankey(
    income_sources,
    expenses,
    title="Budget Sankey Diagram",
    title_color="black",
    layout=None
):
    """Creates a dynamic Sankey diagram to visualize a budget with three verticals:
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
        st.warning(f"Total expenses (${total_expenses:,.2f}) exceed total income (${total_income:,.2f}).")
        st.warning(f"Discrepancy: ${discrepancy:,.2f}")
    else:
        st.success(f"Total Income: ${total_income:,.2f}")
        st.success(f"Total Expenses: ${total_expenses:,.2f}")

    # Define nodes: incomes, budget, and expenses
    income_labels = list(income_sources.keys())
    expense_labels = list(expenses.keys())
    budget_label = "Budget"

    # Append amounts to labels
    income_labels_with_amount = [f"{label}\n${amount:,.2f}" for label, amount in income_sources.items()]
    budget_label_with_amount = f"{budget_label}\n${total_income:,.2f}"  # Assuming Budget receives all income
    expense_labels_with_amount = [f"{label}\n${amount:,.2f}" for label, amount in expenses.items()]

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
        sources.append(label_indices[f"{income}\n${amount:,.2f}"])
        targets.append(label_indices[budget_label_with_amount])
        values.append(amount)
        colors.append(income_color_map[income])

    # Flows from Budget to Expenses
    for expense, amount in expenses.items():
        sources.append(label_indices[budget_label_with_amount])
        targets.append(label_indices[f"{expense}\n${amount:,.2f}"])
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

    return fig

def main():
    st.set_page_config(page_title="Budget Sankey Diagram", layout="wide")
    st.title("📊 Budget Sankey Diagram")

    st.sidebar.header("Input Parameters")

    # === 1. Input Income Sources ===
    st.sidebar.subheader("Income Sources")
    income_sources = {}
    num_incomes = st.sidebar.number_input("Number of Income Sources", min_value=1, max_value=20, value=2, step=1)
    for i in range(int(num_incomes)):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            income_name = st.text_input(f"Income {i+1} Name", key=f"income_name_{i}")
        with col2:
            income_amount = st.number_input(f"Amount for {income_name}", min_value=0.0, value=1000.0, step=100.0, key=f"income_amount_{i}")
        if income_name:
            income_sources[income_name] = income_amount

    st.sidebar.markdown("---")

    # === 2. Input Expense Categories ===
    st.sidebar.subheader("Expense Categories")
    expenses = {}
    num_expenses = st.sidebar.number_input("Number of Expense Categories", min_value=1, max_value=20, value=3, step=1)
    for i in range(int(num_expenses)):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            expense_name = st.text_input(f"Expense {i+1} Name", key=f"expense_name_{i}")
        with col2:
            expense_amount = st.number_input(f"Amount for {expense_name}", min_value=0.0, value=500.0, step=50.0, key=f"expense_amount_{i}")
        if expense_name:
            expenses[expense_name] = expense_amount

    st.sidebar.markdown("---")

    # === 3. Customize Diagram Appearance ===
    st.sidebar.subheader("Diagram Appearance")
    title = st.sidebar.text_input("Title of the Diagram", "Annual Budget Overview")
    title_color = st.sidebar.color_picker("Title Color", "#000000")

    # === 4. (Optional) Customize Layout ===
    st.sidebar.subheader("Layout Customization")
    paper_bgcolor = st.sidebar.color_picker("Paper Background Color", "#FFFFFF")
    plot_bgcolor = st.sidebar.color_picker("Plot Background Color", "#FFFFFF")
    custom_layout = {
        'paper_bgcolor': paper_bgcolor,
        'plot_bgcolor': plot_bgcolor
    }

    # === 5. Create and Display the Sankey Diagram ===
    if st.sidebar.button("Generate Sankey Diagram"):
        if not income_sources:
            st.error("Please enter at least one income source.")
        elif not expenses:
            st.error("Please enter at least one expense category.")
        else:
            fig = create_budget_sankey(
                income_sources=income_sources,
                expenses=expenses,
                title=title,
                title_color=title_color,
                layout=custom_layout
            )
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

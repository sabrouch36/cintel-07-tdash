# ==========================================
# 📊 Penguins Dashboard using PyShiny
# ==========================================

# --- 📦 Imports: Load required packages ---
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

# --- 📄 Load Dataset ---
# Loads the built-in Palmer Penguins dataset for analysis
df = palmerpenguins.load_penguins()

# --- 🧾 Set App Title ---
ui.page_opts(title="Penguins Dashboard", fillable=True)

# ==========================================
# 🎛️ Sidebar: Filters and External Links
# ==========================================
with ui.sidebar(title="Filter controls"):
    # --- Filter: Body Mass (grams) ---
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)

    # --- Filter: Penguin Species ---
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    # --- 🔗 External Resource Links ---
    ui.hr()
    ui.h6("Links")
    ui.a("GitHub Source", href="https://github.com/denisecase/cintel-07-tdash", target="_blank")
    ui.a("GitHub App", href="https://denisecase.github.io/cintel-07-tdash/", target="_blank")
    ui.a("GitHub Issues", href="https://github.com/denisecase/cintel-07-tdash/issues", target="_blank")
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("Template: Basic Dashboard", href="https://shiny.posit.co/py/templates/dashboard/", target="_blank")
    ui.a("See also", href="https://github.com/denisecase/pyshiny-penguins-dashboard-express", target="_blank")

# ==========================================
# 🔢 Value Boxes: Summary Metrics
# ==========================================
with ui.layout_column_wrap(fill=False):
    # --- 🐧 Total Penguins Count ---
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"
        @render.text
        def count():
            return filtered_df().shape[0]

    # --- 📏 Average Bill Length ---
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # --- 📐 Average Bill Depth ---
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# ==========================================
# 📊 Charts and Interactive Data Table
# ==========================================
with ui.layout_columns():

    # --- 📈 Scatterplot Card ---
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Bill Depth")
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # --- 📋 Data Table Card ---
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data Table (Interactive)")
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# ==========================================
# 🧠 Reactive Calculation: Filtered Dataset
# ==========================================
@reactive.calc
def filtered_df():
    # Filters the original dataset based on selected species and mass limit
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df

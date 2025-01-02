import json
from typing import Dict, Any
import PySimpleGUI as sg
import pandas as pd

def load_json_data(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)

def get_all_moderator_data(data: Dict[str, Any]) -> pd.DataFrame:
    moderators = []
    for moderator_type in ['Solid', 'Fluid']:
        for category, category_moderators in data[moderator_type].items():
            for moderator in category_moderators:
                moderator['Type'] = moderator_type
                moderator['Mod'] = category
                moderators.append(moderator)
    df = pd.DataFrame(moderators)

    # Define heat conductivity mapping
    conductivity_map = {
        "IHeatEntity.CONDUCTIVITY_AIR": 0.05,
        "IHeatEntity.CONDUCTIVITY_RUBBER": 0.01,
        "IHeatEntity.CONDUCTIVITY_WATER": 0.1,
        "IHeatEntity.CONDUCTIVITY_STONE": 0.15,
        "IHeatEntity.CONDUCTIVITY_GLASS": 0.3,
        "IHeatEntity.CONDUCTIVITY_IRON": 0.6,
        "IHeatEntity.CONDUCTIVITY_COPPER": 1.0,
        "IHeatEntity.CONDUCTIVITY_SILVER": 1.5,
        "IHeatEntity.CONDUCTIVITY_GOLD": 2.0,
        "IHeatEntity.CONDUCTIVITY_EMERALD": 2.5,
        "IHeatEntity.CONDUCTIVITY_DIAMOND": 3.0,
        "IHeatEntity.CONDUCTIVITY_GRAPHENE": 5.0
    }

    # Convert heat conductivity values
    df['heatConductivity'] = df['heatConductivity'].map(lambda x: conductivity_map.get(x, x))
    # Convert numeric columns to float, ignoring non-numeric values
    numeric_columns = ['absorption', 'heatEfficiency', 'moderation', 'heatConductivity']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def main():
    file_path = r"c:\Users\bjzol\Desktop\ExtremeReactors2 Data\reactor_moderator_data.json"
    data = load_json_data(file_path)
    df = get_all_moderator_data(data)

    # Get unique mod names
    mod_names = sorted(df['Mod'].unique())
    sg.theme('DarkBlue3')

    layout = [
        [sg.Text('Reactor Moderator Data Viewer', font=('Helvetica', 20))],
        [sg.Text('Select Mods:'), sg.Listbox(values=mod_names, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key='-MODS-', size=(30, 6))],
        [sg.Text('Sort by:'), sg.Combo(['Type', 'Mod', 'id', 'absorption', 'heatEfficiency', 'moderation', 'heatConductivity'], key='-SORT-', enable_events=True)],
        [sg.Table(values=df[['Type', 'Mod', 'id', 'absorption', 'heatEfficiency', 'moderation', 'heatConductivity']].values.tolist(),
                  headings=['Type', 'Mod', 'ID', 'Absorption', 'Heat Efficiency', 'Moderation', 'Heat Conductivity'],
                  auto_size_columns=False, justification='right', num_rows=20, key='-TABLE-', 
                  col_widths=[10, 15, 30, 15, 15, 15, 15])],
        [sg.Button('Update'), sg.Button('Exit')]
    ]

    window = sg.Window('Extreme Reactors 2 Data Viewer', layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        if event == 'Update' or event == '-SORT-':
            selected_mods = values['-MODS-']
            sort_by = values['-SORT-']

            if selected_mods:
                df_filtered = df[df['Mod'].isin(selected_mods)]
            else:
                df_filtered = df
            if sort_by:
                df_filtered = df_filtered.sort_values(by=sort_by, ascending=False)

            table_data = df_filtered[['Type', 'Mod', 'id', 'absorption', 'heatEfficiency', 'moderation', 'heatConductivity']].values.tolist()
            window['-TABLE-'].update(values=table_data)
    window.close()

if __name__ == "__main__":
    main()


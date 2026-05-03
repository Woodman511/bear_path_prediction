import graph_prob as gp
import cartopy.crs as ccrs
import path_find as pf
import random as rand
import tkinter as tk
import customtkinter as ctk
import path_find_branch as pfb

#gp.plt.ion()
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root.title("Bear Path Visualization")
root.geometry("375x350")
root.attributes('-topmost', True) 
root.resizable(False, False)



def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def run_branch_visualization(user_start_lat, user_start_lon):
    clear_window()
    root.geometry("600x90")
    ctk.CTkLabel(root, text="Running Running Simulation for Bear Path...", font=fnt2).pack(pady=20)
    root.update()

    # Print the valid coordinate range for the loaded grid.
    print(f"Grid latitude range: {gp.lat_matrix.min():.6f} to {gp.lat_matrix.max():.6f}")
    print(f"Grid longitude range: {gp.lon_matrix.min():.6f} to {gp.lon_matrix.max():.6f}")

    start_row, start_col = pf.nearest_grid_cell(gp.lat_matrix, gp.lon_matrix, user_start_lat, user_start_lon)
    print(f"Nearest grid cell for start coordinate ({user_start_lat}, {user_start_lon}) -> row={start_row}, col={start_col}")

    # Run path finding algorithm to get the bear movement path using the nearest grid cell for the given lon/lat.
    paths = pfb.run(users_pos_row=start_row, users_pos_col=start_col)

        # Convert grid indices to geographic coordinates for plotting
    first = True
    x_list = []
    y_list = []

    for n in paths:
        for x, y in n:
            x_list.append(gp.lon_matrix[x,y])
            y_list.append(gp.lat_matrix[x,y])

    # Plot the path on the map
    ca_map.plot(x_list, y_list,
                markersize=3,
                color='blue',
                zorder=3,
                transform=ccrs.PlateCarree(), 
                marker='o', 
                label='Start',
                linestyle='solid',
                linewidth=1)

    # Add a zoomed-in view around the bear path.
    for n in paths:
        gp.graph_zoomed_data(path=n, name="Zoomed Bear Path")

    root.quit()
    root.destroy() # Close the Tkinter window after plotting

    #gp.plt.pause(0.01)
    gp.plt.show()


def run_visualization(user_start_lat, user_start_lon):
    clear_window()
    root.geometry("600x90")
    ctk.CTkLabel(root, text="Running Running Simulation for Bear Path...", font=fnt2).pack(pady=20)
    root.update()

    # Print the valid coordinate range for the loaded grid.
    print(f"Grid latitude range: {gp.lat_matrix.min():.6f} to {gp.lat_matrix.max():.6f}")
    print(f"Grid longitude range: {gp.lon_matrix.min():.6f} to {gp.lon_matrix.max():.6f}")

    start_row, start_col = pf.nearest_grid_cell(gp.lat_matrix, gp.lon_matrix, user_start_lat, user_start_lon)
    print(f"Nearest grid cell for start coordinate ({user_start_lat}, {user_start_lon}) -> row={start_row}, col={start_col}")

    # Run path finding algorithm to get the bear movement path using the nearest grid cell for the given lon/lat.
    path = pf.run(
        user_start_lon=user_start_lon,
        user_start_lat=user_start_lat,
    )

    # Convert grid indices to geographic coordinates for plotting
    first = True
    x_list = []
    y_list = []

    for x, y in path:
        x_list.append(gp.lon_matrix[x,y])
        y_list.append(gp.lat_matrix[x,y])

    # Plot the path on the map
    ca_map.plot(x_list, y_list,
                markersize=3,
                color='blue',
                zorder=3,
                transform=ccrs.PlateCarree(), 
                marker='o', 
                label='Start',
                linestyle='solid',
                linewidth=1)

    # Add a zoomed-in view around the bear path.
    gp.graph_zoomed_data(path=path, name="Zoomed Bear Path")

    root.quit()
    root.destroy() # Close the Tkinter window after plotting

    #gp.plt.pause(0.01)
    gp.plt.show()

fnt = ("Arial", 20)
fnt2 = ("Arial", 25, "bold")
fnt3 = ("Arial", 10)

ctk.CTkLabel(root, font=fnt3, text="").pack()  # Spacer
ctk.CTkLabel(root, font=fnt, text="Enter Starting Latitude:").pack(pady=10)
lat_entry = ctk.CTkEntry(root, font=fnt, justify=tk.RIGHT)
lat_entry.pack()
lat_entry.insert(0, "61.180106")  # Default to Anchorage, Alaska latitude

ctk.CTkLabel(root, font=fnt, text="").pack(pady=5)  # Spacer

ctk.CTkLabel(root, font=fnt, text="Enter Starting Longitude:").pack(pady=10)
lon_entry = ctk.CTkEntry(root, font=fnt, justify=tk.RIGHT)
lon_entry.pack()
lon_entry.insert(0, "-149.787058")  # Default to Anchorage, Alaska longitude

ctk.CTkLabel(root, font=fnt3, text="").pack()  # Spacer
ctk.CTkButton(root, text="Run Path Simulation", font=fnt2, command=lambda: run_branch_visualization(float(lat_entry.get()), float(lon_entry.get()))).pack(pady=20)

root.update()
# Create initial probability map visualization
ca_map = gp.graph_data(name="Initial Probability Map")
gp.plt.show()


root.mainloop()
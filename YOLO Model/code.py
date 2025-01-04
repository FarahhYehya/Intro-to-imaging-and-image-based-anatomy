import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
import cv2
from ultralytics import YOLO
import numpy as np
import math
import os
import threading

# Load the YOLO model
model = YOLO(r"C:\Users\MARIAM\OneDrive\Documenten\Desktop\best.pt")

# Initialize player tracking and storage for movement data
player_tracker = {}
next_id = 0
max_distance = 50  # Max distance to match players across frames
player_positions = {}  # Store positions per player ID for heatmap generation
output_path = ""

def get_player_id(x, y):
    global next_id

    for player_id, (px, py) in player_tracker.items():
        distance = math.sqrt((x - px) ** 2 + (y - py) ** 2)
        if distance < max_distance:
            player_tracker[player_id] = (x, y)
            return player_id

    # Assign new ID if no match is found
    player_id = next_id
    player_tracker[player_id] = (x, y)
    player_positions[player_id] = []  # Initialize empty list for new player's positions
    next_id += 1
    return player_id

def detect_and_save_video(input_path, output_folder):
    global output_path
    output_path = os.path.join(output_folder, "processed_video.mp4")
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform detection with YOLO
        results = model(frame)

        for result in results[0].boxes:
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            cls = int(result.cls[0])

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            player_id = get_player_id(center_x, center_y)

            # Store player positions by ID for heatmap
            player_positions[player_id].append((center_x, center_y))

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"ID {player_id} - {model.names[cls]}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()

    # Populate player list after processing video
    populate_player_list()

def populate_player_list():
    player_list.delete(0, tk.END)  # Clear existing entries
    for player_id in player_positions.keys():
        player_list.insert(tk.END, player_id)

def select_player_for_heatmap():
    try:
        selected_index = player_list.curselection()[0]  # Get selected index
        player_id = player_list.get(selected_index)  # Get player ID
        if player_id not in player_positions:
            messagebox.showwarning("Warning", "No positions recorded for this Player ID.")
            return

        # Generate and display the heatmap for the selected player
        show_player_heatmap(player_id)
    except IndexError:
        messagebox.showwarning("Warning", "Please select a player ID.")

def show_player_heatmap(player_id):
    positions = player_positions[player_id]

    # Load the football pitch background
    pitch_background = cv2.imread(r"C:\Users\MARIAM\OneDrive\Desktop\Screenshot 2024-10-28 215128.png")  # Provide the correct path to your pitch image
    height, width = pitch_background.shape[:2]  # Get the dimensions of the pitch image

    # Create the heatmap with increased intensity for movement trails
    heatmap = np.zeros((height, width), np.float32)

    for (x, y) in positions:
        if 0 <= y < height and 0 <= x < width:
            heatmap[y, x] += 10  # Increase intensity value for more visibility

    # Apply Gaussian blur for smoother heat distribution
    heatmap = cv2.GaussianBlur(heatmap, (15, 15), 0)

    # Normalize and apply temperature color map
    normalized_heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    colored_heatmap = cv2.applyColorMap(normalized_heatmap.astype(np.uint8), cv2.COLORMAP_JET)

    # Resize the pitch image to match heatmap dimensions
    pitch_background = cv2.resize(pitch_background, (width, height))  # Resize to match heatmap dimensions

    # Blend heatmap with the pitch background
    blended_heatmap = cv2.addWeighted(pitch_background, 0.6, colored_heatmap, 0.4, 0)

    # Display the blended heatmap
    cv2.imshow(f"Movement Heatmap for Player {player_id}", blended_heatmap)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def play_video():
    global output_path
    cv2.namedWindow("Processed Video", cv2.WINDOW_NORMAL)
    video_cap = cv2.VideoCapture(output_path)
    while video_cap.isOpened():
        ret, frame = video_cap.read()
        if not ret:
            break
        cv2.imshow("Processed Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit playback early
            break
    video_cap.release()
    cv2.destroyAllWindows()

def upload_video():
    input_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4;.avi")])
    if not input_path:
        return

    output_folder = filedialog.askdirectory(title="Select Folder to Save Processed Video")
    if not output_folder:
        return

    # Run video processing in a separate thread
    threading.Thread(target=detect_and_save_video, args=(input_path, output_folder)).start()

    # Run video playback in a separate thread once processing is complete
    threading.Thread(target=play_video).start()

# GUI Setup
root = tk.Tk()
root.title("YOLO Video Detection with Player-Specific Heatmap")

upload_button = tk.Button(root, text="Upload Video", command=upload_video)
upload_button.pack(pady=20)

# Listbox for player selection
player_list = Listbox(root, height=10)
player_list.pack(pady=20)

# Add a scrollbar
scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
player_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=player_list.yview)

# Button to select heatmap
heatmap_button = tk.Button(root, text="Select Player for Heatmap", command=select_player_for_heatmap)
heatmap_button.pack(pady=20)

root.mainloop()
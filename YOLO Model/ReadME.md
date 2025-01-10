🎥 YOLO Video Detection with Player-Specific Heatmap
This project is a Python application that uses the YOLO (You Only Look Once) object detection model to detect players in a video, track their movements, and generate player-specific heatmaps. Built with tkinter for the GUI, OpenCV for video processing, and ultralytics for YOLO model integration, this tool is perfect for analyzing sports videos (e.g., football/soccer) and visualizing player movements on a heatmap overlaid on a football pitch.

✨ Features
- Player Detection: Detect players in a video using a pre-trained YOLO model.
- Player Tracking: Track players across frames and assign unique IDs to each player.
- Heatmap Generation: Generate heatmaps for individual players based on their movement throughout the video.
- User-Friendly GUI: Easily upload videos, process them, and view heatmaps with a simple interface.
- Multi-Threading: Process videos and play them back in separate threads for a smooth user experience.

### 📸 Screenshots

Here are some screenshots of the match and the generated heatmaps:

#### Match Screenshots
1. **Player Detection**  
   ![Player Detection](https://github.com/user-attachments/assets/a8a1d189-2891-4604-9c69-b75678b66823)  
   *Players detected and tracked using the YOLO model.*

2. **Player Tracking**  
   ![Player Tracking](https://github.com/user-attachments/assets/1ceb07d2-c9cb-4247-a959-e1c5c9cd1765)  
   *Players are assigned unique IDs and tracked across frames.*

#### Heatmap Screenshots
   **Player-Specific Heatmap**  
   ![Player Heatmap](https://github.com/user-attachments/assets/fcc59fd7-c6b5-4d7f-918f-267f063902b0)  
   *Heatmap showing the movement of a specific player on the football pitch.*

🛠️ Requirements
To run this project, you need the following Python packages:
- tkinter (usually comes pre-installed with Python)
- opencv-python
- ultralytics
- numpy

Install the required packages using pip:
```bash
pip install opencv-python ultralytics numpy
```

🚀 Setup
1. Clone the Repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Download YOLO Model:
   - Download the YOLO model weights file (e.g., `best.pt`) and place it in the project directory.
   - Update the model path in the script to point to your model file.

3. Football Pitch Background:
   - Download a football pitch image (e.g., `pitch_background.png`) and place it in the project directory.
   - Update the `pitch_background` path in the script to point to your image file.

4. Run the Application:
   ```bash
   python your_script_name.py
   ```

🎮 Usage
- **Upload a Video**: Click the "Upload Video" button to select a video file (e.g., `.mp4`, `.avi`).
- **View Processed Video**: The processed video will be displayed in a new window once the processing is complete. Press `q` to exit the video playback.
- **Generate Heatmap**: After processing the video, select a player ID from the list and click the "Select Player for Heatmap" button to generate and view the heatmap for the selected player.

🧩 How It Works
- **Video Upload**: The user uploads a video file, which is processed frame-by-frame using the YOLO model to detect players.
- **Player Tracking**: Each detected player is assigned a unique ID. Players are tracked across frames using a distance-based matching algorithm.
- **Heatmap Generation**: The movement of each player is recorded and stored as a list of coordinates. A heatmap is generated for the selected player by plotting their movement on a football pitch background.
- **Video Playback**: The processed video (with bounding boxes and player IDs) is saved and can be played back in a new window.

🔧 Customization
- **YOLO Model**: Train your own YOLO model or use a pre-trained model for specific use cases (e.g., different sports or objects). Update the model path in the script to use your custom model.
- **Heatmap Intensity**: Adjust the intensity of the heatmap by modifying the value in the `heatmap[y, x] += 10` line in the `show_player_heatmap` function.
- **Football Pitch Background**: Replace the `pitch_background.png` file with a different image to customize the heatmap background.
- **Max Distance for Player Tracking**: Adjust the `max_distance` variable in the `get_player_id` function to control how far a player can move between frames before being assigned a new ID.

🗂️ Code Structure
- `detect_and_save_video`: Processes the video, detects players, and saves the processed video.
- `get_player_id`: Tracks players across frames and assigns unique IDs.
- `show_player_heatmap`: Generates and displays a heatmap for a selected player.
- `play_video`: Plays the processed video in a new window.
- `upload_video`: Handles video upload and initiates processing.
- `populate_player_list`: Populates the list of player IDs in the GUI.

🔮 Future Improvements
- **Multi-Player Heatmaps**: Generate heatmaps for multiple players simultaneously.
- **Advanced Tracking**: Implement more robust player tracking algorithms (e.g., Kalman filters).
- **Export Heatmaps**: Add functionality to save heatmaps as image files.
- **Performance Optimization**: Optimize the code for faster processing of high-resolution videos.
- **Custom Sports**: Extend the application to support other sports (e.g., basketball, hockey).

🤝 Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Submit a pull request.

Feel free to open an issue if you find any bugs or have suggestions for improvements.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgments
- YOLO by Ultralytics for the object detection model.
- OpenCV for video processing and heatmap generation.
- Tkinter for the GUI interface.
```

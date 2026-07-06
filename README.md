## Music Library Manager

> 📌 Part of the Music Engineering Journey  
> [Roadmap](https://github.com/amin-soleimani1/music-engineering-journey)

🌐 **Language:** English | [فارسی](README.fa.md)


## Phase 2 — Database-Driven Desktop Application

A desktop music library manager built with **Python**, **CustomTkinter**, and **SQLite**.

This project is the second iteration of my original **Music Player** project. While the first version focused on learning the fundamentals of GUI development, this version was redesigned to explore software architecture, database integration, refactoring, and building a more maintainable desktop application.

---

## 🔗 Project Roadmap

⬅️ **Previous Phase**  
[Music Player Basic](https://github.com/amin-soleimani1/music-player-basic)

➡️ **Next Phase**  
Music Management Platform *(Coming Soon)*

---

> **Note**  
> This is an educational project focused on learning software design, architecture, and Python development. It is not intended to be a production-ready application.

---

| Version | Main Focus |
|----------|------------|
| 🎵 Music Player | GUI development, audio playback, basic architecture |
| 📚 Music Library Manager | SQLite integration, MVC-style architecture, refactoring, improved UX, modular design |

Instead of starting from scratch, this project was built by iterating on an existing codebase to gain real-world experience in refactoring and improving software architecture.

---

# Preview

### Main Interface
<p align="center">
  <img src="assets/images/Screenshot 1.png" width="800"/>
</p>

### Playlist View
<p align="center">
  <img src="assets/images/Screenshot 2.png" width="800"/>
</p>

### Demo
<p align="center">
  <img src="assets/images/demo_gif.gif" width="800"/>
</p>

---

# ✨ Features

## 🎼 Music Library
- Browse all music files
- Automatic library management using stored metadata
- Album artwork support
- Display artist and song metadata

## ❤️ Favorites
- Mark songs as favorites
- Dedicated favorites section

## 🕒 Recently Played
- Automatic playback history tracking
- View recently played songs

## 📂 Playlist Management
- Create custom playlists
- Store playlists in SQLite database
- Manage playlist contents

## Smart Song Search

* 🔍 Search songs by name
* Fuzzy search that suggests the closest match when a partial song name is entered

## ▶ Playback Controls
- Play / Pause
- Previous / Next
- Repeat single song
- Repeat playlist

## 🖥 User Interface
- Fully redesigned UI
- Improved user experience
- Cleaner navigation structure
- More modular UI architecture

---

# 🧠 Architecture

This project follows a **hybrid MVC + service-layer architecture** to clearly separate responsibilities across the application.

---

## 📦 Models

The Models layer contains only data structures.

It defines simple data representations such as:

- Track model
- Playlist model

> Models do not contain business logic or database operations.

---

## ⚙️ Core (Service Layer)

The Core layer contains the main business logic of the application, including:

- Audio playback engine
- SQLite database operations
- Application-level logic

> This layer acts as the service layer of the system.

---

## 🎮 Controller

The Controller layer manages communication between the UI and Core.

In this version, the controller has been redesigned to improve decoupling.

Instead of relying on UI indexes, operations are now based on the selected music file path, reducing coupling between UI and logic.

---

## 🖼 View (UI)

The View layer is implemented using **CustomTkinter**.

It is responsible only for:
- Displaying information
- Handling user interactions

---

## 🧩 Utils

Reusable helper functions are organized in the `utils` package to improve code reuse and maintainability.

---

# 🗄 Database

The application uses **SQLite** for local data storage.

Stored data includes:

- Music metadata
- File paths
- Favorite songs
- Recently played history
- Playlist data

Using a database enabled persistent storage and made it possible to implement more advanced features compared to the previous version.

---

# 🛠 Technologies

- Python
- CustomTkinter
- CTklistbox
- SQLite
- pygame
- Pillow
- music_tag

---

# 📁 Project Structure

The project follows a modular architecture that separates UI, logic, data models, database operations, and utilities for better maintainability.

```
Music Library Manager/
│
├── main.py # Application entry point
│
├── app/ # Application layer
│   ├── app.py # Application initialization
│   └── controllers.py # Controller layer
│
├── core/ # Business logic (service layer)
│   ├── database.py # Database operations
│   └── player.py # Audio playback engine
│
├── models/ # Data models
│   ├── track.py # Track data model
│   └── playlist.py # Playlist data model
│
├── ui/ # User interface
│   └── main_window.py # Main application window
│
├── utils/ # Utility functions
│   └── file_utils.py # File handling utilities
│
└── assets/ # Static resources
    ├── icons/ # Application icons
    └── images/ # Album artwork and UI images
```

---

# 📚 What I Learned

This project was built as a learning experience.

During development, I gained a deeper understanding of:

- Database design and persistent storage
- Practical use of SQLite in desktop applications
- MVC and service-layer architecture
- Object-oriented programming
- Code refactoring and restructuring
- Writing cleaner and more maintainable Python code
- Organizing medium-sized projects
- Using virtual environments (`venv`)
- Iterative UI/UX improvements

Most importantly, I learned that software development is not just about adding features, but about continuously improving structure, readability, and maintainability.

---

## Requirements
- Python 3.10+ (tested on 3.10, 3.11, 3.12)


# 🚀 Installation

Clone the repository:
```bash
git clone https://github.com/amin-soleimani1/Music-Library-Manager.git
```

Create a virtual environment:
```bash
python -m venv .venv
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run application:
```bash
python main.py
```

# 🔮 Future Plans

This is the final desktop version of the Music Library Manager.

Future versions will transition into a web-based architecture using:

FastAPI (Backend)     
React (Frontend)     
PostgreSQL     
AI-powered features in later stages     

---

This project is created for educational purposes.     
Feel free to explore, learn from, and reuse ideas from this repository.

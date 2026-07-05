# 🎵 Music Library Manager

> 📌 Part of the Music Engineering Journey  
> https://github.com/amin-soleimani1/music-engineering-journey

🌐 **Language:** English | [فارسی](README.fa.md)

Phase 2 — Database-Driven Desktop Application

A desktop music library manager built with **Python**, **CustomTkinter**, and **SQLite**.

This project is the second iteration of my original **Music Player** project. While the first version focused on learning the fundamentals of GUI development, this version was redesigned and expanded to explore software architecture, database integration, code organization, and building a more maintainable desktop application.

### 🔗 Project Roadmap
⬅️ **Previous Phase**     
[Music Player Basic](https://github.com/amin-soleimani1/music-player-basic)     
➡️ **Next Phase**     
Music Management Platform *(Coming Soon)*

> **Note**
>
> This is an educational project developed to practice software design concepts and improve my Python development skills. It is not intended to be a production-ready music player.

---

# Project Evolution

This project represents the evolution of a previous learning project.

| Version                  | Main Focus                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| 🎵 Music Player          | GUI development, audio playback, basic project structure                                          |
| 📚 Music Library Manager | SQLite integration, MVC architecture, code refactoring, improved UX, cleaner project organization |

Instead of starting a completely new project, I chose to improve and redesign an existing one. This allowed me to experience the process of refactoring, restructuring, and extending a real codebase while applying newly learned concepts.

---

# Preview

### Main Interface
<p align="center">
  <img src="assets\images\Screenshot 1.png" width="3000"/>
</p>

### Playlist View
<p align="center">
  <img src="assets\images\Screenshot 2.png" width="3000"/>
</p>

### Demo
<p align="center">
  <img src="assets\images\demo_gif.gif" width="3000"/>
</p>

---

# Features

## 🎼 Music Library

* Browse all music files
* Automatically manage the music library using stored metadata
* Album artwork support
* Artist and song metadata display

## ❤️ Favorites

* Mark songs as favorites
* Browse all favorite songs in a dedicated section

## 🕒 Recently Played

* Automatically track recently played songs
* Dedicated view for playback history

## 📂 Playlist Management

* Create custom playlists
* Store playlists in the database
* Manage playlist contents

## ▶ Playback Controls

* Play / Pause
* Previous / Next
* Repeat current song
* Repeat playlist

## 🖥 User Interface

* Completely redesigned interface
* Improved user experience
* Better navigation and organization
* More maintainable UI structure

---

# Architecture

This project follows the **Model–View–Controller (MVC)** architectural pattern to better separate responsibilities across the application.

## Model

The Model layer contains the application's data structures and database-related logic.

Examples include:

* Music metadata model
* SQLite interaction
* Data persistence

## View

The View layer is responsible for rendering the graphical interface using **CustomTkinter**.

It focuses only on presenting information and receiving user interactions.

## Controller

The Controller coordinates communication between the user interface and the application's logic.

Compared to the previous version, the controller has been significantly redesigned.

Instead of relying on UI indexes to identify songs, it now performs operations based on the selected music file path. This reduces unnecessary coupling between the interface and the application logic, resulting in a more maintainable architecture.

## Utilities

Reusable helper modules are organized inside a dedicated `utils` package to reduce duplicated code and improve project organization.

---

# Database

The application uses **SQLite** as its local database.

The database stores information such as:

* Music metadata
* File paths
* Favorite songs
* Recently played history
* Playlist information

Using a database made it possible to implement features that were difficult to manage in the previous version while also providing practical experience with persistent application data.

---

# Technologies

* Python
* CustomTkinter
* SQLite
* pygame
* Pillow
* music_tag

---

# Project Structure
The project follows a modular architecture that separates the user interface, application logic, data models, database operations, and utility modules to improve maintainability and scalability.

```
Music Library Manager/
│
├── main.py                  # Application entry point
│
├── app/                     # Application layer
│   ├── app.py               # Application initialization
│   └── controllers.py       # Application controllers
│
├── core/                    # Core application logic
│   ├── database.py          # Database operations
│   └── player.py            # Audio playback engine
│
├── models/                  # Data models
│   ├── track.py             # Track data model
│   └── playlist.py          # Playlist data model
│
├── ui/                      # User interface
│   └── main_window.py       # Main application window
│
├── utils/                   # Utility functions
│   └── file_utils.py        # File handling utilities
│
└── assets/                  # Static resources
    ├── icons/               # Application icons
    └── images/              # Album artwork and UI images
```

---

# What I Learned

This project was mainly developed as a learning experience.

During development I gained a much deeper understanding of:

* Database design and why persistent storage matters
* Practical use of SQLite in desktop applications
* MVC architecture
* Object-oriented programming
* Refactoring an existing codebase
* Writing cleaner and more maintainable Python code
* Organizing larger projects
* Using Python virtual environments (`venv`)
* Improving user experience through iterative interface redesign

More importantly, this project helped me understand that software development is not only about adding features, but also about improving architecture, readability, and maintainability.

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it and install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

---

# Future Plans

This project represents the final desktop iteration of this learning journey.

Future versions will explore modern web technologies such as **React** and **FastAPI**, applying the same concepts in a web-based environment with a different application architecture.

---

# License

This repository is published for educational purposes.

Feel free to explore the source code, learn from it, and use ideas from the project in your own learning journey.

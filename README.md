# 💡 Tensile Test Machine powered by a Raspberry Pi!

A low-cost, open-source tensile testing machine designed to measure the **Young’s modulus** of soft materials — perfect for classrooms, underfunded labs, or makerspaces. It uses a **Raspberry Pi** for data acquisition and offers a hands-on introduction to electronics, programming, and materials science.

---

## 🔧 Features

- Measures force and displacement to calculate Young’s modulus  
- Raspberry Pi-powered for real-time data acquisition  
- Designed for educational and experimental use  
- Budget-friendly and easy to build  

---

## 📚 Background

**Young's modulus** (elasticity modulus) describes how a material stretches or deforms under stress. It’s a fundamental property used in engineering and science — from construction to biomedical devices. Measuring it helps us understand how materials behave under force.

Professional-grade tensile testing machines are expensive and inaccessible for many schools and labs. That’s why we built this simplified, affordable version using commonly available parts — including a **Raspberry Pi**.

This project introduces students and makers to:
- Hands-on mechanical testing  
- Basic electronics  
- Python programming  
- Data collection and analysis  

---

## 🚀 Ready to Get Started?

👉 **[Full Guide: Setting up the Raspberry Pi](https://yarelisacevedo.github.io/Raspberry-Pi-powered-Tensile-Machine/)**

---

## 🔌 Step 1: Update your Raspberry Pi

Before installing anything, make sure your Pi is fully updated:

```bash
sudo apt update
sudo apt full-upgrade
sudo reboot
```

## 🧰 Step 2: Install Required Libraries for the GUI

Use pip and apt to install all the dependencies:

```bash
pip install RPi.GPIO PyQt5 matplotlib hx711
sudo apt-get install python3-rpi.gpio
```

## 📥 Step 3: Download the GUI Files

If you'd like to save the GUI in your Documents folder:

```bash
cd ~/Documents
git clone https://github.com/YarelisAcevedo/Raspberry-Pi-powered-Tensile-Machine.git
```

## ▶️ Step 4: Run the GUI

Navigate into the GUI folder and start the program:

```bash
cd Raspberry-Pi-powered-Tensile-Machine/GUI
python3 main.py
```


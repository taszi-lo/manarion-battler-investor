# Various Manarion Data Visualizations

This project showcases a  **data visualization** created with [Plotly](https://plotly.com/).  
It explores and presents various aspects of Manarion-related data through clear, interactive charts and graphs.

---

## Overview
The goal of this project is to turn raw Manarion data into intuitive visual stories.

This visualization focuses on a singular dataset or metric, rendered using **Plotly Express** for easy exploration and interactivity.

---

## Requirements
Make sure you have **Python 3.8+** and install dependencies:
```bash
pip install plotly pandas
```
---

## Usage
Clone the repository, enter name, tax and 300 to main.py, and run the visualization locally:
git clone https://github.com/taszi-lo/manarion-battler-investor.git

cd manarion-battler-investor

python main.py

This will open a chart in your default browser.

---

## Assumptions
Bigger number = better upgrade.
Being a battler in manarion is hard, lots of variables, so we must assume a couple things, here are my assumptions:
The player does not use resurrect pet. (From a defensive point of view, it is a worse pet than a ward pet)
The player has enough mana to sustain higher mana costs from either higher level spell tome upgrades or more haste/multicast/time dilation/overload.
The player can fight stronger monsters by elongating the fight through defensive upgrades. (aka not at round limit of 199)
For the dust collector the efficiency is assuming an x1 speed, if the player decides to run higher speed, efficiency will lower accordingly.
For shards the lowest of the offensive skills will be the one to provide the highest efficiency. Unless you raise the lowest, the script will keep saying the same value.
The red dots are offensive upgrades, upgrade these when you reach round limit. The blue ones are defensive, upgrade these when you're not at round limit. (Or don't, it's up to you.)
Mobshift is the amount of mob strength you can fight stronger mobs if you increase your damage output by 10%. Seems to be around 300 at 250k-330k, i'm assuming it's the same for most of the mob progression. Feel free to change it if you're on a different opinion.
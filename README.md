# Scientific Calculator

A dark-themed scientific calculator with a desktop GUI, built with Python's standard `tkinter` library. No third-party packages are needed.

## Features

- Basic arithmetic: `+`, `−`, `×`, `/`, and percent
- Power (`xʸ`) and trigonometric functions: `sin`, `cos`, `tan`
- **2nd** key switches the trig buttons to their inverses (`sin⁻¹`, `cos⁻¹`, `tan⁻¹`)
- **deg** key toggles between degrees and radians
- Running history line above the main display
- Hover effects on buttons

## Run it

Requires Python 3.8+ (tkinter ships with the standard Python installers).

```bash
git clone https://github.com/Hammad-Ahmed-hk/Scientific-Calculator..git
cd Scientific-Calculator.
python scientific_calculator.py
```

## Known limitations

- The **Converter** tab is visible in the UI but not implemented yet.
- All logic lives in a single file; splitting the UI from the calculation code would make it easier to test.

## Project structure

```
Scientific-Calculator./
├── scientific_calculator.py   # GUI and calculation logic
├── README.md
└── .gitignore
```

## Author

Hammad Ahmed, [@Hammad-Ahmed-hk](https://github.com/Hammad-Ahmed-hk)

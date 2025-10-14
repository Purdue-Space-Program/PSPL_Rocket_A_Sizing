# PSPL_Rocket_A_Sizing

Hi! Welcome to the PSPL's "Rocket A" sizing code. "Sizing" is the process of determining the optimal dimensions

The outputs of this code are not the word of god, they are a set of preliminary vehicle parameters that we can be confident will be near enough to a rocket we can actually build that might work.


## How to Run the Sizing Script (in VS code)

1. Clone the repository onto your computer (video on how to do it using [GitHub desktop](https://www.youtube.com/watch?v=CAwStH0ay-M) [click "Clone a Repository" instead of creating one at 0:43])
2. Open this folder in VS Code
3. Open an integrated terminal: <kbd>⌃ ⇧ `</kbd>
4. Run the following code in the terminal to activate a virtual environment (or don't). [Learn more about virtual environments](https://www.youtube.com/watch?v=KxvKCSwlUv8) 🙂
    1. ```python -m venv .venv```
    2. Choose next line based off your operating system:
        1. MacOS🍎:
           ```source .venv/bin/activate```
        4. Windows🪟:
           ```.venv\Scripts\activate.bat```

5. Run the below code in the terminal to import all required packages
```python -m pip install -r requirements.txt```

5. Change inputs in inputs.py
    1. Choose fuel
    2. Choose parameter's upper and lower boundaries and step size
6. Run main.py

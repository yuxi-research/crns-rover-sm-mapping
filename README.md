# crns-rover-sm-mapping
**Yuxi Zhang** · Nov 27, 2026 · [@yuxi-research](https://github.com/yuxi-research)
*The University of Sydney*



## Installation guide (for beginners)

### Install the required software

We recommend using Visual Studio Code (VS Code) to open and run this project.
Please download and install VS Code from: [VS Code download](https://code.visualstudio.com/download).


This project uses `uv` to manage Python and project dependencies. Please follow the installation instructions: [uv installation](https://docs.astral.sh/uv/#installation)

### Open project in VS Code

In VS Code, go to **File → Open Folder**, then open the root folder of this project.

In VS Code, click **Terminal → New Terminal** from the menu bar to open a terminal. The terminal's **working directory (WD)** should automatically be set to the root folder of this project.

In terminal, check if uv is correctly installed:
```sh
uv --version
```
If a version number is displayed, uv has been installed successfully.

### Install Python depedencies in a virtual environment

Enter the following command in terminal to install all required dependencies under the root folder of this project.
```sh
uv sync
```
* Troubleshooting: If the project does not run correctly, try:
  
    ```sh
    uv pip install -e .
    ```

## Activate the virtual enviornment
Activate the environment, by running

```
.venv/bin/activate  # For Linux/MacOS

.venv/Scripts/activate  # For Windows
```

## Run a test

Run the following command to verify that the environment and dependencies are correctly installed:
```bash
python tests/test_env.py
```
If everything is set up correctly, you should see:
```text
...
All tests passed successfully.
```
## Run the main pipeline

Copy the `example_data` folder to the root directory of this project. After copying, your project structure should look like this:

```text
crns-rover-sm-mapping/      # Root directory
├── example_data/           # Copy example_data here
├── main_pipeline.ipynb
├── notebooks_process/
├── src/
├── pyproject.toml
├── README.md
└── ...
```

Open `main_pipeline.ipynb`. In the top-right corner of the notebook, click **Select Kernel → Select Another Kernel**, then find and select the `crns-rover-sm-mapping` virtual environment created in the previous steps.

Click **Run All** in the top toolbar to run the entire notebook.



### AI-assisted development

Generative AI tools were used for code completion and suggestion. All generated suggestions were reviewed before use.
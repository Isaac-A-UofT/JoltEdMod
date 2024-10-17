# README

## Curriculum Module Generator

This project is a content generator that creates educational materials for a given topic using OpenAI's GPT model. The generator creates both Jupyter Notebook tutorials and Wiki-style markdown files based on user-defined parameters.

### Features

* Automatically generates content for a given topic

* Creates Jupyter Notebook tutorials and Wiki-style markdown files

* Customizable content creator identity, target audience, and more

### Prerequisites

* Python 3.9 or higher

* Poetry ([installation guide](https://pypi.org/project/poetry/))

* OpenAI user API key ([get one here](https://platform.openai.com/settings/profile?tab=api-keys))

* Jupyter Notebook (to view the generated tutorial)

### Installation

1. Clone this repository.

2. Install the required packages using poetry:

    ```
    poetry install
    ```

3. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key:

- **For macOS and Linux**:

    ```
    export OPENAI_API_KEY=<your_api_key>
    ```

- **For Windows PowerShell**:

    ```
    $env:OPENAI_API_KEY="<your_api_key>"
    ```

### Usage

1. To activate the virtual environment, run:

    ```
    poetry shell
    ```

    You can also run individual scripts or commands within the Poetry environment without activating it by using:

    ```
    poetry run python your_script.py
    ```

2. Run the script with the desired command-line arguments:

    ```
    curriculum_module_generator --topic <topic> [--identity <identity>] [--target_audience <target_audience>] [--tutorial_output_file <tutorial_output_file>] [--wiki_output_file <wiki_output_file>] [--model <model>]
    ```

Required arguments:

* --topic: The topic for the content

Optional arguments:

* --identity: The identity of the content creator (default: "Professor of Computer Science")

* --target_audience: The target audience for the content (default: "first year computer science students")

* --tutorial_output_file: Path to the tutorial output file (default: "output.ipynb")

* --wiki_output_file: Path to the wiki output file (default: "output.md")

* --model: The OpenAI GPT model to use for generating cell content (default: "gpt-3.5-turbo")
The generated content will be saved in the specified output files.

3. To exit poetry shell, enter the command:

    ```bash
    exit
    ```

### Contributing
Feel free to submit issues or pull requests to improve this project.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Citing in academic works

```
@misc{Laundry:currentdate,
  author = {Laundry, Nathan},
  year = {current date},
  title = {Curriculum\_module\_generator},
  version = {Current code version},
  howpublished = {Computer Program},
  url = {https://github.com/TheAcademicsFieldGuideToWritingCode/Tutorials-Generator}
}
```

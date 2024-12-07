# Mobile De Car Data Postprocessor

This project is a Python-based postprocessor for car data obtained from Mobile.de. It processes the extracted raw data strings into numbers and other proper formats that are faster and easier to query, filter and sort.

## Requirements

- Python 3.11
- Conda env

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/mobile-de-car-data-postprocessor.git
    ```
2. Navigate to the project directory:
    ```sh
    cd mobile-de-car-data-postprocessor
    ```
3. Install the required packages:
    ```sh
    conda env create -f environment.yml
    ```
4. Activate the new environment 
    ```sh
    conda activate <my_new_project_env>
    ```

## Usage

1. Place your mongodb connection string into environment variables
2. Run the postprocessor script:
    ```sh
    python string-to-number-postprocessor.py
    ```
3. The processed data will be created in a new collection called: listings-v2-postprocessed

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact / Author

For any questions or suggestions, please contact  **Robert Ciotoiu** - [robertciotoiu](https://github.com/robertciotoiu)

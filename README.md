# Bank Management System

The Bank Management System is a command-line application that allows users to perform various banking operations such as account management, transactions, and administrative tasks. It provides a user-friendly interface for customers and administrators to interact with the banking system.

## Features

1. **User Authentication**: Users can log in using their phone number and password. The system verifies the credentials and grants access to the user account.

2. **Account Management**: Users can create new bank accounts, check balances, withdraw money, deposit money, get a loan, and view transaction history.

3. **Card Management**: Users can request new credit or debit cards, view card details, and update the card PIN.

4. **Branch Information**: Users can retrieve branch details, including the branch name, city, state, and pin code.

5. **Administrative Tasks**: Administrators have additional functionalities, such as viewing transaction history across all accounts, adding new branches, and deactivating user accounts.

## Prerequisites

To run the Bank Management System, you need to have the following:

- Python 3.x: Make sure Python is installed on your system.
- MYSQL database

## Getting Started

1. Clone the repository or download the project files to your local machine.

2. Open a terminal or command prompt and navigate to the project directory.
3. Login to mysql and create the required tables using the `Tables.sql` script
  ``` 
  SOURCE Tables.sql
  ```
4. Populate the tables with sample data
  ```
  SOURCE sample_data.sql
  ```

4. Install the required dependencies by running the following command:

   ```
   pip install mysql-connector-python
   ```

5. Start the server by running the following command in a new terminal:

   ```
   python server.py
   ```

6. Open another terminal or command prompt and navigate to the project directory.

7. Run the client application by executing the following command:

   ```
   python client.py
   ```

8. Follow the prompts in the client application to interact with the Bank Management System.

## Usage

- **Login**: Enter your phone number and password to log in to your account. If the credentials are valid, you will be granted access to your account.

- **Account Operations**: Once logged in, you can perform various account operations, such as checking balance, withdrawing money, depositing money, getting a loan, and viewing transaction history.

- **Card Operations**: You can request new credit or debit cards, view card details, and update the card PIN.

- **Branch Information**: Retrieve branch details, including the branch name, city, state, and pin code.

- **Administrative Tasks**: Administrators have additional functionalities. They can view transaction history across all accounts, add new branches, and deactivate user accounts.

## Contributing

Contributions to the Bank Management System project are welcome. If you find any bugs, have feature requests, or want to contribute improvements or new functionalities, please create a pull request or open an issue in the project repository.

## License

The Bank Management System project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You can find more details in the [LICENSE](LICENSE) file.

## Disclaimer

The Bank Management System is a sample project and should not be used for real-world banking operations. It is provided as-is without any warranties or guarantees. Use it at your own risk.

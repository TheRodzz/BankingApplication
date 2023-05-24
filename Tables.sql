CREATE TABLE customer(
    fname VARCHAR(50),
    mname VARCHAR(50),
    ltname VARCHAR(50),
    phone_no CHAR(10) PRIMARY KEY,
    encrypted_password BINARY(32),
    dob DATE,
    isAdmin BOOLEAN
);

CREATE TABLE branch
   (
    bid INT PRIMARY KEY,
    bname VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    pincode CHAR(6)
   );

CREATE TABLE account(
    acc_no  CHAR(16) PRIMARY KEY,
    bid INT,
    phone_no CHAR(10),
    balance INT,
    isActive BOOLEAN,
    type CHAR(1),
    FOREIGN KEY (phone_no) REFERENCES customer(phone_no) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (bid) REFERENCES branch(bid) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE transaction(
    tid INT PRIMARY KEY,
    acc_no CHAR(16),
    type CHAR(1),
    amount INT,
    time TIMESTAMP,
    FOREIGN KEY (acc_no) REFERENCES account(acc_no) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE card(
    card_no CHAR(16) PRIMARY KEY,
    acc_no CHAR(16),
    card_type CHAR(1), 
    expiry_date DATE,
    pin CHAR(4),
    cvv CHAR(3),
    isActive BOOLEAN,
    FOREIGN KEY (acc_no) REFERENCES account(acc_no) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE loan(
    lid INT PRIMARY KEY,
    acc_no CHAR(16),
    amount INT,
    interest_rate INT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (acc_no) REFERENCES account(acc_no) ON UPDATE CASCADE ON DELETE SET NULL
);
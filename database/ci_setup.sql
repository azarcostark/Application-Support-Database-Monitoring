CREATE DATABASE IF NOT EXISTS application_support;

USE application_support;

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id)
);

CREATE TABLE orders (
    order_id INT NOT NULL AUTO_INCREMENT,
    customer_id INT NOT NULL,
    product VARCHAR(150) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_product (product),
    INDEX idx_status (status),
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE incidents (
    incident_id INT NOT NULL AUTO_INCREMENT,
    severity VARCHAR(20) NOT NULL,
    area VARCHAR(50) NOT NULL,
    root_cause VARCHAR(255) NOT NULL,
    recommended_action VARCHAR(500) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    PRIMARY KEY (incident_id)
);

INSERT INTO customers (name, email)
VALUES
    ('John Smith', 'john.smith@example.com'),
    ('Jane Doe', 'jane.doe@example.com'),
    ('Michael Brown', 'michael.brown@example.com'),
    ('Sarah Wilson', 'sarah.wilson@example.com'),
    ('David Miller', 'david.miller@example.com');

INSERT INTO orders (
    customer_id,
    product,
    amount,
    status
)
SELECT
    CASE
        WHEN n <= 20 THEN 1
        WHEN n <= 40 THEN 2
        WHEN n <= 60 THEN 3
        ELSE 4
    END,
    CONCAT('Product ', n),
    10.00 + n,
    'PENDING'
FROM (
    SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
    SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL
    SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL
    SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL
    SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL
    SELECT 19 UNION ALL SELECT 20 UNION ALL SELECT 21 UNION ALL
    SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 UNION ALL
    SELECT 25 UNION ALL SELECT 26 UNION ALL SELECT 27 UNION ALL
    SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30 UNION ALL
    SELECT 31 UNION ALL SELECT 32 UNION ALL SELECT 33 UNION ALL
    SELECT 34 UNION ALL SELECT 35 UNION ALL SELECT 36 UNION ALL
    SELECT 37 UNION ALL SELECT 38 UNION ALL SELECT 39 UNION ALL
    SELECT 40 UNION ALL SELECT 41 UNION ALL SELECT 42 UNION ALL
    SELECT 43 UNION ALL SELECT 44 UNION ALL SELECT 45 UNION ALL
    SELECT 46 UNION ALL SELECT 47 UNION ALL SELECT 48 UNION ALL
    SELECT 49 UNION ALL SELECT 50 UNION ALL SELECT 51 UNION ALL
    SELECT 52 UNION ALL SELECT 53 UNION ALL SELECT 54 UNION ALL
    SELECT 55 UNION ALL SELECT 56 UNION ALL SELECT 57 UNION ALL
    SELECT 58 UNION ALL SELECT 59 UNION ALL SELECT 60 UNION ALL
    SELECT 61 UNION ALL SELECT 62 UNION ALL SELECT 63 UNION ALL
    SELECT 64 UNION ALL SELECT 65 UNION ALL SELECT 66 UNION ALL
    SELECT 67 UNION ALL SELECT 68 UNION ALL SELECT 69 UNION ALL
    SELECT 70
) AS numbers;

INSERT INTO orders (
    customer_id,
    product,
    amount,
    status
)
VALUES
    (1, 'Completed Product 1', 125.00, 'COMPLETED'),
    (2, 'Completed Product 2', 225.00, 'COMPLETED'),
    (3, 'Cancelled Product', 75.00, 'CANCELLED');

INSERT INTO incidents (
    severity,
    area,
    root_cause,
    recommended_action,
    status
)
VALUES
    (
        'CRITICAL',
        'DATABASE',
        'Database connection failure.',
        'Check MySQL service and database connectivity.',
        'OPEN'
    ),
    (
        'CRITICAL',
        'DATABASE',
        'Database query timeout.',
        'Review database performance and slow queries.',
        'OPEN'
    ),
    (
        'CRITICAL',
        'APPLICATION',
        'API health check failed.',
        'Review application logs and failed API endpoint.',
        'OPEN'
    ),
    (
        'WARNING',
        'APPLICATION',
        'API response time exceeded threshold.',
        'Review API and database performance.',
        'OPEN'
    ),
    (
        'WARNING',
        'TEST',
        'Automated test execution warning.',
        'Review test execution logs.',
        'OPEN'
    ),
    (
        'CRITICAL',
        'DATABASE',
        'Previous database connection failure.',
        'Database connectivity was restored.',
        'RESOLVED'
    ),
    (
        'WARNING',
        'APPLICATION',
        'Previous API performance issue.',
        'API performance issue was resolved.',
        'RESOLVED'
    ),
    (
        'WARNING',
        'TEST',
        'Previous test execution warning.',
        'Test execution returned to normal.',
        'RESOLVED'
    ),
    (
        'CRITICAL',
        'APPLICATION',
        'Previous API failure.',
        'Application API was restored.',
        'RESOLVED'
    ),
    (
        'CRITICAL',
        'TEST',
        'Previous test infrastructure failure.',
        'Test infrastructure was restored.',
        'RESOLVED'
    );

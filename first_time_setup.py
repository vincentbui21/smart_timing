import os

MYSQL_USER = "admin"
MYSQL_PASSWORD = "123"
MYSQL_DATABASE = "std"
MYSQL_ROOT_PASSWORD = "admin"  # Change this if needed


def install_mysql():
    """Installs MySQL Server & Client (for Raspberry Pi)"""
    print("🚀 Installing MySQL Server & Client...")
    os.system("sudo apt update && sudo apt install -y mysql-server mysql-client")
    os.system("sudo systemctl start mysql && sudo systemctl enable mysql")
    print("✅ MySQL installation complete!")


def setup_mysql():
    """Sets up MySQL: root password, database, and user 'admin'."""
    print("🔧 Setting up MySQL database and user...")

    setup_commands = f"""
    sudo mysql -u root -e "
    SET PASSWORD FOR 'root'@'localhost' = PASSWORD('{MYSQL_ROOT_PASSWORD}');
    FLUSH PRIVILEGES;

    -- Create database if not exists
    CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE};

    -- Create user 'admin' if not exists
    CREATE USER IF NOT EXISTS '{MYSQL_USER}'@'localhost' IDENTIFIED BY '{MYSQL_PASSWORD}';
    GRANT ALL PRIVILEGES ON {MYSQL_DATABASE}.* TO '{MYSQL_USER}'@'localhost';
    FLUSH PRIVILEGES;
    "
    """
    os.system(setup_commands)
    print("✅ MySQL database and user setup complete!")


def setup_tables():
    """Creates tables and inserts initial data"""
    print("📦 Setting up tables and inserting data...")

    table_commands = f"""
    mysql -u {MYSQL_USER} -p{MYSQL_PASSWORD} -e "
    USE {MYSQL_DATABASE};

    -- Create runners table
    CREATE TABLE IF NOT EXISTS runners (
        id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );

    -- Create timestamphistory table
    CREATE TABLE IF NOT EXISTS timestamphistory (
        timestamp VARCHAR(255) NOT NULL,
        runner_id INT,
        FOREIGN KEY (runner_id) REFERENCES runners(id) ON DELETE CASCADE
    );

    -- Insert runners (ignore if already exists)
    INSERT IGNORE INTO runners (id, name) VALUES
        (101, 'ERIC'),
        (102, 'VINCENT'),
        (103, 'NIKO'),
        (104, 'MARKKU'),
        (105, 'TEEMU');

    -- Insert timestamp history (ignore if already exists)
    INSERT IGNORE INTO timestamphistory (timestamp, runner_id) VALUES
        ('00:01:20:15', 101),
        ('00:05:45:30', 102),
        ('00:10:10:45', 103),
        ('00:15:30:50', 104),
        ('00:20:40:55', 105);
    "
    """
    os.system(table_commands)
    print("✅ Tables and initial data setup complete!")


def main():
    """Runs the full setup process"""
    install_mysql()
    setup_mysql()
    setup_tables()
    print("🚀 First-time setup complete! MySQL is ready to use.")


if __name__ == "__main__":
    main()

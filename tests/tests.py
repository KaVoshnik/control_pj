import pytest
import psycopg2

# Test database connection parameters
TEST_DBNAME = "notes_db"
TEST_USER = "postgres"
TEST_PASSWORD = "496284"
TEST_HOST = "127.0.0.1"

# Fixture to set up the database
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    # Connect to the test database
    conn = psycopg2.connect(
        dbname=TEST_DBNAME,
        user=TEST_USER,
        password=TEST_PASSWORD,
        host=TEST_HOST
    )
    cursor = conn.cursor()
    
    # Create the notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL
    )
    """)
    conn.commit()

    # Clear the notes table to ensure a clean state
    cursor.execute("TRUNCATE TABLE notes")
    conn.commit()

    yield cursor  # This will be the cursor for the tests

    # Teardown: drop the table after tests
    cursor.execute("DROP TABLE IF EXISTS notes")
    conn.commit()
    cursor.close()
    conn.close()

# Test creating a note
def test_create_note(setup_database):
    cursor = setup_database
    cursor.execute("INSERT INTO notes (content) VALUES (%s)", ("Test note",))
    cursor.connection.commit()

    cursor.execute("SELECT * FROM notes WHERE content = %s", ("Test note",))
    note = cursor.fetchone()
    assert note is not None
    assert note[1] == "Test note"

# Test saving a note
def test_save_note(setup_database):
    cursor = setup_database
    cursor.execute("INSERT INTO notes (content) VALUES (%s)", ("Another test note",))
    cursor.connection.commit()

    cursor.execute("SELECT * FROM notes WHERE content = %s", ("Another test note",))
    note = cursor.fetchone()
    assert note is not None
    assert note[1] == "Another test note"

    # Update the note
    cursor.execute("UPDATE notes SET content = %s WHERE id = %s", ("Updated note", note[0]))
    cursor.connection.commit()

    cursor.execute("SELECT * FROM notes WHERE id = %s", (note[0],))
    updated_note = cursor.fetchone()
    assert updated_note[1] == "Updated note"

# Test loading notes
def test_load_notes(setup_database):
    cursor = setup_database
    cursor.execute("INSERT INTO notes (content) VALUES (%s)", ("Load this note",))
    cursor.connection.commit()

    cursor.execute("SELECT * FROM notes ORDER BY id ASC")
    notes = cursor.fetchall()
    assert len(notes) > 0
    assert notes[0][1] == "Load this note"

# Test deleting a note
def test_delete_note(setup_database):
    cursor = setup_database
    cursor.execute("INSERT INTO notes (content) VALUES (%s)", ("Delete this note",))
    cursor.connection.commit()

    cursor.execute("SELECT * FROM notes WHERE content = %s", ("Delete this note",))
    note = cursor.fetchone()
    assert note is not None

    cursor.execute("DELETE FROM notes WHERE id = %s", (note[0],))
    cursor.connection.commit()

    cursor.execute("SELECT * FROM notes WHERE id = %s", (note[0],))
    deleted_note = cursor.fetchone()
    assert deleted_note is None

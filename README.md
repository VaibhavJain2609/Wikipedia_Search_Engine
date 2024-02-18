## Wikipedia Search Engine

A project that searches through a SQL database consisting of Wikipedia pages as the core dataset.

**Features:**

* Search through a core dataset of Wikipedia pages
* Retrieve information efficiently from Wikipedia pages stored in the dataset.

## Getting Started

### Prerequisites

* Python 3.8 or later
* Sqlite3

### Installation

1. Clone the project repository:
```bash
cd wikipedia-search-engine
git clone https://<URL github repository>
```
2. Navigate to the project directory:
```bash
cd wikipedia-search-engine
```
3. Create a virtual environment:
```bash
python3 -m venv env
source env/bin/activate
```
4. Install the required dependencies:
```bash
pip install -r requirements.txt
```
5. Install the project in editable mode:
```bash
pip install -e search_server
pip install -e index_server
```

### Running the Code



1. Start the indexing service:
```bash
./bin/index start
```
2. Run the search server:
```bash
flask --app search run --host 0.0.0.0 --port 8000
```
3. Open http://localhost:8000/ in your web browser to access the search interface.


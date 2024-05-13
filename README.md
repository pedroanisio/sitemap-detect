# Sitemap Detector API

The Sitemap Detector API is a Python Flask application designed to detect sitemap URLs from a given website URL using multiple detection strategies. This API can be particularly useful for SEO purposes, allowing users to quickly find sitemap files referenced in either the robots.txt file or embedded within HTML pages.

## Features

- Detection of sitemap URLs from `robots.txt`.
- Detection of commonly named sitemap XML files.
- Detection of sitemap URLs embedded in HTML via `<link>` tags.

## Requirements

Ensure that you have Python 3.8+ installed on your system. You can install all necessary Python packages using the provided `requirements.txt`.

## Installation

1. Clone the repository to your local machine:

```
git clone https://github.com/pedroanisio/sitemap-detect.git
```

2. Navigate to the project directory:

```
cd sitemap-detect
```

3. Install the required Python libraries:

```
pip install -r requirements.txt
```

## Usage

To start the server, run:

```
python src/main.py
```

This will host the API on `http://localhost:5000`.

### API Endpoint

#### GET `/detect_sitemap`

Parameters:
- `url` (required): The URL of the website to detect sitemaps from.

Example request:

```
curl http://localhost:5000/detect_sitemap?url=http://example.com
```

Response format:

```json
{
  "url": "http://example.com",
  "sitemaps": [
    "http://example.com/sitemap.xml",
    "http://example.com/sitemap_index.xml"
  ]
}
```

## Directory Structure

- 📄 🌟 `Dockerfile`: Dockerfile for containerizing the application.
- 📄 🌟 `requirements.txt`: List of packages required to run the application.
- 📁 `src`: Source files for the application.
  - 📄 `main.py`: Main application script.

## Docker Support

A Dockerfile is provided for building a containerized version of the application.

To build and run the Docker container, use:

```
docker build -t sitemap-detector:1.0 .
docker run -p 5000:5000 sitemap-detector
```

## License

Specify your license or leave this empty if you wish to adopt a default license such as MIT.

## Contributing

Contributions to the Sitemap Detector API are welcome. Please feel free to fork the repository and submit pull requests.

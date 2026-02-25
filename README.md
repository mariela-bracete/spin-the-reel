Spin The Reel is a hybrid movie recommendation system using ALS for collaborative signals and TF-IDF/FAISS for content-based similarity. It  consists of an ETL pipeline, model training and output generation using PySpark for implementation at scale, and a Flask demo app.

## What does it do?
⁃ Ingests MovieLens ratings and TMDB metadata from CSV files  
⁃ Performs data cleaning and transformation, including handling missing values, dropping unused columns, and preparing modeling-ready datasets  
⁃ Persists cleaned ratings data to PostgreSQL and movie metadata to MongoDB (dual persistence)  
⁃ Trains a hybrid recommendation system that combines:
⁃ Collaborative filtering using PySpark ALS, trained on user–movie ratings sourced from PostgreSQL via JDBC  
⁃ Content-based similarity derived from TMDB metadata using TF-IDF, dimensionality reduction, and FAISS for efficient similarity search  
⁃ Generates Top-N movie recommendations and saves results as Parquet artifacts 
⁃ Serves recommendations through a Flask web application, enriching outputs with TMDB metadata for human-readable results  

## Tech Stack
- Python (see requirements.txt for full list of packages)  
⁃ PostgreSQL: storage of preprocessed ratings data and source for Spark-based ALS training  
⁃ MongoDB: storage of movie metadata and content features for flexible document-based access  
⁃ Apache Spark (PySpark): scalable training of the collaborative filtering component (ALS) via JDBC  
⁃ FAISS: efficient similarity search over content-based movie representations  
⁃ scikit-learn: TF-IDF vectorization and dimensionality reduction for metadata-based similarity  
⁃ Flask: lightweight web application for serving recommendations  

## Pipeline Overview
- Extract and clean MovieLens ratings and TMDB metadata  
- Load ratings data into PostgreSQL and metadata into MongoDB  
- Train collaborative filtering model using PySpark ALS, consuming ratings data from PostgreSQL via JDBC  
- Build content-based similarity representations from TMDB metadata using TF-IDF and FAISS  
- Combine collaborative and content-based signals to generate hybrid Top-N recommendations  
- Precompute recommendation outputs and store as parquet artifacts  
- Serve recommendations via Flask using precomputed results  

## Project Structure
	```text	
	spin-the-reel/
	├── app/
	│   ├── app.py
	│   ├── routes.py
	│   ├── recommender.py
	│   └── templates/
	│       ├── index.html
	│       ├── mongo.html
	│       └── postgres.html
	├── notebooks/
	│   └── SpinTheReel_vF_Final.ipynb
	├── data/
	│   ├── ratings.csv
	│   └── TMDB_movie_dataset_v11.csv
	├── artifacts/
	│   └── precomputed_recs.parquet
	├── requirements.txt
	└── .gitignore
	```

## Prerequisites
- Large datasets and generated artifacts are not included in this repository due to GitHub size limitations. 
- To reproduce results, download MovieLens ratings dataset and TMDB movie metadata dataset.
- Place them in a local `data/` directory before running the notebook.

## How to Run
1. Run `SpinTheReel_vF_Final.ipynb` to:
	- clean the data
	- load datasets into PostgreSQL (ratings) and MongoDB (metadata)
	- train the collaborative filtering model (PySpark ALS)
	- build the content-based similarity component (TF-IDF + FAISS, in-memory)
	- generate hybrid Top-N recommendations and save precomputed outputs (Parquet)
2. From the project root, start the Flask app:
	```bash
	python app/app.py
	```
3. Open a browser and navigate to:
	- http://127.0.0.1:5000/
	- http://127.0.0.1:5000/mongo
	- http://127.0.0.1:5000/postgres

## Application Structure
- app.py: Entry point for the Flask application; initializes the app and starts the server
- routes.py: Defines application routes and handles user requests, invoking recommendation logic as needed
- recommender.py: Contains the core recommendation logic, including hybrid collaborative (ALS) and content-based (FAISS) components
- templates/: HTML templates used by Flask to render the UI

## Notes / Limitations
- Known Issue: Spark ingestion from PostgreSQL may require JDBC tuning depending on environment configuration  
- The collaborative and content-based components are trained separately and combined at recommendation time, rather than via a single joint model 
- The default demo workflow serves recommendations from precomputed Parquet artifacts for improved performance and reproducibility
- Datasets and generated artifacts are excluded due to GitHub file size limits.
- The FAISS index and Parquet recommendation outputs are generated locally and are not version-controlled.
- Run the notebook to regenerate all required artifacts before starting the Flask app.
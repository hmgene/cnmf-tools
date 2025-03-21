curl -X 'POST' 'http://localhost:8000/upload/' \
  -H 'Content-Type: application/json' \
  -d '{
    "chunk_number": 0,
    "total_chunks": 2,
    "file_id": "myfile.csv",
    "csv_data": [
     {"0": 1.5, "2": 2.3},{"0": 3.0, "1": 4.1}
    ]
  }'

curl -X 'GET' 'http://localhost:8000/get_spectra' \
  -H 'Content-Type: application/json'

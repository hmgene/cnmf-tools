FILE="data/sample.csv"
CHUNK_SIZE=100 # lines
FILE_ID="myfile123"
HEADER=$( head -n 1 $FILE )
out=chunks/sample_chunk_
rm $out*
split -l $CHUNK_SIZE -d "$FILE" $out



TOTAL_CHUNKS=$(ls $out* | wc -l)

for i in $(seq 0 $(($TOTAL_CHUNKS - 1))); do
  CHUNK_FILE=$(printf "%s%02d" $out $i)
  echo -e "$HEADER\n$(cat $CHUNK_FILE)" > $CHUNK_FILE
  echo "Uploading chunk $i..."

  curl -X POST "http://localhost:8000/upload/" \
    -F "file=@$CHUNK_FILE" \
    -F "chunk_number=$i" \
    -F "total_chunks=$TOTAL_CHUNKS" \
    -F "file_id=$FILE_ID"

  echo "Chunk $i uploaded."
done

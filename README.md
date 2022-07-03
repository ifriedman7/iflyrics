# iflyrics

## A Python script and webapp to search lyrics using the Musixmatch API
	
To run the script, add your search text as command line arguments:
	
	python3 query.py Pass the tanning butter
	
The result will be written to tracks.csv
### -------------
To build the image:
	
	docker image build -t iflyrics .
	
To run the container:
	
	docker run -p 3001:3001 -d iflyrics
	
Browse to the Web page on port 3001

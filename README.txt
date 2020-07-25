-----------------------------------------------------------------------------------------------------------------------
API:

For GET request:
curl -i -X GET http://hostname/api/<str:hash_name>/
where <hash_name> is required file hash, returns HTTP 404 if nothing found

For POST request:
curl -i -X POST -H "Content-Type:multipart/form-data" -F "file=@filepath" http://hostname/api/
where <filepath> is the path for your file, if instance already exists it's immediately returned to the front
with 201 code and JSON with "name" value, if not - it's created and the same result is returned. Files are saved
in the directory specified in setting

For DELETE request:
curl -i -X DELETE http://hostname/api/<str:hash_name>/
where <hash_name> is required file hash, returns HTTP 404 if such instance doesn't exists, if it does - deletes
the file from drive and then the model instance

-----------------------------------------------------------------------------------------------------------------------
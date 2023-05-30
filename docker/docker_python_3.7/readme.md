# step 1

{name} testing

`docker build -t testing-image .`

# step 2

`docker run --name testing-container -p 80:80 -v $(pwd):/code testing-image`

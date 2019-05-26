## photo-processor

The POST json format for `/photos/process` -

`{
	"uuid" : ["c43c85f0-f9b4-46f8-933f-3beb351fe024", "905523ec-ae8b-4ece-891a-9448a52882b5", "5d61afcc-779f-4448-9125-c8d48d42e55f", "eda5241b-f932-4025-84b5-7eabd4ede753", "3e0296d1-5ee1-41dd-8c34-58755740d06d", "7eb98252-3e59-4e33-bb89-240c7fbfda04"]
}`

### Installation

Prerequisites:  
- Docker  
- Ability to run `make`.

Start the app:
- `make start`

Create or reset the db schema after booting the app:  
- `make db-schema`

Postgres PSQL can be accessed via:
- `make psql`

RabbitMQ management console can be accessed at:  
`http://localhost:15672/`  

Web app can be accessed at:  
`http://localhost:3000/`


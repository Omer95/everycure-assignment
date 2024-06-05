## EveryCure Programming Challenge: Submitted by Omer Farooq Ahmed

### 1. Instructions to run code
1. Please ensure that Docker and Postman are installed on your machine.
2. Clone the code to your local machine: git clone https://github.com/Omer95/everycure-assignment.git
3. The docker-compose yaml file contains configurations for two container services: the inference API server, and a postgres database. Run these service with:
`docker-compose up`
4. This will start the two container services. The Flask API server is listening on http://0.0.0.0:5000/api/v1/extract for post requests.
5. Open the Postman application and start a new POST request to host: http://0.0.0.0:5000/api/v1/extract . Click Body, and add one PDF test file with key 'file' to the form-data. Click Send.
6. After a while, you will receive a JSON response of a list of entity objects with entity name, start and end indexes, and entity context.
7. You can view logs in the following logfile: data/app.log
8. You can view the NER results for each uploaded file in the data directory as well. This is a volume bound to the server container service.
9. You can also log into the postgres database to query the inference table that contains records for each inference made:
`docker-compose exec db psql -U postgres`
`\c postgres`
`select * from inference;`
10. Once you've tested all files, please shut down the containers:
`docker-compose down`

### Review Questions

1. Technical Choices: What influenced your decision on the specific tools and models used?
I wanted to create a self contained environment that could run the inference API on any machine. Containerzation was the natural choice. Given more time, I would deploy the flask API and database on a K8s cluster to ensure scalability, load balancing and fault tolerance. I used the huggingface transformers library as I can do inference on a large number of NER models with just a few lines of code. The d4data biomedical NER had the most entities recognized among the few models I researched, however, I can easily change the model in the config file and the code should run as it is on the new model. I used pdfminer to parse the PDF documents as there was good documentation on getting started with the API fast. Finally, I wanted to add a database to ensure we record each inference for reproducibility. The database is very simple to show proof of concept, but can be extended to include more information such as the user that sent the http request, specifc model hyperparameters, basically a precursor to an experiments tracking system. I used the postgres database as I had the init files ready from a previous project.

2. Entity Contextualization: How did you approach the problem of providing context for each identified entity?
I used a manual method of simply looking behind and ahead of the entity by a certain context stride and getting a substring of the text around the recognized entity from the original pdf text. I can imporve this by either fine tuning a model to include context as output, or using other models that contain this information. The Azure Text Analytics for Health does include similar contextual information, though not in the exact same format as was required in this assingment.

3. Error Handling: Can you describe how your API handles potential errors?
The API handles the errors defined in the openAPI spec. It checks if multiple files have been uploaded and returns a server error to upload a single file. There is basic valdiation for the PDF file extension, and error handling for if no file is attached or the file key is not 'file'. With more time, I would have included file size validation and uploaded large files in chunks and appended them to a file on disk rather than keep them in memory.

4. Challenges and Learnings: What were the top challenges faced, and what did you learn from them?
The biggest challenge was to get everything working on time. Connecting many different components of a software system can lead to a lot of time wasted thinking about business logic. I tried to use tools and approaches I'm familiar with and refer to official documentation to resove issues. I faced challenges with docker networking in order to make both services talk to each other and since I haven't used docker-compose in a while, this meant reading the official docs again. Fortunately, I resolved it quickly with 'links' and 'depends_on' keys in the yaml file. It was also a challenge to parse the PDFs in a readable format. Using regular expressions is never easy but I was able to refer to some blogs that detailed how they extract text from different elements on a PDF and replace stray new lines and other non alphanumeric characters to extract the appropriate text. I applied the hackathon mindset of trying a tool, and making an educated guess on how long it will take to configure, and then going for something else that's faster. I initially wanted to make a cloud native application but soon realized that configuring cloud services will take longer, compared to a local docker container.

5. Improvement Propositions: Given more time, what improvements or additional features would you consider adding?
With more time, I would make the following changes: use a managed K8s service such as EKS on AWS to deploy the API server as a pod. This would allow fault tolerance through replication, load balancing for large volume of requests and a simple interface for deployment. I would use a managed database/data warehouse on AWS such as Redshift to store one big table with inference metadata and the results stored as a large struct. This would make the database scalable and allow fast querying through EMR. It would mean I wouldn't need to persist the results separately. I would configure a VPC endpoint to expose my REST API to specific users as well. I would also experiment with more PDF OCR models to see which ones produce the best text output, rather than using a single python library and manually arranging text elements. Finally, I would also create a basic front end for end users to seamlessly upload their files for inference. It would be a good idea to deploy the front end pod to the same K8s cluster and leverage the same VPC for security and isolation. 
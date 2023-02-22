# Sensitive Personal Document Management System

## General Descriptions and Expectations
- In the loan application process, several sensitive personal documents need to be scanned (e.g. drivers license, last 2 pay stubs, etc.) Many time these documents are required by different organizations within a large company. By creating a sensitive personal document management system to store these sensitive documents, a customer only needs to scan the required documents one time. Other interested internal organizations can then query the system to gain the sensitive personal information required. This speeds up the time to gain access to information already available. It also avoids the duplicate effort of scanning document multiple times; a customer dissatisfier.

- The system should have the following features:

  · Secure login

    · Upload and store files

    · Extract data from scanned images (PDF, png, gif, etc.)

    § There are many OCR solutions

    · Confirm/edit data prior to storage

    · Store extracted data and original images

    · REST API to securely query system and return data and original image

    &nbsp;

    &nbsp;


# High-level System Design Pattern
## Frontend (React):
The frontend of the system will be built using React. It will consist of a login page, an upload page, and a search page.

1. Login page: Users will be able to log in to the system using a secure login page.

2. Upload page: Once logged in, users will be able to upload scanned images of sensitive personal documents. The uploaded documents will be saved to a separate file storage system, such as Amazon S3 or Google Cloud Storage, and the metadata (such as the file path or URL) will be saved to the backend.

3. Search page: Internal organizations will be able to search for the uploaded documents by entering the necessary criteria. The backend will then return the metadata, which can be used to retrieve the original image from the file storage system.

## Backend (Django):
The backend will handle the storage and retrieval of documents and their associated data. The backend will use Django to create the REST API that the frontend will communicate with. The backend API will provide secure access to the system for internal organizations to query and retrieve documents. It will handle requests from the frontend and return the metadata and original images.

The backend will consist of several components, including:

1. Authentication system: This system will handle user authentication and authorization, ensuring that only authorized users can access sensitive documents.

2. Document storage system: This system will store the documents and their associated data in a secure manner, with encryption and access controls in place to protect sensitive data.

3. OCR system: This system will use an OCR solution to extract data from scanned images and store it in the system. The system will also allow users to edit the extracted data before storing it.

4. Search system: This system will allow users to search for documents based on various criteria, such as name, document type, and date.

## Database (PostgreSQL):
The database of the system will be built using PostgreSQL. 

1. API: The backend API will provide secure access to the system for internal organizations to query and retrieve documents. It will handle requests from the frontend and return the metadata and original images.

2. Database: The metadata of uploaded documents will be stored in a PostgreSQL database. The database will contain information such as the file path or URL, the user who uploaded the document, and any extracted data from the scanned images.

3. File storage system: The original scanned images will be stored in a separate file storage system, such as Amazon S3 or Google Cloud Storage. The metadata saved in the database will include the file path or URL needed to retrieve the original image.

Overall, this system will provide a secure and efficient way to manage sensitive personal documents during the loan application process, while also avoiding the duplicate effort of scanning documents multiple times.

&nbsp;

&nbsp;
# Tech Stack Selection
## Frontend
There are many frontend frameworks and libraries available for building user interfaces, each with their own strengths and weaknesses. Here are some factors to consider when choosing a frontend framework for the sensitive personal document management system:

1. Ease of Use:
   One of the key factors to consider when choosing a frontend framework is how easy it is to use and learn. Ideally, you want a framework that allows you to quickly and easily build user interfaces without requiring extensive knowledge of web development.

2. Performance:
   Performance is another important factor to consider when choosing a frontend framework. You want a framework that is fast and responsive, with minimal overhead and a small footprint.

3. Cross-Platform Support:
   The sensitive personal document management system will likely be used on a variety of devices and platforms, so it's important to choose a frontend framework that provides cross-platform support, including desktop and mobile devices.

4. Community Support:
   A large and active community can provide valuable resources and support for developers, including tutorials, documentation, and open-source components. Choosing a framework with a strong community can help ensure that you have access to the resources you need to build and maintain the system.
   
Based on these factors, some popular frontend frameworks for building user interfaces include:

React: React is a popular and widely used library for building user interfaces, with a focus on performance and ease of use. It has a large and active community, and is well-suited for building complex and dynamic user interfaces.

Angular: Angular is a powerful and comprehensive framework for building web applications, with a focus on performance, scalability, and cross-platform support. It has a steep learning curve, but provides a powerful set of tools and features for building complex web applications.

Vue.js: Vue.js is a lightweight and flexible framework for building user interfaces, with a focus on ease of use and performance. It has a small footprint and is well-suited for building small to medium-sized applications.

Ultimately, we choose the React.js among these since we are more familiar with this Framework.


&nbsp;

## Backend
We are going to use Python as our backend programming language. Both Flask and Django are popular web frameworks for building web applications in Python, and each has its own strengths and weaknesses. Here are some factors to consider when choosing between Flask and Django for the sensitive personal document management system:

1. Scalability: Scalability is an important consideration for any web application, particularly if the system is expected to handle large amounts of traffic or data. 
   - Django is well-suited for large, complex applications that require high scalability, with built-in support for features such as caching, database partitioning, and load balancing. 
  
   - Flask, on the other hand, is more lightweight and less opinionated, which can make it easier to scale for smaller applications but may require more effort to scale for larger applications.

2. Built-in Features:
   - Django includes a wide range of built-in features and modules, including an ORM for database access, an admin interface, and built-in user authentication. These features can make it easier to develop and maintain a web application, particularly for developers who are new to web development.

   - Flask, on the other hand, is more minimalist and provides less out-of-the-box functionality, which can make it more flexible but may require more development effort to build certain features.

3. Ease of Use: Ease of use is an important consideration for any web framework, particularly for developers who are new to web development. 
   - Django is a comprehensive framework with many built-in features, which can make it easier for developers to get started and build a web application quickly. 
   
   - Flask is more minimalist and flexible, which can make it more challenging for new developers to get started but can also provide greater flexibility and control over the application.

Based on these factors, Django may be a better choice for the sensitive personal document management system, particularly if scalability and built-in features are important.

&nbsp;
## Database
Both PostgreSQL and MySQL are popular SQL databases that are widely used in web applications. Here are some pros and cons of each database in the context of the sensitive personal document management system:

### PostgreSQL:

Pros:

- Strong data consistency: PostgreSQL is known for its strong data consistency and reliability, which makes it a good choice for applications that require accurate and consistent data.

- Advanced features: PostgreSQL has many advanced features, such as support for advanced data types, full-text search, and complex queries.

- Security: PostgreSQL has a strong focus on security and includes features such as row-level security and encryption to protect sensitive data.

Cons:

- Complexity: PostgreSQL can be more complex to set up and configure than MySQL, particularly for users who are not familiar with SQL databases.

- Resource-intensive: PostgreSQL can be more resource-intensive than MySQL, particularly when it comes to memory usage and disk I/O.

- Licensing: PostgreSQL is released under a more restrictive license than MySQL, which may affect its use in some environments.

### MySQL:

Pros:

- Ease of use: MySQL is known for its ease of use and is often preferred by developers who are new to SQL databases.

- Performance: MySQL can be faster than PostgreSQL in some scenarios, particularly when it comes to read-heavy workloads.

- Large user base: MySQL has a large user base and a mature ecosystem of tools and support, making it a good choice for developers who need to quickly find solutions to common problems.

Cons:

- Limited features: MySQL has fewer advanced features than PostgreSQL, particularly when it comes to complex queries and advanced data types.

- Security: MySQL has been criticized for its security in the past, although recent versions have improved in this area.

- Data consistency: MySQL's data consistency can be weaker than PostgreSQL in some scenarios, particularly when it comes to write-heavy workloads.

Based on these factors, PostgreSQL may be a better choice for the sensitive personal document management system, particularly if strong data consistency and advanced features are important.
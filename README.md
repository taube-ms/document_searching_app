# document_searching_app

This is the repo for my searching quates site.
I took both of my novals in hebrow and let OpenAI to read them and created a search engine.

The Process
1.	First step installs requirements.
1.	Reading the .docx file to string type in python.
1.	Split the string to a list of sections and cleaning it.
1.	Creating an index dictionary and translating the document using Azure Translate. 
1.	Creating an embedded matrix out of all the documentation using OpenAI ada2 model.
1.	Saving the matrix and the dictionary in Azure Blob Storage and downloading it back to the app.
1.	Converting the English text to an embedded numpy array and calculating the cosine vector and getting the max index or closes vector.
1.	Creating the app (I used streamlit but a simple flask app will work as well).

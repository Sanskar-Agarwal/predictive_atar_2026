# Use an official Python runtime as a parent image
FROM python:3.11.6

RUN apt-get update && apt-get install -y glpk-utils

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8026 available to the world outside this container
EXPOSE 8026

# Define environment variable
ENV NAME World

# On container start: apply migrations, load the reference data (regions,
# subjects, grade types, scaling/ATAR-conversion tables — no student records),
# then (re)load VIC/WA/TAS scaling from the source CSVs so that data is always
# current, then run the server.
CMD python3 manage.py migrate && \
    python3 manage.py loaddata fixtures/reference_data.json && \
    python3 manage.py load_scaling && \
    python3 manage.py runserver 0.0.0.0:8026

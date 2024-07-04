# Use the official Node.js image from the Docker Hub
FROM node:14 as node-build

# Create and set the working directory
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of your application code
COPY . .

# Use the official Python image from the Docker Hub
FROM python:3.9-slim as python-build

# Create and set the working directory
WORKDIR /usr/src/app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY --from=node-build /usr/src/app .

# Expose the port your app runs on
EXPOSE 8000

# Define the command to run your app
CMD ["npm", "run", "dev"]

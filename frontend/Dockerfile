# Node.js runtime for base image.
FROM node:20.13.1 AS build-stage

# Set working dir.
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker layer caching
COPY package.json package-lock.json ./

# Install dependencies.
RUN npm install

# Copy the rest of the app code.
COPY . .

# Build the react app.
RUN npm run build

# Expose the port for the nginx server.
EXPOSE 80

# Run the Next.js app in production mode
CMD ["npm", "start"]
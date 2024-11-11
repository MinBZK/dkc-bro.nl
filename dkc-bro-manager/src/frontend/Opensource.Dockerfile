FROM node:20-alpine

# Copy source code
COPY ./src/frontend ./src/frontend

# Install dependencies
RUN npm ci

# Expose port
EXPOSE 8080

# Start the application
CMD ["npm", "run", "serve"]
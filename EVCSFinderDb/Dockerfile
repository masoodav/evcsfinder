# Use MongoDB base image
FROM mongo:5.0

# Install additional tools
RUN apt-get update && apt-get install -y python3 python3-pip git && apt-get clean

# Set up working directory
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/openchargemap/ocm-export.git /app/ocm-export

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /app/requirements.txt

RUN chmod +x /app/scripts/docker-entrypoint.sh

# Expose MongoDB port
EXPOSE 27017

# Use the custom entrypoint
ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]

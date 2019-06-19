# Use latest python
FROM python:3.7

# Set the working directory to /BackEnd
RUN mkdir -p /home/coinArrival/BackEnd
WORKDIR /home/coinArrival/BackEnd

# Copy the current directory contents into the container at /BackEnd
COPY . /home/coinArrival/BackEnd

# Install any needed packages
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Make port 3000 available to the world outside this container
EXPOSE 8000

# Run repo when the container launches
CMD ["python", "./BackEnd/manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.11.5
RUN mkdir -p /usr/src/app
RUN mkdir -p ~/.credentials
WORKDIR /usr/src/app
COPY . /usr/src/app
COPY ./.credentials/credentials.json ~/.credentials/credentials.json
RUN pip install --upgrade pip
RUN python3 -m pip install --upgrade Scrapy --trusted-host pypi.org --trusted-host files.pythonhosted.org
RUN pip install --no-cache-dir -r requirements.txt
CMD ["/bin/bash", "/usr/src/app/run.sh"]
FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY ./app /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

RUN apt-get update
RUN apt-get install -y dirmngr apt-transport-https ca-certificates software-properties-common gnupg2

# add key and repo
RUN mkdir -p ~/.gnupg
RUN echo "disable-ipv6" >> ~/.gnupg/dirmngr.conf
RUN apt-key adv --homedir ~/.gnupg --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/debian stretch-cran35/'

RUN apt-get update
RUN apt-get install -y r-base
RUN apt-get install -y build-essential

RUN Rscript /app/install.r

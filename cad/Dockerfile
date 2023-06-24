FROM nikolaik/python-nodejs:python3.11-nodejs18 
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN npm install
CMD npm run dev

# Pledge4Future App

Pledge4Future is a project to help you and your working group to measure and reduce your work-related CO<sub>2</sub>e footprint. It helps you and everyone else to contribute protecting our climate and life on Earth.

The [pledge4future app](https://pledge4future.org) allows you to calculate your work related CO<sub>2</sub>e emissions from heating and electricity consumptions as well as business trips and commuting. The methodology for the calculation the emissions is implemented in the [co2calculator package](https://github.com/pledge4future/co2calculator).

### Installation

This is a dockerized app which uses React in the frontend and Python, Django and GraphQL in the backend.

### 1. Clone repository 

```
git clone 
cd WePledge
```

### 2. Load the submodules

```
git submodule update --init --recursive
```

### 3. Run docker

```
docker compose up
```

This will start the following services on your computer:

Frontend: [http://localhost:3000](http://localhost:3000)  
Backend: [http://localhost:8000](http://localhost:8000)  
Django Admin: [http://localhost:8000/admin](http://localhost:8000/admin)  
GraphQL API: [http://localhost:8000/graphql](http://localhost:8000/graphql)  

Refer to the [wiki](https://github.com/pledge4future/WePledge/wiki) for detailed instructions on how to run, adapt and debug the app.

## Contribution guidelines 

We're always happy about people contributing to our project. So if you encounter problems with the app, just create an issue in this repository. If you can fix it yourself, please create a new branch from 'dev', add your changes and once you're done create a pull request. 

If you would like to become a regular contributor to the project, please write an email to [info@pledge4future.org](mailto:info@pledge4future.org).

## License

This project is licensed under the [GPL-3.0 License](./LICENSE).

## Acknowledgments

We are supported by

- Goethe Institute
- HeiGIT gGmbH (Heidelberg Institute for Geoinformation Technology)
- GIScience Research Group, Institute of Geography at Heidelberg University
- Scientists4Future Heidelberg
- Max Planck Institute for Astronomy Heidelberg

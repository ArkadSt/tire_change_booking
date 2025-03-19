# Tire Change Booking

![Main page](https://imgur.com/a/eV4Jp3H)
![Booking page](https://imgur.com/a/41wU7ML)

The backend is built using **Django** and the frontend using **Vue.js**.

By default, the frontend expects the backend to run on **localhost**, port **8000**. This can be changed by editing `/frontend/src/store/slots.js`.

These are the steps to start the backend and frontend in non-production mode:

### Backend:
```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```

For running tests, please use the following [config file](https://raw.githubusercontent.com/ArkadSt/tire_change_booking/refs/heads/main/backend/workshops.yaml) (already there when you clone the repository) and make sure that [workshops](https://github.com/Surmus/tire-change-workshop) are running. Then go to the `backend` folder and run:
```bash
python3 manage.py test
```


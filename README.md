# [Sure-Bo: A Data-Driven Web Application to Detecting Online Job Scams](report.pdf)
## Get started
### Run using docker (Highly Recommended)
Run `./docker-start.sh` in project root dir <br>
Site will be available on http://127.0.0.1:8080

### Run locally
> It is recommended to run this project using python 3.8x

1. Download pretrained model [here](https://github.com/FishPain/sure-bo/releases/download/v0.1.0/{rf}.pkl) and save it under `src/models`<br>
2. ```pip install -r requirements.txt```<br>
3. Debug mode: ```python app.py```<br>
4. Prod mode: ```flask --app app run```
5. Site will be available on http://127.0.0.1:5001

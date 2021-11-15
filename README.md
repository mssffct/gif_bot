# give_me_gif_bot
Created with the help of the [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)    
Database provided by [MinIo](https://min.io/)    
Test it at: [@give_me_gif_bot](@give_me_gif_bot)
## installation:
#### Clone repository as usual
#### In order to create docker container with minio use:
`$ docker run -p 9000:9000 -p 9001:9001 --name minio1 -v specify_your_path_here -e "MINIO_ROOT_USER=your_user" -e "MINIO_ROOT_PASSWORD=ypur_pass"
  quay.io/minio/minio server /data --console-address ":9001"`
#### To build docker container with project and to connect it to minio use:
`$ docker-compose build`
#### Finally use:
`$ docker-compose up`
## getting started:
:rocket: main script-file will run automatically after the start of the container 
## usage: 
- To get started type in ***/start*** command
- Choose the option you want then Follow the instructions below
    - If your choise is addition the text to the picture:
        - Enter the text that you want in the input field 
        - Then choose the font you like
        - Finally add one picture and enjoy the result!
    - If you want to create your own gif:
        - Add more than two pictures (more - more interesting result)
        - Enjoy   
- For help type in ***/help*** command
- To recieve all the gifs that you ever created type in ***/get_gifs*** command

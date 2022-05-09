# flask_blog
A blog web application written in python using the Flask framework, following a series of tutorials by Corey Schafer, contained in the playlist bellow. Some implemented features are not discussed in the playlist, like the sidebar and the comment functionality.

![image](https://user-images.githubusercontent.com/26972046/167320996-9999b1ff-acb5-4e36-976a-13256bd229b5.png)

Test locally with Docker by running the following command in the project directory.
```
docker image build . -t flask_blog && docker run flask_blog:latest
```
Make sure to suply a secret key, a mail server, a mail username and a mail password in [config_template.json](config_template.json) before running the server.

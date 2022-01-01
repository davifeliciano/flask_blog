FROM python:3.9.6
RUN useradd -m user
USER user
COPY --chown=user:user . /home/user/flask_blog
COPY --chown=user:user ./config_template.json /etc/flask_blog_config.json
WORKDIR /home/user/flask_blog
ENV PATH="/home/user/.local/bin:${PATH}"
RUN pip install --upgrade pip setuptools
RUN pip install --user -r requirements.txt
EXPOSE 5000:5000
CMD ["python","app.py"]
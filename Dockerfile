FROM maguowei/python-app:onbuild

ENV APP_NAME today
ENV APP_ENV dev

USER app

VOLUME /var/lib/${APP_NAME}/data
WORKDIR ${APP_SOURCE_CODE_PATH}
CMD ["rss.py"]
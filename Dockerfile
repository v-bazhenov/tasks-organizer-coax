# Set python image version
ARG PYTHON_VERSION=3.8-alpine

# Setup Image for building packages
FROM python:${PYTHON_VERSION} as builder

# Add some additional dependencies for compiling some of our python modules
RUN apk add --no-cache \
            --upgrade \
            --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
        libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
        libxcb-dev libpng-dev libjpeg\
        alpine-sdk \
        postgresql-dev
WORKDIR /wheels

# install and compile py modules
#COPY ./Pipfile /wheels/
#COPY ./Pipfile.lock /wheels/
COPY ./requirements.txt /wheels/
RUN pip install -U pip \
        && pip wheel -r ./requirements.txt

# Setup Application Image
FROM python:${PYTHON_VERSION}

# Get modules from builder
COPY --from=builder /wheels /wheels
RUN pip install -U pip \
        && pip install -r /wheels/requirements.txt \
                       -f /wheels \
        && rm -rf /wheels \
        && rm -rf /root/.cache/pip/*

# Install additional packeges required by application
RUN apk add --no-cache \
            --upgrade \
    postgresql-libs \
    && rm -rf /var/cache/apk/*

# Copy Application Code inside Image
WORKDIR /code
COPY . /code

# Set Default values for environment variables
ENV DJANGO_ENV=development

# Run Application Server
ENTRYPOINT ["sh", "entrypoint.sh"]
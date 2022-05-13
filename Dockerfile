FROM debian:bullseye

RUN apt-get update && apt-get install -y python3 unzip opam python3-cairo python3-igraph python-is-python3 \
  && rm -rf /var/lib/apt/lists/*

RUN useradd user -g users --create-home
USER user
RUN opam init --yes --disable-sandboxing

COPY --chown=user:users eve-py /home/user/eve/eve-py
COPY --chown=user:users ply /home/user/eve/ply
RUN cd /home/user/eve/eve-py/ \
  && find /home/user/eve/eve-py -type f -name "*.sh" -print0 | xargs -0 chmod +x \
  && sed -i 's!opam install!opam install --yes!' config.sh \
  && ./config.sh

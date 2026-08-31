FROM debian:bullseye

RUN apt-get update && apt-get install -y python3 unzip opam python3-cairo curl bzip2 python-is-python3 \
  && rm -rf /var/lib/apt/lists/*

RUN useradd user -g users --create-home
USER user
RUN opam init --yes --disable-sandboxing

# EVE's LTL-to-automaton conversion is built on Spot, whose Python bindings
# (spot + buddy, see eve-py/environment-spot.yml) are not available as apt
# packages -- Miniforge/conda-forge is the supported way to get them (see
# README.md's "Recommended: Conda/Miniforge environment").
ENV MINIFORGE_HOME=/home/user/miniforge3
RUN curl -L -o /tmp/miniforge.sh \
      "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" \
  && bash /tmp/miniforge.sh -b -p $MINIFORGE_HOME \
  && rm /tmp/miniforge.sh
ENV PATH=$MINIFORGE_HOME/bin:$PATH

COPY --chown=user:users eve-py /home/user/eve/eve-py
COPY --chown=user:users ply /home/user/eve/ply
RUN cd /home/user/eve/eve-py/ \
  && find /home/user/eve/eve-py -type f -name "*.sh" -print0 | xargs -0 chmod +x \
  && sed -i 's!opam install!opam install --yes!' config.sh \
  && ./config.sh \
  && conda env create -f environment-spot.yml

WORKDIR /home/user/eve/eve-py/src
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "eve-spot", "python", "main.py"]

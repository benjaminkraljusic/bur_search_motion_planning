FROM ros:noetic-ros-base

SHELL ["/bin/bash", "-c"]
ARG WS_PATH="/ws"
ENV WS_PATH="${WS_PATH}"
 	
WORKDIR "${WS_PATH}"

# Setup Catkin workspace
ADD ./ "${WS_PATH}"/src/bur_search_motion_planning

# Install dependencies
RUN "${WS_PATH}"/src/bur_search_motion_planning/bur_search_utils/bash_scripts/pre-build.sh

# Build the workspace
RUN "${WS_PATH}"/src/bur_search_motion_planning/bur_search_utils/bash_scripts/build-ws.sh

# Prepare the environment
RUN "${WS_PATH}"/src/bur_search_motion_planning/bur_search_utils/bash_scripts/post-build.sh

ENTRYPOINT ls && source devel/setup.bash && exec /bin/bash

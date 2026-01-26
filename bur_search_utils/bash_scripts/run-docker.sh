sudo docker run -it \
                --device=/dev/dri \
                -e DISPLAY=$DISPLAY \
                -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
                --name bur_search_container bur_search_planning:latest
                

#!/bin/bash
while true
do
    cd ~/repos/why2/NUS-NCS_comp
    git fetch
    if [ -z "$(git diff origin/main)" ]; then
        echo "No changes in the remote repository."
    else
        echo "Changes detected, executing another script..."

        screen -S vite -X quit
        screen -S gradio -X quit

        git pull

        sleep 3
        screen -S vite -dm sh startVite.sh
        screen -S gradio -dm sh startGradio.sh

    fi

    sleep 10
done
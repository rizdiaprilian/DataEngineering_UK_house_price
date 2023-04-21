from prefect.infrastructure.docker import DockerContainer

# alternative to creating DockerContainer block in the UI
docker_block = DockerContainer(
    image="rizdi21/prefect:de_zoomcamp", # insert your image here
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save("docker-zoomcamp", overwrite=True)


docker_container_block = DockerContainer.load("docker-zoomcamp")
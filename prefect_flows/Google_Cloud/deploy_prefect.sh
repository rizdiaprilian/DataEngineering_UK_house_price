## Build deployment with parameter flows
prefect deployment build parameterized_flow.py:etl_parent_flow -n "Parameterized ETL"

## Apply deployment once it has been configured
prefect deployment apply etl_parent_flow-deployment.yaml

## Trigger deployment with "Quick run" and view it in UI.
## No agent picking up this runs, go to work queues 
## Specify an agent where we want this job to run 
## Start Agent
prefect agent start --pool default-agent-pool --work-queue default 


### Building docker
docker image build -t rizdi21/prefect:de_zoomcamp .

### Push to DockerHub
docker tag rizdi21/prefect:de_zoomcamp 21492rar/uk-house-price:deployment
docker push 21492rar/uk-house-price:deployment

### Register  docker image ro Prefect
python docker_deploy.py

### use a local Orion API server
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"

### use Prefect Cloud
prefect config set PREFECT_API_URL="http://api.prefect.cloud/api/accounts/[ACCOUNT-ID]/workspace"

### Start flow
prefect deployment run etl-parent-flow/Docker-flow -p "months=[10,11]"

### Fire up an agent
prefect agent start -q default



build:
	sam build --template  CloudFormation/dev_yaml/template-local.yaml
run:
	sam local start-api --template  CloudFormation/dev_yaml/template-local.yaml
update-dependencies:
	cd WebApp/backend/lib && zip -r python.zip python
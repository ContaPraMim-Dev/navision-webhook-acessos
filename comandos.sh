# Login
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 767397842961.dkr.ecr.us-east-2.amazonaws.com
# Build da imagem
docker build --platform linux/amd64 -t navision/webhooks-acessos --provenance=false .
# Tag da imagem
docker tag navision/webhooks-acessos:latest 767397842961.dkr.ecr.us-east-2.amazonaws.com/navision/webhooks-acessos:latest
# Push da imagem
docker push 767397842961.dkr.ecr.us-east-2.amazonaws.com/navision/webhooks-acessos:latest

function main_build() {
    # Build da imagem
    docker build --platform linux/amd64 -t navision/webhooks-acessos --provenance=false .
    # Tag da imagem
    docker tag navision/webhooks-acessos:latest 767397842961.dkr.ecr.us-east-2.amazonaws.com/navision/webhooks-acessos:latest
    # Push da imagem
    docker push 767397842961.dkr.ecr.us-east-2.amazonaws.com/navision/webhooks-acessos:latest
}

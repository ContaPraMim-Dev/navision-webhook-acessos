# Use a imagem base oficial do AWS Lambda para Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Defina o diretório de trabalho como /var/task (padrão para AWS Lambda)
WORKDIR /var/task

# Copie as dependências e instale no ambiente do Lambda
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Atualize o pip para a versão mais recente
RUN pip install --upgrade pip

# Copie o código da função Lambda
COPY main.py ${LAMBDA_TASK_ROOT}/main.py
COPY handlers ${LAMBDA_TASK_ROOT}/handlers

# Defina o comando de entrada para o contêiner Lambda
CMD ["main.webhook_navision"]

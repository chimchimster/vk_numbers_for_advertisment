FROM python3.10:slim
WORKDIR app/
COPY requirements.txt .
RUN pip install requirements.txt --no-cache-dir
COPY vk_numbers_for_advertisment .
CMD ["python3", "vk_numbers_for_advertisment/finder.py"]

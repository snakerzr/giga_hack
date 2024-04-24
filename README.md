# 1. Перейти в папку, где будет проект и склонировать репозиторий

```
cd ./projects/
git clone https://github.com/snakerzr/giga_hack
```

# 2. Создание среды (при необходимости) и установка зависимостей

Создать среду в конде:
```
conda create -n giga_hack python=3.11
conda activate giga_hack
```

Установить зависимости:
```
pip install -r requirements.txt
```

# 3. Апи ключи к гигачату

См. файл (.env.example), заполни, переименуй в `.env`

Минимум - заполнить CREDS, остальное опционально

В CREDS должно идти вот это:
![alt text](imgs/image.png)


# 3. Запусти jupyter lab
```
jupyter lab
```

# 4. См. notebook/example.ipynb
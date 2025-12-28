---
title: 無標題

---


# 使用 Docker Compose 建置 Flask 與 MySQL 之全端系統

使用 **Docker Compose** 快速建置一個全端 CRUD 系統：  
- 後端：**Flask** 提供 RESTful API  
- 前端：**HTML / JavaScript**（由 Flask 提供頁面）  
- 資料庫：**MySQL**（Docker Container + Volume 持久化）

只要一行指令即可啟動整套服務，並支援資料庫資料持久化（容器重啟資料仍保留）。

---

## 系統架構

本系統採三層式架構：

- **Frontend**：HTML / JavaScript（由 Flask 提供）
- **Backend**：Flask RESTful API
- **Database**：MySQL（Docker Container，使用 Volume 持久化資料）

服務之間透過 Docker Compose 建立的內部網路通訊：  
後端使用 service name `db` 連線至 MySQL。

---

## 使用技術

- Docker
- Docker Compose
- Flask
- MySQL
- Python

---

## 專案結構

```text
flask-project/
├─ backend/
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ templates/
│  │  └─ index.html
│  └─ static/
│     ├─ main.js
│     └─ style.css
├─ db/
│  └─ init.sql
├─ Dockerfile
├─ docker-compose.yml
├─ .gitignore
└─ README.md
````

---

## 如何執行專案

### 1. 環境需求

請先安裝：

* Docker
* Docker Compose

---

### 2. 啟動系統

在專案根目錄執行：

```bash
docker compose up --build
```

> 第一次啟動會建置映像檔並初始化資料庫（若有 `db/init.sql`）。

---

### 3. 存取系統

* 前端介面（由 Flask 提供）：
  -> [http://localhost:5000](http://localhost:5000)

* API 測試端點（範例）：
  -> [http://localhost:5000/items](http://localhost:5000/items)

---

## API 測試方式

### 使用瀏覽器或 curl

```bash
curl http://localhost:5000/items
```

---

## 功能說明（CRUD）

* 新增資料（Create）
* 查詢資料（Read）
* 刪除資料（Delete）


---

## Docker 說明

### Dockerfile

`Dockerfile` 用於建置後端 Flask 應用程式映像檔，包含：

* 安裝 Python 套件（`requirements.txt`）
* 複製專案程式碼
* 啟動 Flask 服務

---

### docker-compose.yml

Docker Compose 負責協調多個服務：

* `backend`：Flask 應用程式
* `db`：MySQL 資料庫

並透過以下機制提升穩定性：

* `depends_on`：確保服務啟動順序
* `healthcheck`：確認 MySQL 已可連線後再讓後端開始工作
* `volumes`：保存 MySQL 資料（持久化）

---

## 資料庫持久化（Volume）

本專案使用 Docker Volume 將 MySQL 資料存放於容器外部：
即使容器停止、刪除或重啟，只要 Volume 未被刪除，資料就會保留。


---

## 常用指令

### 背景啟動

```bash
docker compose up -d --build
```

### 停止服務

```bash
docker compose down
```

### 觀看 logs

```bash
docker compose logs -f
```

### 重新建置並啟動

```bash
docker compose up --build
```



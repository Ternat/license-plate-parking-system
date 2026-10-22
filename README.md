# License Plate Recognition Smart Parking System
# 车牌识别智能停车系统

<div align="center">

**An end-to-end Automatic License Plate Recognition (ALPR) smart parking management system powered by deep learning.**

**一个基于深度学习的端到端车牌识别（ALPR）智能停车管理系统。**

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](backend/requirements.txt)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)](backend/requirements.txt)
[![Vue 3](https://img.shields.io/badge/Vue_3-4FC08D?logo=vuedotjs&logoColor=white)](frontend/package.json)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)](frontend/package.json)
[![Element Plus](https://img.shields.io/badge/Element_Plus-409EFF?logo=element&logoColor=white)](frontend/package.json)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-detection-FFB800)](backend/weights/best.pt)

</div>

---

## Overview / 项目简介

This project is an **Automatic License Plate Recognition (ALPR) smart parking system**. It combines **YOLOv8 object detection with OCR** to automatically locate and recognise vehicle license plates, and provides a complete parking workflow: vehicle entry registration, exit billing, historical record query and rate management.

本项目是一套**车牌识别智能停车管理系统**，结合 **YOLOv8 目标检测与 OCR**，实现车牌的自动定位与识别，并提供完整的停车业务流程：车辆入场登记、出场计费、历史记录查询与费率管理。

The core ALPR pipeline / 核心识别流程：

```
Image input → Enhancement (CLAHE) → Detection (YOLOv8)
            → Perspective correction → OCR (fast-plate-ocr) → Persist & display
```

---

## Features / 功能特性

| Feature | Description |
| --- | --- |
| Admin login | JWT authentication with a configurable demo account |
| Vehicle entry | Upload a vehicle image; the plate is auto-detected and recognised, and entry time is recorded |
| Vehicle exit | Upload an exit image; the plate is matched and the parking duration and fee are calculated |
| Billing rule | First 2 hours free, then 5.0 per hour (configurable) |
| Record query | Search, filter and export historical parking records |
| Rate management | Adjust the hourly rate from the admin panel |
| Recognition test | Test the ALPR pipeline standalone without creating a parking record |

---

## Screenshots / 界面预览

### Login / 登录
![Login](docs/screenshots/login.png)

### License Plate Recognition / 车牌识别
![Recognition](docs/screenshots/recognition.png)

### Vehicle Entry / 车辆入场
![Vehicle Entry](docs/screenshots/entry.png)

### Vehicle Exit / 车辆出场
![Vehicle Exit](docs/screenshots/exit.png)

### Parking Records / 停车记录
![Parking Records](docs/screenshots/records.png)

### Price Management / 费率管理
![Price Management](docs/screenshots/price.png)

---

## My Contribution / 我的贡献

- Designed and implemented the end-to-end ALPR pipeline — image enhancement (CLAHE + denoising), YOLOv8 license-plate detection, perspective correction, and OCR integration.
- Fine-tuned YOLOv8s on license-plate images (reaching ~0.90 mAP@0.5) and wired the trained weights into the serving pipeline.
- Built the FastAPI backend — JWT authentication, vehicle entry/exit workflow, duration & fee calculation, record query, and pricing management.
- Built the Vue 3 frontend — all views and components, routing with authentication guards, and API integration.
- Integrated third-party components (fast-plate-ocr, OpenCV) into a cohesive, deployable system.

- 独立设计与实现端到端 ALPR 流水线——图像增强（CLAHE + 去噪）、YOLOv8 车牌检测、透视校正与 OCR 集成。
- 在车牌图像上微调 YOLOv8s（mAP@0.5 约 0.90），并将训练权重接入推理流水线。
- 构建 FastAPI 后端——JWT 认证、车辆入场/出场流程、时长与费用计算、记录查询、费率管理。
- 构建 Vue 3 前端——全部页面与组件、带鉴权守卫的路由、API 集成。
- 集成第三方组件（fast-plate-ocr、OpenCV），形成一套可部署的完整系统。

---

## Design Decisions / 设计决策

1. **CPU-first inference** — the model runs on CPU by default (`DEVICE=cpu`). This keeps the demo portable and reproducible on any machine with no GPU/driver setup; YOLOv8s is light enough for acceptable latency. `DEVICE=cuda` is available for GPU acceleration.
2. **Perspective correction before OCR** — plates are often tilted by the camera angle in real parking scenes. A homography-based rectification (Canny → contour → 4-point approximation → warp) normalises the plate before character recognition, which measurably improves OCR on angled shots.
3. **Modular pipeline stages** — enhancement, detection, correction and OCR are isolated modules, so each can be tested or replaced independently; intermediate images are saved for debugging.
4. **Stateless JWT + configurable demo account** — authentication is stateless (JWT). The demo account is compared against configuration values, and a bcrypt hash/verify helper is kept in `security.py` for a real user store — keeping the demo dependency-free while being explicit about the trade-off.
5. **SQLite persistence** — zero-configuration storage that is auto-created on first run.
6. **Billing: `ceil()` of chargeable hours** — after the free period, any started hour is charged in full (UK "per started hour" style).

1. **CPU 优先推理** —— 模型默认在 CPU 上运行（`DEVICE=cpu`）。这让演示在任何机器上都能直接复现，无需 GPU/驱动配置；YOLOv8s 足够轻量，延迟可接受。需要时可通过 `DEVICE=cuda` 启用 GPU 加速。
2. **OCR 前的透视校正** —— 真实停车场景中，车牌常因摄像头角度而倾斜。基于单应变换的校正（Canny → 轮廓 → 四角拟合 → 透视变换）在字符识别前对车牌进行归一化，显著改善倾斜拍摄下的 OCR 效果。
3. **模块化的流水线阶段** —— 增强、检测、校正、OCR 彼此独立，便于单独测试或替换；中间图像会保存下来用于调试。
4. **无状态 JWT + 可配置演示账号** —— 认证采用无状态 JWT。演示账号与配置值比对，同时在 `security.py` 中保留 bcrypt 哈希/校验函数，以备接入真实用户存储——在保持演示零依赖的同时，明确说明这一取舍。
5. **SQLite 持久化** —— 零配置存储，首次运行时自动创建。
6. **计费：对可收费小时向上取整 `ceil()`** —— 免费时段之后，不足一小时按一小时计费（英国"按已开始小时计费"惯例）。

---

## Tech Stack / 技术栈

**Backend / 后端**

| Technology | Purpose |
| --- | --- |
| [FastAPI](https://fastapi.tiangolo.com/) | REST API framework / REST API 框架 |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM + SQLite |
| [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) | License-plate detection / 车牌检测 |
| [fast-plate-ocr](https://github.com/ankandrew/fast-plate-ocr) | Plate OCR / 车牌 OCR |
| [OpenCV](https://opencv.org/) | Image enhancement / perspective correction / 图像增强与透视校正 |
| [python-jose](https://github.com/mpdavis/python-jose) + [passlib](https://passlib.readthedocs.io/) | JWT and password hashing / JWT 与密码哈希 |

**Frontend / 前端**

| Technology | Purpose |
| --- | --- |
| [Vue 3](https://vuejs.org/) | UI framework / UI 框架 |
| [Vite](https://vitejs.dev/) | Build tool & dev server / 构建工具与开发服务器 |
| [Element Plus](https://element-plus.org/) | UI component library / UI 组件库 |
| [Pinia](https://pinia.vuejs.org/) + [Vue Router](https://router.vuejs.org/) | State management & routing / 状态管理与路由 |
| [Axios](https://axios-http.com/) | HTTP client / HTTP 客户端 |

---

## Getting Started / 快速开始

### Requirements / 环境要求

- **Python** 3.10 / 3.11 (3.12+ not supported)
- **Node.js** 18+ (Vite 5)
- Ports `8000` (backend) and `3001` (frontend) free

### 1. Backend / 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

> On first start the YOLOv8 and OCR models are loaded, which takes about 20–30 seconds.
> The SQLite database `parking.db` is created automatically on first run.

### 2. Frontend / 前端

```bash
cd frontend
npm install
npm run dev
```

### 3. Access / 访问

| Entry | URL |
| --- | --- |
| Frontend | http://localhost:3001 |
| API docs (Swagger) | http://localhost:8000/docs |

**Default account / 默认账号**: `admin` / `123456`

---

## Demo: Complete Entry-to-Exit Flow / 演示：完整入场—出场流程

A full entry → exit flow can be reproduced with the commands below (run from the `backend/` directory with both servers started):

```bash
# 1. Login and store the token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"123456"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['data']['access_token'])")

# 2. Vehicle entry — the plate is recognised and the entry is recorded
curl -X POST http://localhost:8000/api/v1/parking/entry \
  -H "Authorization: Bearer $TOKEN" -F "file=@../test_images/2.jpg"

# 3. Vehicle exit — the plate is matched and duration + fee are computed
curl -X POST http://localhost:8000/api/v1/parking/exit \
  -H "Authorization: Bearer $TOKEN" -F "file=@../test_images/2.jpg"

# 4. Inspect the parking records
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/records/all"
```

> A quick entry → exit produces a fee of `0` (within the free period); longer stays are charged `5.0` per started hour beyond the first 2 free hours.

完整入场—出场流程可用上面同一组命令复现（在 `backend/` 目录下、前后端均已启动时执行）。快速入场再出场费用为 `0`（在免费时段内）；停留更长则超出 2 小时免费期后，按每小时 `5.0` 计费。

---

## Testing / 测试

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

The test suite (`backend/tests/`) covers the key business-logic edge cases:

- Duplicate entry rejection (a plate already parked cannot enter again)
- Billing boundaries (free-period edge and hourly `ceil()` rounding)
- Exit without an active record
- Authentication failure (wrong username / password) and JWT round-trip

测试套件（`backend/tests/`）覆盖关键业务边界：

- 重复入场拒绝（已停放的车辆不能再次入场）
- 计费边界（免费时段临界点与按小时向上取整）
- 无活动记录离场
- 认证失败（错误的用户名 / 密码）与 JWT 往返校验

---

## Limitations / 局限说明

- Recognition quality depends on image quality — low light, blur, occlusion, or a plate that is too small may cause detection or OCR to fail (a "no plate detected" error is returned rather than a wrong guess).
- Non-UK / non-standard plate formats may be misrecognised, since the model and OCR target UK-style plates.
- If multiple plates appear in one frame, only the highest-confidence detection is used.
- CPU inference is slower than GPU, and latency grows with larger images.
- The demo account compares credentials against configuration values in plaintext (see Design Decisions); a production deployment should hash credentials and use a real user store.

- 识别质量取决于图像质量——低光照、模糊、遮挡或车牌过小都可能导致检测或 OCR 失败（此时返回"未检测到车牌"错误，而不是给出错误结果）。
- 非英国 / 非标准车牌格式可能被误识别，因为模型与 OCR 面向英式车牌。
- 一帧中出现多块车牌时，仅使用置信度最高的检测结果。
- CPU 推理比 GPU 慢，且大图下延迟更高。
- 演示账号以明文与配置值比对（见设计决策）；生产部署应使用哈希存储并接入真实用户存储。

---

## Project Structure / 项目结构

```
backend/
  app/
    algorithm/          # ALPR pipeline: enhance -> detect -> correct -> OCR
    api/v1/endpoints/   # auth / parking / recognition / records / pricing
    core/               # config, database, security
    models/             # SQLAlchemy models
    schemas/            # Pydantic validation
    services/           # business logic (parking / records)
    utils/              # logging, image utilities
  tests/                # pytest suite (billing, entry/exit, auth)
  weights/best.pt       # YOLOv8 trained weights (22MB)
frontend/
  src/
    views/              # login, layout, recognition, entry/exit, records, pricing
    components/         # reusable components (image upload, etc.)
    api/                # Axios wrappers
    router/             # router with auth guards
test_images/            # sample vehicle images
docs/screenshots/       # UI screenshots
```

---

## Author / 作者

**Li Wenhao** · [University of Aberdeen](https://www.abdn.ac.uk/)

> Contact / 联系方式：[13798873528@163.com](mailto:13798873528@163.com) · [GitHub](https://github.com/Ternat) · [LinkedIn](https://linkedin.com/in/wenhao-li-4b9769437)

---

## License / 许可

This project is open-sourced under the [MIT License](LICENSE). 本项目代码采用 [MIT License](LICENSE) 开源。

> Third-party components (e.g. YOLOv8, fast-plate-ocr) are subject to their own licenses. 第三方组件（如 YOLOv8、fast-plate-ocr 等）遵循其各自的许可证。
